from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Iterable

from .phase3_source import parse_fixed_width_directive, parse_phalam, parse_vikalpam
from .ast import (
    Assign,
    Bind,
    BinaryValue,
    Block,
    BoolLiteral,
    BytesLiteral,
    Call,
    CallValue,
    CompareEq,
    CompareLt,
    Condition,
    Decrease,
    Display,
    ForwardDecl,
    ForEachDestructure,
    Invariant,
    ListLiteral,
    MapLiteral,
    ModuleDef,
    NilLiteral,
    Panic,
    Pop,
    Phase3Bind,
    PostCondition,
    PreCondition,
    FieldContains,
    FieldGet,
    FieldSet,
    FloatLiteral,
    FunctionDef,
    HeapAlloc,
    HeapFree,
    HeapLoad,
    HeapStore,
    Assert,
    Break,
    ConstDecl,
    Continue,
    CountedFor,
    Defer,
    ForEach,
    Guard,
    If,
    InfiniteLoop,
    Increase,
    Match,
    MatchArm,
    ImportDirective,
    ImportSymbol,
    ReexportDef,
    NewtypeDecl,
    ListAppend,
    ListGet,
    ListInit,
    ListLength,
    ListMap,
    ListFilter,
    ListReduce,
    ListAll,
    ListScan,
    ListZip,
    ListEnumerate,
    ListAny,
    ImmutableListInit,
    ImmutableListAppend,
    ListComprehension,
    LazyIterNew,
    LazyIterNext,
    GeneratorNew,
    GeneratorNext,
    Yield,
    PipelineChain,
    MatchExpr,
    ResultBind,
    DataQuery,
    RuleDecl,
    RuleInvoke,
    MemoFunction,
    AlgebraicTypeDecl,
    Literal,
    MapContains,
    MapGet,
    MapInit,
    MapPut,
    Multiply,
    PatternLiteral,
    PatternWildcard,
    Program,
    Propagate,
    Reference,
    RecordInit,
    ClassDecl,
    ClassNew,
    ClassMethodCall,
    ClassReflect,
    GenericRecordDecl,
    GroupValue,
    InstanceFinalize,
    LifetimeDecl,
    MethodCall,
    MethodReflect,
    PropertyGet,
    StaticMethodCall,
    RecordTypeDecl,
    Return,
    TraitDecl,
    TraitImpl,
    TypeReflect,
    Throw,
    TryCatch,
    TypeAliasDecl,
    TypeConvert,
    Until,
    While,
    Statement,
    TextConcat,
    TextContains,
    TextGet,
    TextLength,
    TextLiteral,
    TextSlice,
    UnsafeEnter,
    UnsafeExit,
    Value,
)
from .errors import MorphologyError, ParseError
from .grammar import VERB_FRAMES, Analysis, FrameOperation, PartOfSpeech, Role, VerbFrame
from .identifiers import IdentifierError, canonical_identifier
from .learning_mode import enrich_error
from .morphology import split_sentences
from .morphology_facade import get_default_facade
from .parser_core import (
    parse_bytes_payload,
    parse_call_arg_tokens,
    parse_condition_tokens,
    parse_value_tokens,
)
from .source_context import span_at
from .source_pipeline import prepare_source
import re

_BLOCK_END_MARKERS = frozenset({"antam", "anta", "yadi", "punaḥ", "punah", "vidhānam", "vidhanam", "samāpanam", "samapanam"})
_TIER_MARKERS = {
    "surakṣitam": "surakshita",
    "surakshitam": "surakshita",
    "rakṣitam": "rakshita",
    "rakshitam": "rakshita",
    "arakṣitam": "arakshita",
    "arakshitam": "arakshita",
}
_TEXT_MARKERS = frozenset({"vākyam", "vakyam", "śabdam", "shabdam"})
_ASSIGN_VERBS = frozenset({"nidadhāti", "sthāpayati"})
_DISPLAY_VERBS = frozenset({"darśayati", "prakāśayati"})
_SOURCE_INT_WORDS = {
    "śūnya": 0,
    "shunya": 0,
    "eka": 1,
    "dvi": 2,
    "tri": 3,
    "catur": 4,
    "pañca": 5,
    "panca": 5,
    "ṣaṭ": 6,
    "sat": 6,
    "sapta": 7,
    "aṣṭa": 8,
    "asta": 8,
    "nava": 9,
    "daśa": 10,
    "dasha": 10,
}
_BINARY_VALUE_OPERATORS = {
    "yoga": "add",
    "yogena": "add",
    "vyavakalanam": "subtract",
    "hīna": "subtract",
    "hina": "subtract",
    "guṇanam": "multiply",
    "gunanam": "multiply",
    "guṇena": "multiply",
    "gunena": "multiply",
    "bhāga": "divide",
    "bhaga": "divide",
    "bhāgena": "divide",
    "bhagena": "divide",
}
_PHASE5_DIRECTIVE_PREFIXES: dict[str, str] = {
    "prasāraḥ": "propagate",
    "prasarah": "propagate",
    "vikṣepaḥ": "throw",
    "viksepah": "throw",
    "vipattim": "panic",
    "āgrahītvā": "try/catch",
    "agrahitva": "try/catch",
    "pūrvaśartam": "precondition",
    "purvasartam": "precondition",
    "purvaśartam": "precondition",
    "pūrvasartam": "precondition",
    "uttaraśartam": "postcondition",
    "uttarasartam": "postcondition",
    "nityaśartam": "invariant",
    "nityasartam": "invariant",
}


def parse_program(source: str) -> Program:
    prepared = prepare_source(source)
    facade = get_default_facade()
    facade.strict = prepared.strict_paninian
    try:
        return _parse_program_body(prepared.text, facade=facade, prepared=prepared)
    except (ParseError, MorphologyError) as exc:
        raise enrich_error(
            exc,
            original=prepared.original,
            script=prepared.normalized.script,
        ) from exc  # learning suggestions only; compilation stays strict


def _script_label(source_text: str | None) -> str | None:
    if not source_text:
        return None
    from .script_normalize import detect_script

    return detect_script(source_text).value


def _parse_program_body(
    source: str,
    *,
    facade,
    prepared=None,
) -> Program:
    sentences = split_sentences(source)
    sentence_starts = _sentence_start_offsets(source, sentences)
    statements: list[Statement] = []
    functions: list[FunctionDef] = []
    pending_decorators: list[str] = []
    modules: list[ModuleDef] = []

    index = 0
    current_module: str | None = None
    module_functions: list[FunctionDef] = []
    module_exports: set[str] = set()
    module_reexports: list[ReexportDef] = []
    known_modules: set[str] = set()
    safety_tier = "surakshita"
    type_aliases: list[TypeAliasDecl] = []
    newtypes: list[NewtypeDecl] = []
    record_types: list[RecordTypeDecl] = []
    generic_records: list[GenericRecordDecl] = []
    traits: list[TraitDecl] = []
    trait_impls: list[TraitImpl] = []
    classes: list[ClassDecl] = []
    lifetimes: list[LifetimeDecl] = []
    constants: list[ConstDecl] = []
    imports: list[ImportDirective] = []
    algebraic_types: list[AlgebraicTypeDecl] = []
    rules: list[RuleDecl] = []

    def _flush_module() -> None:
        nonlocal current_module, module_functions, module_exports, module_reexports
        if current_module and (module_functions or module_exports or module_reexports):
            modules.append(
                ModuleDef(
                    current_module,
                    tuple(module_functions),
                    frozenset(module_exports),
                    tuple(module_reexports),
                )
            )
        current_module = None
        module_functions = []
        module_exports = set()
        module_reexports = []

    while index < len(sentences):
        sentence = sentences[index].strip()
        if not sentence:
            index += 1
            continue
        # Allow stray block terminators at top-level (e.g. examples with trailing antam.)
        if _is_marker_sentence(sentence, {"antam", "anta"}):
            index += 1
            continue

        text_statement = _parse_text_sentence(sentence)
        if text_statement is not None:
            statements.append(text_statement)
            index += 1
            continue

        header = _parse_directive_header(sentence, known_modules=known_modules)
        if header is not None:
            kind, payload = header
            if kind == "tier":
                safety_tier = payload
                index += 1
                continue
            collection_stmt = _collection_statement_from_directive(kind, payload)
            if collection_stmt is not None:
                statements.extend(collection_stmt)
                index += 1
                continue
            if kind == "module":
                _flush_module()
                current_module = payload
                known_modules.add(current_module)
                index += 1
                continue
            if kind == "export":
                module_exports.add(str(payload))
                index += 1
                continue
            if kind == "reexport":
                module_exports.add(payload.name)  # type: ignore[union-attr]
                module_reexports.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "import":
                directive = payload  # type: ignore[assignment]
                imports.append(directive)
                local_module_name = directive.alias or _default_import_name(directive.module_path)
                if local_module_name:
                    known_modules.add(local_module_name)
                index += 1
                continue
            if kind == "block":
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"antam", "anta"},
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(Block(body))
                continue
            if kind == "bind":
                target, value, immutable = payload  # type: ignore[misc]
                statements.append(Bind(target, value, immutable=immutable))
                index += 1
                continue
            if kind == "bind_owned":
                target, value, immutable, ownership, lifetime = payload  # type: ignore[misc]
                statements.append(
                    Bind(
                        target,
                        value,
                        immutable=immutable,
                        ownership=ownership,
                        lifetime=lifetime,
                    )
                )
                index += 1
                continue
            if kind == "forward":
                statements.append(ForwardDecl(str(payload)))
                index += 1
                continue
            if kind == "pop":
                statements.append(Pop(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "bytes":
                target, data = payload  # type: ignore[misc]
                statements.append(Bind(target, BytesLiteral(data), immutable=True))
                index += 1
                continue
            if kind == "phase3_bind":
                normalized = list(payload)  # type: ignore[arg-type]
                while len(normalized) < 5:
                    normalized.append(None)
                target, opcode, operand, value, items = normalized[:5]
                if items is None:
                    items = ()
                statements.append(Phase3Bind(target, opcode, operand, value=value, items=tuple(items)))
                index += 1
                continue
            if kind == "phase3_some":
                target, value_tokens = payload  # type: ignore[misc]
                value = _value_from_tokens(value_tokens, known_modules=known_modules)
                if value is not None:
                    statements.append(Phase3Bind(target, "option_some", value=value))
                index += 1
                continue
            if kind == "phase3_result":
                target, ok, value_tokens = payload  # type: ignore[misc]
                value = _value_from_tokens(value_tokens, known_modules=known_modules)
                if value is not None:
                    opcode = "result_ok" if ok else "result_err"
                    statements.append(Phase3Bind(target, opcode, value=value))
                index += 1
                continue
            if kind == "phase3_tuple":
                target, values = payload  # type: ignore[misc]
                statements.append(
                    Phase3Bind(target, "tuple_new", operand=len(values), items=values),
                )
                index += 1
                continue
            if kind == "phase3_set":
                target, values = payload  # type: ignore[misc]
                statements.append(Phase3Bind(target, "set_new", items=values))
                index += 1
                continue
            if kind == "list_literal":
                target, elements = payload  # type: ignore[misc]
                statements.append(Bind(target, ListLiteral(elements)))
                index += 1
                continue
            if kind == "map_literal":
                target, entries = payload  # type: ignore[misc]
                statements.append(Bind(target, MapLiteral(entries)))
                index += 1
                continue
            if kind == "record_literal":
                target, fields = payload  # type: ignore[misc]
                statements.append(RecordInit(target))
                for field_key, field_val in fields:
                    statements.append(FieldSet(target, field_key, field_val))
                index += 1
                continue
            if kind == "decorator":
                pending_decorators.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "function":
                header = payload  # type: ignore[assignment]
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"samāpanam", "samapanam"},
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                fn = FunctionDef(
                    header.name,
                    body,
                    module=current_module,
                    params=header.params,
                    param_defaults=header.param_defaults,
                    variadic_param=header.variadic_param,
                    param_types=header.param_types,
                    effect=header.effect,
                    decorators=tuple(pending_decorators) + header.decorators,
                    capture_mut=header.capture_mut,
                    is_inline=header.is_inline,
                    is_naked=header.is_naked,
                    is_compile_time=header.is_compile_time,
                    named_returns=header.named_returns,
                    abi_name=header.abi_name,
                )
                pending_decorators.clear()
                if current_module:
                    module_functions.append(fn)
                else:
                    functions.append(fn)
                continue
            if kind == "if":
                condition = payload
                index += 1
                then_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"anyathā", "anyatha", "athavā", "athava", "antam", "anta"},
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                elif_branches: list[tuple[Condition, tuple[Statement, ...]]] = []
                while index < len(sentences):
                    elif_tokens = _directive_tokens(sentences[index])
                    if not elif_tokens or elif_tokens[0] not in {"athavā", "athava"}:
                        break
                    if len(elif_tokens) < 2 or elif_tokens[1] not in {"yadi"}:
                        break
                    elif_cond = _parse_condition_tokens(elif_tokens[2:], known_modules=known_modules)
                    if elif_cond is None:
                        break
                    index += 1
                    elif_body, index = _collect_until(
                        sentences,
                        index,
                        end_markers={"anyathā", "anyatha", "athavā", "athava", "antam", "anta"},
                        stop_before_markers=True,
                        known_modules=known_modules,
                        facade=facade,
                        source_text=source,
                    )
                    elif_branches.append((elif_cond, elif_body))
                else_body: tuple[Statement, ...] = ()
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"anyathā", "anyatha"}):
                    index += 1
                    else_body, index = _collect_until(
                        sentences,
                        index,
                        end_markers=_BLOCK_END_MARKERS,
                        stop_before_markers=True,
                        known_modules=known_modules,
                        facade=facade,
                        source_text=source,
                    )
                if index < len(sentences) and _is_marker_sentence(
                    sentences[index], {"antam", "anta"}
                ):
                    index += 1
                statements.append(If(condition, then_body, else_body, tuple(elif_branches)))
                continue
            if kind == "while":
                condition = payload
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(
                    sentences[index], {"antam", "anta"}
                ):
                    index += 1
                statements.append(While(condition, body))
                continue
            if kind == "call":
                if len(payload) == 4:  # type: ignore[arg-type]
                    module_name, fn_name, args, kwargs = payload
                    statements.append(Call(fn_name, module=module_name, args=args, kwargs=kwargs))
                else:
                    module_name, fn_name, args = payload  # type: ignore[misc]
                    statements.append(Call(fn_name, module=module_name, args=args))
                index += 1
                continue
            if kind == "assign":
                target, value = payload
                statements.append(Assign(target, value))
                index += 1
                continue
            if kind == "display":
                statements.append(Display(payload))
                index += 1
                continue
            if kind == "return":
                statements.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "type_alias":
                type_aliases.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "newtype":
                newtypes.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "record_type":
                record_types.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "generic_record":
                generic_records.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "trait":
                traits.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "trait_impl":
                trait_impls.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "class_decl":
                classes.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "class_new":
                target, class_name, args = payload  # type: ignore[misc]
                statements.append(ClassNew(target, class_name, args))
                index += 1
                continue
            if kind == "method_call":
                target, receiver, method, args = payload  # type: ignore[misc]
                statements.append(MethodCall(target, receiver, method, args))
                index += 1
                continue
            if kind == "static_method_call":
                target, class_name, method, args = payload  # type: ignore[misc]
                statements.append(StaticMethodCall(target, class_name, method, args))
                index += 1
                continue
            if kind == "class_method_call":
                target, class_name, method, args = payload  # type: ignore[misc]
                statements.append(ClassMethodCall(target, class_name, method, args))
                index += 1
                continue
            if kind == "property_get":
                target, receiver, prop = payload  # type: ignore[misc]
                statements.append(PropertyGet(target, receiver, prop))
                index += 1
                continue
            if kind == "instance_finalize":
                statements.append(InstanceFinalize(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "class_reflect":
                target, receiver = payload  # type: ignore[misc]
                statements.append(ClassReflect(target, receiver))
                index += 1
                continue
            if kind == "method_reflect":
                target, receiver, method = payload  # type: ignore[misc]
                statements.append(MethodReflect(target, receiver, method))
                index += 1
                continue
            if kind == "lifetime":
                lifetimes.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "type_reflect":
                statements.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "const":
                constants.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "type_convert":
                target, to_type, value = payload  # type: ignore[misc]
                statements.append(TypeConvert(target, to_type, value))
                index += 1
                continue
            if kind == "match":
                subject = payload
                index += 1
                arms, index = _collect_match_arms(sentences, index, known_modules=known_modules)
                statements.append(Match(subject, arms))
                continue
            if kind == "match_expr":
                target, subject = payload  # type: ignore[misc]
                index += 1
                arms, index = _collect_match_arms(sentences, index, known_modules=known_modules)
                statements.append(MatchExpr(target, subject, arms))
                continue
            if kind == "rule_decl":
                rules.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "rule_invoke":
                target, rule_id, context = payload  # type: ignore[misc]
                statements.append(RuleInvoke(target, rule_id, context))
                index += 1
                continue
            if kind == "algebraic_type":
                algebraic_types.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "guard":
                condition = payload
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(Guard(condition, body))
                continue
            if kind == "until":
                condition = payload
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(Until(condition, body))
                continue
            if kind == "counted_for":
                counter, start, end = payload  # type: ignore[misc]
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(CountedFor(counter, start, end, body))
                continue
            if kind == "foreach":
                item, container = payload  # type: ignore[misc]
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(ForEach(item, container, body))
                continue
            if kind == "foreach_destructure":
                names, container = payload  # type: ignore[misc]
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(ForEachDestructure(names, container, body))
                continue
            if kind == "infinite":
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(InfiniteLoop(body))
                continue
            if kind == "break":
                statements.append(Break(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "continue":
                statements.append(Continue(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "defer":
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                statements.append(Defer(body))
                continue
            if kind == "assert":
                condition, message = payload  # type: ignore[misc]
                statements.append(Assert(condition, message))
                index += 1
                continue
            if kind == "propagate":
                statements.append(Propagate(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "throw":
                statements.append(Throw(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "panic":
                statements.append(Panic(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "try_catch":
                error_name = str(payload)
                header_start = sentence_starts[index] if index < len(sentence_starts) else 0
                header_span = span_at(source, header_start, header_start + len(sentences[index]))
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"anyathā", "anyatha", "antam", "anta"},
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source,
                )
                handler: tuple[Statement, ...] = ()
                saw_else = index < len(sentences) and _is_marker_sentence(sentences[index], {"anyathā", "anyatha"})
                if saw_else:
                    index += 1
                    handler, index = _collect_until(
                        sentences,
                        index,
                        end_markers={"antam", "anta"},
                        stop_before_markers=True,
                        known_modules=known_modules,
                        facade=facade,
                        source_text=source,
                    )
                if not saw_else:
                    raise ParseError(
                        "āgrahītvā block requires anyathā handler block before antam.",
                        hint="Use: āgrahītvā <name>. ... anyathā. ... antam.",
                        span=header_span,
                        original_script=_script_label(source),
                    )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                else:
                    raise ParseError(
                        "āgrahītvā block is missing terminating antam.",
                        hint="Close the try/catch block with antam.",
                        span=header_span,
                        original_script=_script_label(source),
                    )
                if not handler:
                    raise ParseError(
                        "āgrahītvā handler body cannot be empty.",
                        hint="Add at least one statement between anyathā and antam.",
                        span=header_span,
                        original_script=_script_label(source),
                    )
                statements.append(TryCatch(body, error_name, handler))
                continue
            if kind == "precondition":
                statements.append(PreCondition(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "postcondition":
                statements.append(PostCondition(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "invariant":
                statements.append(Invariant(payload))  # type: ignore[arg-type]
                index += 1
                continue

        if _is_marker_sentence(sentence, {"samāpanam", "samapanam"}):
            _flush_module()
            index += 1
            continue

        sentence_start = sentence_starts[index] if index < len(sentence_starts) else 0
        _raise_if_malformed_phase5_directive(sentence, source=source, sentence_start=sentence_start)
        statements.append(parse_sentence(sentence, facade=facade, source_text=source, sentence_start=sentence_start))
        index += 1

    _flush_module()

    return Program(
        tuple(statements),
        tuple(functions),
        tuple(modules),
        imports=tuple(imports),
        safety_tier=safety_tier,
        type_aliases=tuple(type_aliases),
        newtypes=tuple(newtypes),
        record_types=tuple(record_types),
        generic_records=tuple(generic_records),
        traits=tuple(traits),
        trait_impls=tuple(trait_impls),
        classes=tuple(classes),
        lifetimes=tuple(lifetimes),
        constants=tuple(constants),
        algebraic_types=tuple(algebraic_types),
        rules=tuple(rules),
    )


def _sentence_start_offsets(source: str, sentences: list[str]) -> list[int]:
    starts: list[int] = []
    cursor = 0
    for sentence in sentences:
        offset = source.find(sentence, cursor)
        if offset < 0:
            offset = source.find(sentence)
        if offset < 0:
            offset = cursor
        starts.append(offset)
        cursor = offset + len(sentence)
    return starts


def parse_sentence(
    sentence: str,
    *,
    facade=None,
    source_text: str | None = None,
    sentence_start: int = 0,
) -> Statement:
    if facade is None:
        facade = get_default_facade()
    span = span_at(source_text or sentence, sentence_start, sentence_start + len(sentence))
    script_label = _script_label(source_text)
    try:
        analyses = facade.analyze_sentence(
            sentence,
            source_text=source_text,
            sentence_start=sentence_start,
        )
    except MorphologyError as exc:
        if exc.span is None:
            exc.span = span
        raise
    verbs = [item for item in analyses if item.pos == PartOfSpeech.VERB]
    if len(verbs) != 1:
        raise ParseError(
            f"Expected exactly one finite verb, found {len(verbs)} in {sentence!r}",
            span=span,
            original_script=script_label,
        )

    verb = verbs[0]
    try:
        frame = VERB_FRAMES[verb.surface]
    except KeyError as exc:
        raise ParseError(
            f"No verb frame has been declared for {verb.surface!r}",
            hint="Declare the surface in data/verb_frames.json and rebuild the lexicon.",
            span=span,
            original_script=script_label,
        ) from exc

    try:
        _validate_verb_analysis(verb, frame)
        facade.validate_karaka(analyses, verb)
        roles = _roles_by_type(item for item in analyses if item.pos != PartOfSpeech.VERB)
        return FRAME_DISPATCH[frame.operation](frame, roles)
    except KeyError as exc:
        raise ParseError(
            f"No parser operation has been declared for {frame.operation.value!r}",
            hint="Add the operation to parser.FRAME_DISPATCH.",
            span=span,
            original_script=script_label,
        ) from exc
    except ParseError as exc:
        if exc.span is None:
            exc.span = span
        if exc.original_script is None:
            exc.original_script = script_label
        raise


FrameBuilder = Callable[[VerbFrame, dict[Role, list[Analysis]]], Statement]


def _build_assign(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Assign:
    return Assign(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        value=_value_from(_single(roles, _frame_role(frame, "value_role"))),
    )


def _build_increase(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Increase:
    return Increase(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        amount=_value_from(_single(roles, _frame_role(frame, "amount_role"))),
    )


def _build_decrease(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Decrease:
    return Decrease(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        amount=_value_from(_single(roles, _frame_role(frame, "amount_role"))),
    )


def _build_multiply(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Multiply:
    return Multiply(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        factor=_value_from(_single(roles, _frame_role(frame, "amount_role"))),
    )


def _build_display(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Display:
    return Display(value=_value_from(_single(roles, _frame_role(frame, "value_role"))))


FRAME_DISPATCH: dict[FrameOperation, FrameBuilder] = {
    FrameOperation.ASSIGN: _build_assign,
    FrameOperation.INCREASE: _build_increase,
    FrameOperation.DECREASE: _build_decrease,
    FrameOperation.MULTIPLY: _build_multiply,
    FrameOperation.DISPLAY: _build_display,
}


def _parse_directive_header(
    sentence: str,
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[str, object] | None:
    tokens = _directive_tokens(sentence)
    if not tokens:
        return None

    first = tokens[0]
    if first in {"kṣetram", "ksetram"} and len(tokens) >= 2:
        return ("module", tokens[1])

    if first in {"saṃskāraṃ", "samskaram", "saṃskāra", "samskara"} and len(tokens) >= 2:
        return ("decorator", _identifier_from_token(tokens[1]))

    if first in {"vidhānam", "vidhanam"} and len(tokens) >= 2:
        header = _parse_function_header_tokens(tokens)
        if header is not None:
            return ("function", header)

    if first in {"āhvānam", "ahvanam"}:
        if len(tokens) >= 4 and tokens[-1] in _ASSIGN_VERBS:
            value = _call_value_from_tokens(tokens[:-2], known_modules=known_modules)
            if value is not None:
                return ("assign", (_identifier_from_token(tokens[-2]), value))
        if len(tokens) >= 3 and tokens[-1] in _DISPLAY_VERBS:
            value = _call_value_from_tokens(tokens[:-1], known_modules=known_modules)
            if value is not None:
                return ("display", value)
        if len(tokens) >= 2:
            module_name, fn_name = _split_qualified_call_target(tokens[1], known_modules=known_modules)
            if module_name and len(tokens) >= 3 and not fn_name:
                args, kwargs = parse_call_arg_tokens(tokens[3:], known_modules=known_modules)
                return ("call", (module_name, tokens[2], args, kwargs))
            args, kwargs = parse_call_arg_tokens(tokens[2:], known_modules=known_modules)
            return ("call", (module_name, fn_name, args, kwargs))
        return None

    if first in {"pratyāvartanam", "pratyavartanam"}:
        ret = _parse_return_directive(tokens, known_modules=known_modules)
        if ret is not None:
            return ("return", ret)
        return None

    if first == "punaḥ" or first == "punah":
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("while", condition)
        return None

    if first == "yadi":
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("if", condition)
        return None

    if first in {"rakṣa", "raksha"}:
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("guard", condition)
        return None

    if first in {"yāvat", "yavat"}:
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("until", condition)
        return None

    if first in {"saṅkhyā", "sankhya"} and len(tokens) >= 4:
        counter = _identifier_from_token(tokens[1])
        start = _value_from_tokens(tokens[2:3], known_modules=known_modules)
        end = _value_from_tokens(tokens[3:], known_modules=known_modules)
        if start is not None and end is not None:
            return ("counted_for", (counter, start, end))

    if first in {"pratyekam"} and len(tokens) >= 4:
        # Check for destructuring pattern: pratyekam (a b) container
        raw_item = tokens[1]
        if raw_item.startswith("(") or (len(tokens) >= 3 and tokens[1] == "("):
            # collect names between ( and )
            joined = " ".join(tokens[1:])
            import re as _re
            m = _re.match(r"\(\s*([\w\s,]+)\s*\)", joined)
            if m:
                names = tuple(_identifier_from_token(n.strip()) for n in _re.split(r"[\s,]+", m.group(1)) if n.strip())
                remaining = joined[m.end():].split()
                container = _identifier_from_token(remaining[-1]) if remaining else ""
                return ("foreach_destructure", (names, container))
        item = _identifier_from_token(tokens[1])
        if tokens[2] in {"samūhe", "samuhe", "madhye"}:
            container = _identifier_from_token(tokens[3])
        else:
            container = _identifier_from_token(tokens[-1])
        return ("foreach", (item, container))

    if first in {"anavaratam", "anavaratam"}:
        return ("infinite", None)

    if first in {"viramaḥ", "viramah", "virama"}:
        label = _identifier_from_token(tokens[1]) if len(tokens) >= 2 else None
        return ("break", label)

    if first in {"agragamanam", "agragamana"}:
        label = _identifier_from_token(tokens[1]) if len(tokens) >= 2 else None
        return ("continue", label)

    if first in {"ante"}:
        return ("defer", None)

    if first in {"prasāraḥ", "prasarah", "prasara"} and len(tokens) >= 2:
        value = _value_from_tokens(tokens[1:], known_modules=known_modules)
        if value is not None:
            return ("propagate", value)

    if first in {"niścayaḥ", "nishcayah", "nishcaya"}:
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("assert", (condition, None))

    if first in {"prakāraḥ", "prakarah", "prakara"} and len(tokens) >= 4 and tokens[2] == "iti":
        return ("type_alias", TypeAliasDecl(tokens[1], tokens[3]))

    if first in {"navaprakāraḥ", "navaprakarah"} and len(tokens) >= 4 and tokens[2] == "iti":
        return ("newtype", NewtypeDecl(tokens[1], tokens[3]))

    if first in {"parivartana"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        to_type = tokens[2]
        value = _value_from_tokens(tokens[3:], known_modules=known_modules)
        if value is not None:
            return ("type_convert", (target, to_type, value))

    if first in {"vastu-prakāraḥ", "vastu-prakarah", "vastuprakarah"} and len(tokens) >= 4:
        name = tokens[1]
        if len(tokens) >= 5 and len(tokens[2]) == 1 and tokens[2].isalpha():
            type_param = tokens[2]
            fields = _parse_type_field_pairs(tokens[3:])
            if fields:
                return ("generic_record", GenericRecordDecl(name, type_param, fields))
        fields = _parse_type_field_pairs(tokens[2:])
        if fields:
            return ("record_type", RecordTypeDecl(name, fields))

    if first in {"abhilakṣaṇaṃ", "abhilakshanam", "abhilaksanam"} and len(tokens) >= 3:
        name = tokens[1]
        idx = 2
        type_param: str | None = None
        if len(tokens) >= 4 and len(tokens[2]) == 1 and tokens[2].isalpha():
            type_param = tokens[2]
            idx = 3
        methods = _parse_trait_methods(tokens[idx:])
        if methods:
            return ("trait", TraitDecl(name, type_param, methods))

    if first in {"sādhayati", "sadhayati"} and len(tokens) >= 3:
        return ("trait_impl", TraitImpl(tokens[1], tokens[2]))

    if first in {"prakāra-āharaṇam", "prakara-aharanam", "prakaraaharanam"} and len(tokens) >= 3:
        return ("type_reflect", TypeReflect(_identifier_from_token(tokens[1]), tokens[2]))

    if first in {"vargaḥ", "vargah"} and len(tokens) >= 4:
        decl = _parse_class_decl(tokens)
        if decl is not None:
            return ("class_decl", decl)

    if first in {"nirmāṇam", "nirmanam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        class_name = tokens[2]
        args = _values_from_tokens(tokens[3:], known_modules=known_modules)
        return ("class_new", (target, class_name, args))

    if first in {"paddhati-āhvānam", "paddhati-ahvanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        receiver = _identifier_from_token(tokens[2])
        method = _identifier_from_token(tokens[3])
        args = _values_from_tokens(tokens[4:], known_modules=known_modules)
        return ("method_call", (target, receiver, method, args))

    if first in {"sthira-paddhati-āhvānam", "sthira-paddhati-ahvanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        class_name = tokens[2]
        method = _identifier_from_token(tokens[3])
        args = _values_from_tokens(tokens[4:], known_modules=known_modules)
        return ("static_method_call", (target, class_name, method, args))

    if first in {"varga-paddhati-āhvānam", "varga-paddhati-ahvanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        class_name = tokens[2]
        method = _identifier_from_token(tokens[3])
        args = _values_from_tokens(tokens[4:], known_modules=known_modules)
        return ("class_method_call", (target, class_name, method, args))

    if first in {"guṇa-āharaṇam", "guna-aharanam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        receiver = _identifier_from_token(tokens[2])
        prop = _identifier_from_token(tokens[3])
        return ("property_get", (target, receiver, prop))

    if first in {"antima-saṃskāraṃ", "antima-samskaram", "antima-samskara"} and len(tokens) >= 2:
        receiver = _identifier_from_token(tokens[1])
        return ("instance_finalize", receiver)

    if first in {"varga-prakāra-āharaṇam", "varga-prakara-aharanam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        receiver = _identifier_from_token(tokens[2])
        return ("class_reflect", (target, receiver))

    if first in {"paddhati-prakāra-āharaṇam", "paddhati-prakara-aharanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        receiver = _identifier_from_token(tokens[2])
        method = _identifier_from_token(tokens[3])
        return ("method_reflect", (target, receiver, method))

    if first in {"āyuḥ", "ayuh", "āyuh"} and len(tokens) >= 2:
        lifetime_name = tokens[1]
        region = tokens[2] if len(tokens) >= 3 else None
        return ("lifetime", LifetimeDecl(lifetime_name, region))

    if first in {"yathā-artham", "yatha-artham"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        subject = _value_from_tokens(tokens[2:], known_modules=known_modules)
        if subject is not None:
            return ("match_expr", (target, subject))

    if first in {"yathā", "yatha"} and len(tokens) >= 2:
        subject = _value_from_tokens(tokens[1:], known_modules=known_modules)
        if subject is not None:
            return ("match", subject)

    if first in {"niyamaḥ", "niyamah"} and len(tokens) >= 4:
        rule_id = tokens[1]
        when_fn = _identifier_from_token(tokens[2])
        then_fn = _identifier_from_token(tokens[3])
        return ("rule_decl", RuleDecl(rule_id, when_fn, then_fn))

    if first in {"niyama-āhvānam", "niyama-ahvanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        rule_id = tokens[2]
        context = _value_from_tokens(tokens[3:], known_modules=known_modules)
        if context is not None:
            return ("rule_invoke", (target, rule_id, context))

    if first in {"prakāra-vikalpaḥ", "prakara-vikalpah", "prakaravikalpah"} and len(tokens) >= 3:
        name = tokens[1]
        variants = tuple(tokens[2:])
        return ("algebraic_type", AlgebraicTypeDecl(name, variants))

    fw = parse_fixed_width_directive(first, tokens)
    if fw is not None:
        return fw

    if first in {"ati-pūrṇāṅka", "ati-purnanka", "ati-purnaanka"} and len(tokens) >= 4:
        if tokens[2] in {"asti", "aste"}:
            try:
                return ("phase3_bind", (_identifier_from_token(tokens[1]), "push_bigint", int(tokens[3])))
            except ValueError:
                pass

    if first in {"rāśi-saṅkhyā", "rashi-sankhya"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        if len(values) == 2:
            return ("phase3_bind", (target, "push_rational", None, None, values))

    if first in {"daśāṃśa-saṅkhyā", "dashamsha-sankhya"} and len(tokens) >= 4:
        if tokens[2] in {"asti", "aste"}:
            return ("phase3_bind", (_identifier_from_token(tokens[1]), "push_decimal", " ".join(tokens[3:])))

    if first in {"saṅkīrṇa-saṅkhyā", "sankirna-sankhya"} and len(tokens) >= 5:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        if len(values) == 2:
            return ("phase3_bind", (target, "push_complex", None, None, values))

    if first in {"akṣara-bījam", "akshara-bijam"} and len(tokens) >= 4:
        if tokens[2] in {"asti", "aste"}:
            try:
                return ("phase3_bind", (_identifier_from_token(tokens[1]), "push_scalar", int(tokens[3])))
            except ValueError:
                pass

    if first in {"vikalpam", "vikalpa"}:
        vk = parse_vikalpam(tokens)
        if vk is not None:
            return vk

    if first in {"phalam", "phala"}:
        pk = parse_phalam(tokens)
        if pk is not None:
            return pk

    if first in {"yugmam", "yugma"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        if values:
            return ("phase3_tuple", (target, values))

    if first in {"saṅgrahaḥ", "sangrahah", "samāhāraḥ", "samaharah"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_set", (target, values))

    if first in {"dviguṇa-samūhaḥ", "dviguna-samuha"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "deque_new", None, None, values))

    if first in {"nitya-samāhāraḥ", "nitya-samaharah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "frozen_set_new", None, None, values))

    if first in {"krama-kośaḥ", "krama-koshah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "ordered_map_new", None, None, values))

    if first in {"svataḥ-kośaḥ", "svatah-koshah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        default_value = _value_from_tokens(tokens[2:3], known_modules=known_modules)
        values = _values_from_tokens(tokens[3:], known_modules=known_modules)
        if default_value is not None:
            return ("phase3_bind", (target, "default_map_new", None, default_value, values))

    if first in {"gaṇanā-sañcayaḥ", "ganana-sanchayah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "counter_new", None, None, values))

    if first in {"panktī", "pankti"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "queue_new", None, None, values))

    if first in {"stūpaḥ", "stupah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "stack_new", None, None, values))

    if first in {"nyūna-śikharaḥ", "nyuna-shikharah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "heap_new", None, None, values))

    if first in {"prādhānya-panktī", "pradhanya-pankti"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "pq_new", None, None, values))

    if first in {"vṛkṣaḥ", "vrkshah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "tree_new", None, None, values))

    if first in {"jālakaḥ", "jalakah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "graph_new", None, None, values))

    if first in {"nāma-yuktiḥ", "nama-yuktih"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("phase3_bind", (target, "named_tuple_new", None, None, values))

    if first in {"gaṇavikalpaḥ", "ganavikalpah"} and len(tokens) >= 5:
        target = _identifier_from_token(tokens[1])
        type_name = _identifier_from_token(tokens[2])
        variant = TextLiteral(_identifier_from_token(tokens[3]))
        payload = _value_from_tokens(tokens[4:], known_modules=known_modules)
        if payload is not None:
            return ("phase3_bind", (target, "enum_new", type_name, None, (variant, payload)))

    if first in {"cihna-saṅghaṭaḥ", "cihna-sanghatah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        tag = _identifier_from_token(tokens[2])
        payload = _value_from_tokens(tokens[3:], known_modules=known_modules)
        if payload is not None:
            return ("phase3_bind", (target, "tagged_union_new", tag, payload))

    if first in {"lakṣita-doṣaḥ", "lakshita-doshah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        code = _identifier_from_token(tokens[2])
        message = _value_from_tokens(tokens[3:], known_modules=known_modules)
        if message is not None:
            return ("phase3_bind", (target, "typed_error_new", code, message))

    if first in {"sambandha-hastaḥ", "sambandha-hastah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        kind = _identifier_from_token(tokens[2])
        handle = _value_from_tokens(tokens[3:], known_modules=known_modules)
        if handle is not None:
            return ("phase3_bind", (target, "handle_new", kind, handle))

    if first in _TIER_MARKERS:
        return ("tier", _TIER_MARKERS[first])

    if first in {"khaṇḍaḥ", "khandah"}:
        return ("block", None)

    if first in {"niḥsāram", "nihsaram"} and len(tokens) >= 2:
        return ("export", _identifier_from_token(tokens[1]))

    if first == "punaranayanam" and len(tokens) >= 4:
        source_module = tokens[1]
        marker = "antaḥ" if "antaḥ" in tokens else "antah"
        if marker not in tokens:
            return None
        marker_idx = tokens.index(marker)
        symbol_name = _identifier_from_token(tokens[marker_idx + 1])
        export_name = symbol_name
        tail = tokens[marker_idx + 2 :]
        if "nāmnā" in tail or "namna" in tail:
            alias_marker = "nāmnā" if "nāmnā" in tail else "namna"
            alias_idx = tail.index(alias_marker)
            if alias_idx + 1 < len(tail):
                export_name = _identifier_from_token(tail[alias_idx + 1])
        return (
            "reexport",
            ReexportDef(name=export_name, source_module=source_module, source_symbol=symbol_name),
        )

    if first in {"ānayanam", "anayanam"} and len(tokens) >= 2:
        module_path = tokens[1]
        alias: str | None = None
        symbols: tuple[ImportSymbol, ...] = ()
        required_features: frozenset[str] = frozenset()
        if "viśeṣe" in tokens or "vishese" in tokens:
            feature_idx = tokens.index("viśeṣe") if "viśeṣe" in tokens else tokens.index("vishese")
            if feature_idx + 1 < len(tokens):
                required_features = frozenset({_identifier_from_token(tokens[feature_idx + 1])})
        if "antaḥ" in tokens or "antah" in tokens:
            marker = "antaḥ" if "antaḥ" in tokens else "antah"
            marker_idx = tokens.index(marker)
            symbol_tokens = tokens[marker_idx + 1 :]
            if not symbol_tokens:
                return None
            if "nāmnā" in symbol_tokens or "namna" in symbol_tokens:
                alias_marker = "nāmnā" if "nāmnā" in symbol_tokens else "namna"
                alias_idx = symbol_tokens.index(alias_marker)
                if alias_idx == 0 or alias_idx + 1 >= len(symbol_tokens):
                    return None
                symbols = (
                    ImportSymbol(
                        _identifier_from_token(symbol_tokens[0]),
                        _identifier_from_token(symbol_tokens[alias_idx + 1]),
                    ),
                )
            else:
                symbols = tuple(ImportSymbol(_identifier_from_token(name)) for name in symbol_tokens)
        elif "nāmnā" in tokens or "namna" in tokens:
            alias_marker = "nāmnā" if "nāmnā" in tokens else "namna"
            alias_idx = tokens.index(alias_marker)
            if alias_idx + 1 >= len(tokens):
                return None
            alias = _identifier_from_token(tokens[alias_idx + 1])
        return (
            "import",
            ImportDirective(
                module_path=module_path,
                alias=alias,
                symbols=symbols,
                required_features=required_features,
            ),
        )

    if first in {"acalachihnam", "acalachihna"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        value = _value_from_tokens(tokens[2:], known_modules=known_modules)
        if value is not None:
            return ("bind", (target, value, True))

    if first in {"ghoṣaṇam", "ghoshanam"} and len(tokens) >= 2:
        return ("forward", _identifier_from_token(tokens[1]))

    if first in {"tyāgaḥ", "tyagah"} and len(tokens) >= 2:
        value = _value_from_tokens(tokens[1:], known_modules=known_modules)
        if value is not None:
            return ("pop", value)

    if first in {"akṣarāṇi", "aksharani"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        data = parse_bytes_payload(tokens[2:])
        if data is not None:
            return ("bytes", (target, data))

    if first in {"akṣara-saṃgrahaḥ", "akshara-sangrahah"} and len(tokens) >= 2:
        target = _identifier_from_token(tokens[1])
        return ("phase3_bind", (target, "bytearray_new"))

    if first in {"samūhalakṣaṇaḥ", "samuhalakshanah"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        if _has_malformed_grouping(tokens[2:]):
            raise ParseError(
                f"Malformed grouping in list literal directive: {sentence!r}",
                hint="Balance each pariveṣṭanam with a matching antam.",
            )
        elements = _values_from_tokens(tokens[2:], known_modules=known_modules)
        return ("list_literal", (target, elements))

    if first in {"kośalakṣaṇaḥ", "kosalakshanah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        if _has_malformed_grouping(tokens[2:]):
            raise ParseError(
                f"Malformed grouping in map literal directive: {sentence!r}",
                hint="Balance each pariveṣṭanam with a matching antam.",
            )
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        if len(values) % 2 == 0:
            entries = tuple((values[i], values[i + 1]) for i in range(0, len(values), 2))
            return ("map_literal", (target, entries))

    if first in {"vastulakṣaṇaḥ", "vastulakshanah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        if _has_malformed_grouping(tokens[2:]):
            raise ParseError(
                f"Malformed grouping in record literal directive: {sentence!r}",
                hint="Balance each pariveṣṭanam with a matching antam.",
            )
        values = _values_from_tokens(tokens[2:], known_modules=known_modules)
        if len(values) % 2 == 0:
            fields: list[tuple[Value, Value]] = []
            for i in range(0, len(values), 2):
                field_key = _record_field_key_from_value(values[i])
                if field_key is None:
                    break
                fields.append((field_key, values[i + 1]))
            if len(fields) == len(values) // 2:
                return ("record_literal", (target, tuple(fields)))

    if first == "nityam" and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        value = _value_from_tokens(tokens[2:], known_modules=known_modules)
        if value is not None:
            return ("bind", (target, value, True))

    if first in {"gaṇitam", "ganitam"} and len(tokens) >= 3:
        idx = 1
        ownership: str | None = None
        lifetime: str | None = None
        if tokens[idx] in {"svāmitvaṃ", "svamitvam"}:
            ownership = "owned"
            idx += 1
        elif tokens[idx] in {"uddhāram", "uddharam"}:
            ownership = "borrow"
            idx += 1
        elif tokens[idx] in {"parivartanīya-uddhāram", "parivartaniayuddharam"}:
            ownership = "borrow_mut"
            idx += 1
        if idx < len(tokens) and tokens[idx] in {"āyuṣā", "ayusa"} and idx + 1 < len(tokens):
            lifetime = tokens[idx + 1]
            idx += 2
        target = _identifier_from_token(tokens[idx])
        value = _value_from_tokens(tokens[idx + 1 :], known_modules=known_modules)
        if value is not None:
            return ("bind_owned", (target, value, False, ownership, lifetime))

    if first in {"darśanam", "darshanam"} and len(tokens) >= 2:
        value = _value_from_tokens(tokens[1:])
        if value is not None:
            return ("display", value)

    if first in {"vākyasaṃyogaḥ", "vakyasamyogah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:])
        if len(values) == 2:
            return ("text_concat", (target, values[0], values[1]))

    if first in {"vākyaparimāṇam", "vakyaparimanam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        text = _value_from_tokens(tokens[2:])
        if text is not None:
            return ("text_len", (target, text))

    if first in {"vākyāharaṇam", "vakyaharanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        text = _value_from_tokens(tokens[2:3])
        index = _value_from_tokens(tokens[3:])
        if text is not None and index is not None:
            return ("text_get", (target, text, index))

    if first in {"vākyacchedaḥ", "vakyacchedah"} and len(tokens) >= 5:
        target = _identifier_from_token(tokens[1])
        text = _value_from_tokens(tokens[2:3])
        start = _value_from_tokens(tokens[3:4])
        end = _value_from_tokens(tokens[4:])
        if text is not None and start is not None and end is not None:
            return ("text_slice", (target, text, start, end))

    if first in {"vākyāsti", "vakyasti"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:])
        if len(values) == 2:
            return ("text_contains", (target, values[0], values[1]))

    if first in {"samūhaḥ", "samuhah"} and len(tokens) >= 2:
        return ("list_init", _identifier_from_token(tokens[1]))

    if first == "yojanam" and len(tokens) >= 3:
        container = _identifier_from_token(tokens[1])
        values = _values_from_tokens(tokens[2:])
        if values:
            return ("list_append", (container, values))

    if first in {"samūhāharaṇam", "samuhaharanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        index = _value_from_tokens(tokens[3:])
        if index is not None:
            return ("list_get", (target, container, index))

    if first in {"parimāṇam", "parimanam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        return ("list_len", (target, container))

    if first in {"māpanam", "mapanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        return ("list_map", (target, container, function_name))

    if first in {"śodhanam", "shodhanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        return ("list_filter", (target, container, function_name))

    if first in {"saṅkocanam", "sankocanam"} and len(tokens) >= 5:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        initial = _value_from_tokens(tokens[4:], known_modules=known_modules)
        if initial is not None:
            return ("list_reduce", (target, container, function_name, initial))

    if first in {"sarvam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        return ("list_all", (target, container, function_name))

    if first in {"avalokanam"} and len(tokens) >= 5:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        initial = _value_from_tokens(tokens[4:], known_modules=known_modules)
        if initial is not None:
            return ("list_scan", (target, container, function_name, initial))

    if first in {"yuktam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        left = _identifier_from_token(tokens[2])
        right = _identifier_from_token(tokens[3])
        return ("list_zip", (target, left, right))

    if first in {"aṅkayuktam", "ankayuktam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        return ("list_enumerate", (target, container))

    if first in {"kācit", "kacit"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        return ("list_any", (target, container, function_name))

    if first in {"nitya-samūhaḥ", "nitya-samuha", "nityasamuha"} and len(tokens) >= 2:
        return ("immutable_list_init", _identifier_from_token(tokens[1]))

    if first in {"nitye", "nitya"} and len(tokens) >= 5 and tokens[1] in {"yojanam"}:
        target = _identifier_from_token(tokens[2])
        container = _identifier_from_token(tokens[3])
        item = _value_from_tokens(tokens[4:], known_modules=known_modules)
        if item is not None:
            return ("immutable_list_append", (target, container, item))

    if first in {"samīkaraṇam", "samikaranam"} and len(tokens) >= 6:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        where_fn = _identifier_from_token(tokens[3])
        if tokens[4] in {"yathā", "yatha"}:
            with_fn = _identifier_from_token(tokens[5])
            if with_fn:
                return ("list_comprehension", (target, container, where_fn, with_fn))

    if first in {"alasaḥ", "alasah"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        return ("lazy_iter_new", (target, container))

    if first in {"alasāt", "alasat"} and len(tokens) >= 4:
        has_more = _identifier_from_token(tokens[1])
        value = _identifier_from_token(tokens[2])
        iterator = _identifier_from_token(tokens[3])
        return ("lazy_iter_next", (has_more, value, iterator))

    if first in {"utpādakaḥ", "utpadakah"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        function_name = _identifier_from_token(tokens[2])
        return ("generator_new", (target, function_name))

    if first in {"utpādakāt", "utpadakat"} and len(tokens) >= 4:
        has_more = _identifier_from_token(tokens[1])
        value = _identifier_from_token(tokens[2])
        generator = _identifier_from_token(tokens[3])
        return ("generator_next", (has_more, value, generator))

    if first in {"pradānam", "pradanam"} and len(tokens) >= 2:
        value = _value_from_tokens(tokens[1:], known_modules=known_modules)
        if value is not None:
            return ("yield", value)

    if first in {"pravāhaḥ", "pravahah"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        steps = tuple(_identifier_from_token(t) for t in tokens[3:] if _identifier_from_token(t))
        if steps:
            return ("pipeline_chain", (target, container, steps))

    if first in {"bandhanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        result = _identifier_from_token(tokens[2])
        function_name = _identifier_from_token(tokens[3])
        return ("result_bind", (target, result, function_name))

    if first in {"anveṣaṇam", "anvesanam"} and len(tokens) >= 5:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        field = tokens[3]
        predicate = _identifier_from_token(tokens[4])
        return ("data_query", (target, container, field, predicate))

    if first in {"kośaḥ", "kosah"} and len(tokens) >= 2:
        return ("map_init", _identifier_from_token(tokens[1]))

    if first in {"sthāpanam", "sthapanam"} and len(tokens) >= 4:
        container = _identifier_from_token(tokens[1])
        key = _map_key_from_tokens(tokens[2:3])
        value = _value_from_tokens(tokens[3:])
        if key is not None and value is not None:
            return ("map_put", (container, key, value))

    if first in {"āharaṇam", "aharanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        key = _map_key_from_tokens(tokens[3:])
        if key is not None:
            return ("map_get", (target, container, key))

    if first == "asti" and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        container = _identifier_from_token(tokens[2])
        key = _map_key_from_tokens(tokens[3:])
        if key is not None:
            return ("map_contains", (target, container, key))

    if first in {"vastuḥ", "vastuh"} and len(tokens) >= 2:
        return ("record_init", _identifier_from_token(tokens[1]))

    if first in {"aṅgasthāpanam", "angasthapanam"} and len(tokens) >= 4:
        record = _identifier_from_token(tokens[1])
        field = _map_key_from_tokens(tokens[2:3])
        value = _value_from_tokens(tokens[3:])
        if field is not None and value is not None:
            return ("field_set", (record, field, value))

    if first in {"aṅgāharaṇam", "angaharanam"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        record = _identifier_from_token(tokens[2])
        field = _map_key_from_tokens(tokens[3:])
        if field is not None:
            return ("field_get", (target, record, field))

    if first in {"aṅgāsti", "angasti"} and len(tokens) >= 4:
        target = _identifier_from_token(tokens[1])
        record = _identifier_from_token(tokens[2])
        field = _map_key_from_tokens(tokens[3:])
        if field is not None:
            return ("field_contains", (target, record, field))

    if (
        tokens[:3] == ["arakṣitaḥ", "adhikāraḥ", "ārabhyate"]
        or tokens[:3] == ["arakshitah", "adhikarah", "arabhyate"]
    ):
        proof: str | None = None
        if len(tokens) > 3:
            if tokens[3] not in {"pramāṇam", "pramanam"}:
                # Proof annotations must be explicit to avoid accidental typos
                # silently bypassing rakṣita unsafe-proof enforcement.
                proof = None
            else:
                parsed = _text_literal_from_tokens(tokens[4:])
                if isinstance(parsed, TextLiteral):
                    proof = parsed.value
                else:
                    proof = " ".join(tokens[4:]).strip() or None
        return ("unsafe_enter", proof)

    if tokens == ["arakṣitaḥ", "adhikāraḥ", "samāpyate"] or tokens == [
        "arakshitah",
        "adhikarah",
        "samapyate",
    ]:
        return ("unsafe_exit", None)

    if first in {"avakāśaḥ", "avakasah"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        size = _value_from_tokens(tokens[2:])
        if size is not None:
            return ("heap_alloc", (target, size))

    if first in {"smṛtisthāpanam", "smritisthapanam"} and len(tokens) >= 3:
        address = _value_from_tokens(tokens[1:2])
        value = _value_from_tokens(tokens[2:])
        if address is not None and value is not None:
            return ("heap_store", (address, value))

    if first in {"smṛtyāharaṇam", "smrtyaharanam", "smrityaharanam"} and len(tokens) >= 3:
        target = _identifier_from_token(tokens[1])
        address = _value_from_tokens(tokens[2:])
        if address is not None:
            return ("heap_load", (target, address))

    if first in {"smṛtimokṣaḥ", "smrtimoksah", "smritimoksah"} and len(tokens) >= 2:
        address = _value_from_tokens(tokens[1:])
        if address is not None:
            return ("heap_free", address)

    if first in {"vikṣepaḥ", "viksepah"} and len(tokens) >= 2:
        value = _text_literal_from_tokens(tokens[1:]) or _value_from_tokens(tokens[1:])
        if value is not None:
            return ("throw", value)

    if first in {"vipattim"} and len(tokens) >= 2:
        value = _text_literal_from_tokens(tokens[1:]) or _value_from_tokens(tokens[1:])
        if value is not None:
            return ("panic", value)

    if first in {"āgrahītvā", "agrahitva"} and len(tokens) >= 2:
        return ("try_catch", _identifier_from_token(tokens[1]))

    if first in {"pūrvaśartam", "purvasartam", "purvaśartam", "pūrvasartam"} and len(tokens) >= 2:
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("precondition", condition)

    if first in {"uttaraśartam", "uttarasartam"} and len(tokens) >= 2:
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("postcondition", condition)

    if first in {"nityaśartam", "nityasartam"} and len(tokens) >= 2:
        condition = _parse_condition_tokens(tokens[1:], known_modules=known_modules)
        if condition is not None:
            return ("invariant", condition)

    return None


def _collection_statement_from_directive(
    kind: str, payload: object
) -> tuple[Statement, ...] | None:
    if kind == "list_init":
        return (ListInit(str(payload)),)
    if kind == "map_init":
        return (MapInit(str(payload)),)
    if kind == "list_append":
        container, values = payload  # type: ignore[misc]
        return tuple(ListAppend(container, value) for value in values)
    if kind == "list_get":
        target, container, index = payload  # type: ignore[misc]
        return (ListGet(target, container, index),)
    if kind == "list_len":
        target, container = payload  # type: ignore[misc]
        return (ListLength(target, container),)
    if kind == "list_map":
        target, container, function_name = payload  # type: ignore[misc]
        return (ListMap(target, container, function_name),)
    if kind == "list_filter":
        target, container, function_name = payload  # type: ignore[misc]
        return (ListFilter(target, container, function_name),)
    if kind == "list_reduce":
        target, container, function_name, initial = payload  # type: ignore[misc]
        return (ListReduce(target, container, function_name, initial),)
    if kind == "list_all":
        target, container, function_name = payload  # type: ignore[misc]
        return (ListAll(target, container, function_name),)
    if kind == "list_scan":
        target, container, function_name, initial = payload  # type: ignore[misc]
        return (ListScan(target, container, function_name, initial),)
    if kind == "list_zip":
        target, left, right = payload  # type: ignore[misc]
        return (ListZip(target, left, right),)
    if kind == "list_enumerate":
        target, container = payload  # type: ignore[misc]
        return (ListEnumerate(target, container),)
    if kind == "list_any":
        target, container, function_name = payload  # type: ignore[misc]
        return (ListAny(target, container, function_name),)
    if kind == "immutable_list_init":
        return (ImmutableListInit(str(payload)),)
    if kind == "immutable_list_append":
        target, container, item = payload  # type: ignore[misc]
        return (ImmutableListAppend(target, container, item),)
    if kind == "list_comprehension":
        target, container, where_fn, with_fn = payload  # type: ignore[misc]
        return (ListComprehension(target, container, where_fn, with_fn),)
    if kind == "lazy_iter_new":
        target, container = payload  # type: ignore[misc]
        return (LazyIterNew(target, container),)
    if kind == "lazy_iter_next":
        has_more, value, iterator = payload  # type: ignore[misc]
        return (LazyIterNext(has_more, value, iterator),)
    if kind == "generator_new":
        target, function_name = payload  # type: ignore[misc]
        return (GeneratorNew(target, function_name),)
    if kind == "generator_next":
        has_more, value, generator = payload  # type: ignore[misc]
        return (GeneratorNext(has_more, value, generator),)
    if kind == "yield":
        return (Yield(payload),)  # type: ignore[arg-type]
    if kind == "pipeline_chain":
        target, container, steps = payload  # type: ignore[misc]
        return (PipelineChain(target, container, steps),)
    if kind == "result_bind":
        target, result, function_name = payload  # type: ignore[misc]
        return (ResultBind(target, result, function_name),)
    if kind == "data_query":
        target, container, field, predicate = payload  # type: ignore[misc]
        return (DataQuery(target, container, field, predicate),)
    if kind == "map_put":
        container, key, value = payload  # type: ignore[misc]
        return (MapPut(container, key, value),)
    if kind == "map_get":
        target, container, key = payload  # type: ignore[misc]
        return (MapGet(target, container, key),)
    if kind == "map_contains":
        target, container, key = payload  # type: ignore[misc]
        return (MapContains(target, container, key),)
    if kind == "record_init":
        return (RecordInit(str(payload)),)
    if kind == "field_set":
        record, field, value = payload  # type: ignore[misc]
        return (FieldSet(record, field, value),)
    if kind == "field_get":
        target, record, field = payload  # type: ignore[misc]
        return (FieldGet(target, record, field),)
    if kind == "field_contains":
        target, record, field = payload  # type: ignore[misc]
        return (FieldContains(target, record, field),)
    if kind == "unsafe_enter":
        return (UnsafeEnter(payload if isinstance(payload, str) else None),)
    if kind == "unsafe_exit":
        return (UnsafeExit(),)
    if kind == "heap_alloc":
        target, size = payload  # type: ignore[misc]
        return (HeapAlloc(target, size),)
    if kind == "heap_store":
        address, value = payload  # type: ignore[misc]
        return (HeapStore(address, value),)
    if kind == "heap_load":
        target, address = payload  # type: ignore[misc]
        return (HeapLoad(target, address),)
    if kind == "heap_free":
        return (HeapFree(payload),)  # type: ignore[arg-type]
    if kind == "text_concat":
        target, left, right = payload  # type: ignore[misc]
        return (TextConcat(target, left, right),)
    if kind == "text_len":
        target, text = payload  # type: ignore[misc]
        return (TextLength(target, text),)
    if kind == "text_get":
        target, text, index = payload  # type: ignore[misc]
        return (TextGet(target, text, index),)
    if kind == "text_slice":
        target, text, start, end = payload  # type: ignore[misc]
        return (TextSlice(target, text, start, end),)
    if kind == "text_contains":
        target, text, needle = payload  # type: ignore[misc]
        return (TextContains(target, text, needle),)
    return None


def _parse_condition_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> Condition | None:
    return parse_condition_tokens(
        tokens,
        value_parser=lambda part: _value_from_tokens(part, known_modules=known_modules),
    )


def _map_key_from_tokens(tokens: list[str]) -> Value | None:
    text = _text_literal_from_tokens(tokens)
    if text is not None:
        return text
    if len(tokens) != 1:
        return None
    token = tokens[0]
    if token in {"satyam", "asatyam"}:
        return BoolLiteral(token == "satyam")
    if re.fullmatch(r"\d+\.\d+", token):
        return FloatLiteral(float(token))
    facade = get_default_facade()
    try:
        analysis = facade.analyze_token(token)
    except Exception:
        return TextLiteral(token)
    if analysis.value is not None:
        return Literal(analysis.value)
    if analysis.pos == PartOfSpeech.NOUN:
        return TextLiteral(analysis.lemma)
    return TextLiteral(token)


def _value_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> Value | None:
    return parse_value_tokens(tokens, known_modules=known_modules)


def _binary_value_from_tokens(tokens: list[str]) -> BinaryValue | None:
    for index, token in enumerate(tokens):
        operator = _BINARY_VALUE_OPERATORS.get(token)
        if operator is None or index == 0 or index == len(tokens) - 1:
            continue
        left = _value_from_tokens(tokens[:index])
        right = _value_from_tokens(tokens[index + 1 :])
        if left is not None and right is not None:
            return BinaryValue(operator, left, right)
    return None


def _call_value_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> CallValue | None:
    if len(tokens) < 2 or tokens[0] not in {"āhvānam", "ahvanam"}:
        return None
    module_name, fn_name = _split_qualified_call_target(tokens[1], known_modules=known_modules)
    if module_name and len(tokens) >= 3 and not fn_name:
        args, kwargs = parse_call_arg_tokens(tokens[3:], known_modules=known_modules)
        return CallValue(tokens[2], module=module_name, args=args, kwargs=kwargs)
    args, kwargs = parse_call_arg_tokens(tokens[2:], known_modules=known_modules)
    return CallValue(fn_name, module=module_name, args=args, kwargs=kwargs)


def _split_qualified_call_target(
    token: str,
    *,
    known_modules: set[str] | frozenset[str],
) -> tuple[str | None, str]:
    if token in known_modules:
        return token, ""
    if "." not in token:
        return None, token
    parts = [part for part in token.split(".") if part]
    if len(parts) < 2:
        return None, token
    return ".".join(parts[:-1]), parts[-1]


def _parse_return_directive(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> Return | None:
    if len(tokens) == 1:
        return Return()
    rest = tokens[1:]
    if len(rest) >= 3 and rest[1] == "iti" and rest[2] in {"artha", "arthaṃ", "artham"}:
        name = _identifier_from_token(rest[0])
        value = _text_literal_from_tokens(rest[3:]) or _value_from_tokens(rest[3:], known_modules=known_modules)
        if value is not None:
            return Return(value, name=name)
    value = _text_literal_from_tokens(rest) or _value_from_tokens(rest, known_modules=known_modules)
    if value is None:
        return None
    return Return(value)


@dataclass(frozen=True)
class _ParsedFunctionHeader:
    name: str
    params: tuple[str, ...]
    param_defaults: tuple[Value | None, ...]
    variadic_param: str | None
    param_types: tuple[str | None, ...]
    effect: str | None
    decorators: tuple[str, ...]
    capture_mut: frozenset[str]
    is_inline: bool
    is_naked: bool
    is_compile_time: bool
    named_returns: tuple[str, ...]
    abi_name: str | None


def _parse_function_header_tokens(tokens: list[str]) -> _ParsedFunctionHeader | None:
    if len(tokens) < 2:
        return None
    idx = 1
    effect: str | None = None
    is_inline = False
    is_naked = False
    is_compile_time = False
    capture_mut: set[str] = set()
    named_returns: list[str] = []
    abi_name: str | None = None

    while idx < len(tokens):
        tok = tokens[idx]
        if tok in {"śuddhaḥ", "shuddhah"}:
            effect = "pure"
            idx += 1
            continue
        if tok in {"sādhanaṃ", "sadhanam"}:
            effect = "effectful"
            idx += 1
            continue
        if tok in {"antarbhūtam", "antarbhutam"}:
            is_inline = True
            idx += 1
            continue
        if tok in {"nagnā", "nagna", "nagnam"}:
            is_naked = True
            idx += 1
            continue
        if tok in {"kālavyāpāre", "kalavyapare"}:
            is_compile_time = True
            idx += 1
            continue
        if tok in {"parivartanīya-gṛhī", "parivartaniaygrahi", "parivartaniyagrihi"}:
            idx += 1
            capture_start = idx
            while idx < len(tokens) and tokens[idx] not in {
                "pratyāvartana-nāmāni",
                "pratyavartana-namani",
                "abi",
            }:
                idx += 1
            if idx == len(tokens):
                if idx == capture_start:
                    return None
                for capture in tokens[capture_start : idx - 1]:
                    capture_mut.add(_identifier_from_token(capture))
                idx -= 1
                break
            for capture in tokens[capture_start:idx]:
                capture_mut.add(_identifier_from_token(capture))
            continue
        if tok in {"pratyāvartana-nāmāni", "pratyavartana-namani"}:
            idx += 1
            while idx < len(tokens) and tokens[idx] != "abi":
                named_returns.append(_identifier_from_token(tokens[idx]))
                idx += 1
            continue
        if tok == "abi":
            if idx + 1 < len(tokens):
                abi_name = tokens[idx + 1]
                idx += 2
            continue
        break

    name = _identifier_from_token(tokens[idx])
    raw_params = tokens[idx + 1 :]
    params, param_defaults, variadic_param, param_types = _parse_function_params(raw_params)
    return _ParsedFunctionHeader(
        name=name,
        params=params,
        param_defaults=param_defaults,
        variadic_param=variadic_param,
        param_types=param_types,
        effect=effect,
        decorators=(),
        capture_mut=frozenset(capture_mut),
        is_inline=is_inline,
        is_naked=is_naked,
        is_compile_time=is_compile_time,
        named_returns=tuple(named_returns),
        abi_name=abi_name,
    )


def _text_literal_from_tokens(tokens: list[str]) -> TextLiteral | None:
    if len(tokens) >= 3 and tokens[0] in _TEXT_MARKERS and tokens[-1] == "iti":
        words = tokens[1:-1]
        if words:
            return TextLiteral(" ".join(words))
    return None


def _parse_text_sentence(sentence: str) -> Statement | None:
    tokens = _directive_tokens(sentence)
    if len(tokens) < 4 or tokens[0] not in _TEXT_MARKERS or "iti" not in tokens:
        return None
    split_at = tokens.index("iti")
    words = tokens[1:split_at]
    tail = tokens[split_at + 1 :]
    if not words or not tail:
        return None
    value = TextLiteral(" ".join(words))
    if len(tail) == 1 and tail[0] in _DISPLAY_VERBS:
        return Display(value)
    if len(tail) == 2 and tail[1] in _ASSIGN_VERBS:
        return Assign(_identifier_from_token(tail[0]), value)
    return None


def _values_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[Value, ...]:
    values: list[Value] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in {"pariveṣṭanam", "parivestanam"}:
            end = _find_group_token_end(tokens, index)
            if end is None:
                index += 1
                continue
            grouped = parse_value_tokens(tokens[index : end + 1], known_modules=known_modules)
            if grouped is not None:
                values.append(grouped)
                index = end + 1
                continue
        if token in _TEXT_MARKERS and "iti" in tokens[index + 1 :]:
            end = tokens.index("iti", index + 1)
            text = _text_literal_from_tokens(tokens[index : end + 1])
            if text is not None:
                values.append(text)
                index = end + 1
                continue
        chunk_end = index + 1
        while chunk_end < len(tokens):
            if (
                tokens[chunk_end] in _TEXT_MARKERS
                and "iti" in tokens[chunk_end + 1 :]
            ):
                break
            trial = parse_value_tokens(tokens[index:chunk_end], known_modules=known_modules)
            if trial is not None:
                chunk_end += 1
            else:
                break
        if chunk_end > index + 1:
            chunk_end -= 1
        value = parse_value_tokens(tokens[index:chunk_end], known_modules=known_modules)
        if value is not None:
            values.append(value)
            index = chunk_end
        else:
            index += 1
    return tuple(values)


def _find_group_token_end(tokens: list[str], start: int) -> int | None:
    if start >= len(tokens) or tokens[start] not in {"pariveṣṭanam", "parivestanam"}:
        return None
    depth = 0
    in_text = False
    for index in range(start, len(tokens)):
        token = tokens[index]
        if token in _TEXT_MARKERS:
            in_text = True
            continue
        if token == "iti":
            in_text = False
            continue
        if in_text:
            continue
        if token in {"pariveṣṭanam", "parivestanam"}:
            depth += 1
            continue
        if token == "antam":
            depth -= 1
            if depth == 0:
                return index
            if depth < 0:
                return None
    return None


def _has_malformed_grouping(tokens: list[str]) -> bool:
    depth = 0
    in_text = False
    for token in tokens:
        if token in _TEXT_MARKERS:
            in_text = True
            continue
        if token == "iti":
            in_text = False
            continue
        if in_text:
            continue
        if token in {"pariveṣṭanam", "parivestanam"}:
            depth += 1
            continue
        if token == "antam":
            depth -= 1
            if depth < 0:
                return True
    return depth != 0


def _record_field_key_from_value(value: Value) -> Value | None:
    if isinstance(value, GroupValue):
        return _record_field_key_from_value(value.inner)
    if isinstance(value, Reference):
        return TextLiteral(value.name)
    if isinstance(value, (TextLiteral, Literal, BoolLiteral, FloatLiteral)):
        return value
    return None


def _identifier_from_token(token: str) -> str:
    try:
        return canonical_identifier(token, facade=get_default_facade())
    except IdentifierError as exc:
        raise ParseError(
            f"Invalid identifier {token!r}: {exc}",
            hint="Use a grammatical Sanskrit noun/compound, or a simple technical name made from letters, digits, '_', '-', or '.'.",
        ) from exc


def _collect_match_arms(
    sentences: list[str],
    index: int,
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[tuple[MatchArm, ...], int]:
    arms: list[MatchArm] = []
    while index < len(sentences):
        sentence = sentences[index].strip()
        if _is_marker_sentence(sentence, {"antam", "anta"}):
            return tuple(arms), index + 1
        tokens = _directive_tokens(sentence)
        if tokens and tokens[0] in {"yathā", "yatha"}:
            pattern = _pattern_from_tokens(tokens[1:], known_modules=known_modules)
            if pattern is None:
                break
            index += 1
            body, index = _collect_until(
                sentences,
                index,
                end_markers={"yathā", "yatha", "antam", "anta"},
                stop_before_markers=True,
                known_modules=known_modules,
            )
            arms.append(MatchArm(pattern, body))
            continue
        break
    return tuple(arms), index


def _pattern_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
):
    if not tokens:
        return None
    if tokens[0] in {"kevalam", "_", "anyat"}:
        return PatternWildcard()
    value = _value_from_tokens(tokens, known_modules=known_modules)
    if value is not None:
        return PatternLiteral(value)
    return PatternWildcard()


def _collect_until(
    sentences: list[str],
    index: int,
    *,
    end_markers: set[str],
    stop_before_markers: bool = False,
    known_modules: set[str] | frozenset[str] = frozenset(),
    facade=None,
    source_text: str | None = None,
) -> tuple[tuple[Statement, ...], int]:
    body: list[Statement] = []
    while index < len(sentences):
        sentence = sentences[index].strip()
        if not sentence:
            index += 1
            continue
        if _is_marker_sentence(sentence, end_markers):
            if stop_before_markers:
                return tuple(body), index
            index += 1
            if not stop_before_markers:
                return tuple(body), index
            continue
        text_statement = _parse_text_sentence(sentence)
        if text_statement is not None:
            body.append(text_statement)
            index += 1
            continue
        header = _parse_directive_header(sentence, known_modules=known_modules)
        if header is not None:
            kind, payload = header
            collection_stmt = _collection_statement_from_directive(kind, payload)
            if collection_stmt is not None:
                body.extend(collection_stmt)
                index += 1
                continue
            if kind == "call":
                if len(payload) == 4:  # type: ignore[arg-type]
                    module_name, fn_name, args, kwargs = payload
                    body.append(Call(fn_name, module=module_name, args=args, kwargs=kwargs))
                else:
                    module_name, fn_name, args = payload  # type: ignore[misc]
                    body.append(Call(fn_name, module=module_name, args=args))
                index += 1
                continue
            if kind == "bind":
                target, value, immutable = payload  # type: ignore[misc]
                body.append(Bind(target, value, immutable=immutable))
                index += 1
                continue
            if kind == "bind_owned":
                target, value, immutable, ownership, lifetime = payload  # type: ignore[misc]
                body.append(
                    Bind(
                        target,
                        value,
                        immutable=immutable,
                        ownership=ownership,
                        lifetime=lifetime,
                    )
                )
                index += 1
                continue
            if kind == "assign":
                target, value = payload
                body.append(Assign(target, value))
                index += 1
                continue
            if kind == "bytes":
                target, data = payload  # type: ignore[misc]
                body.append(Bind(target, BytesLiteral(data), immutable=True))
                index += 1
                continue
            if kind == "list_literal":
                target, elements = payload  # type: ignore[misc]
                body.append(Bind(target, ListLiteral(elements)))
                index += 1
                continue
            if kind == "map_literal":
                target, entries = payload  # type: ignore[misc]
                body.append(Bind(target, MapLiteral(entries)))
                index += 1
                continue
            if kind == "record_literal":
                target, fields = payload  # type: ignore[misc]
                body.append(RecordInit(target))
                for field_key, field_val in fields:
                    body.append(FieldSet(target, field_key, field_val))
                index += 1
                continue
            if kind == "pop":
                body.append(Pop(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "display":
                body.append(Display(payload))
                index += 1
                continue
            if kind == "return":
                body.append(payload)  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "if":
                condition = payload
                index += 1
                then_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"anyathā", "anyatha", "antam", "anta"},
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source_text,
                )
                else_body: tuple[Statement, ...] = ()
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"anyathā", "anyatha"}):
                    index += 1
                    else_body, index = _collect_until(
                        sentences,
                        index,
                        end_markers=_BLOCK_END_MARKERS,
                        stop_before_markers=True,
                        known_modules=known_modules,
                        facade=facade,
                        source_text=source_text,
                    )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(If(condition, then_body, else_body))
                continue
            if kind == "while":
                condition = payload
                index += 1
                loop_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source_text,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(While(condition, loop_body))
                continue
            if kind == "throw":
                body.append(Throw(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "panic":
                body.append(Panic(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "precondition":
                body.append(PreCondition(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "postcondition":
                body.append(PostCondition(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "invariant":
                body.append(Invariant(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "try_catch":
                error_name = str(payload)
                index += 1
                tc_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"anyathā", "anyatha", "antam", "anta"},
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source_text,
                )
                tc_handler: tuple[Statement, ...] = ()
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"anyathā", "anyatha"}):
                    index += 1
                    tc_handler, index = _collect_until(
                        sentences,
                        index,
                        end_markers={"antam", "anta"},
                        stop_before_markers=True,
                        known_modules=known_modules,
                        facade=facade,
                        source_text=source_text,
                    )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(TryCatch(tc_body, error_name, tc_handler))
                continue
            if kind == "foreach_destructure":
                names, container = payload  # type: ignore[misc]
                index += 1
                loop_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source_text,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(ForEachDestructure(names, container, loop_body))
                continue
            if kind == "foreach":
                item, container = payload  # type: ignore[misc]
                index += 1
                loop_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                    facade=facade,
                    source_text=source_text,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(ForEach(item, container, loop_body))
                continue
            if kind == "class_new":
                target, class_name, args = payload  # type: ignore[misc]
                body.append(ClassNew(target, class_name, args))
                index += 1
                continue
            if kind == "method_call":
                target, receiver, method, args = payload  # type: ignore[misc]
                body.append(MethodCall(target, receiver, method, args))
                index += 1
                continue
            if kind == "static_method_call":
                target, class_name, method, args = payload  # type: ignore[misc]
                body.append(StaticMethodCall(target, class_name, method, args))
                index += 1
                continue
            if kind == "class_method_call":
                target, class_name, method, args = payload  # type: ignore[misc]
                body.append(ClassMethodCall(target, class_name, method, args))
                index += 1
                continue
            if kind == "property_get":
                target, receiver, prop = payload  # type: ignore[misc]
                body.append(PropertyGet(target, receiver, prop))
                index += 1
                continue
            if kind == "instance_finalize":
                body.append(InstanceFinalize(payload))  # type: ignore[arg-type]
                index += 1
                continue
            if kind == "class_reflect":
                target, receiver = payload  # type: ignore[misc]
                body.append(ClassReflect(target, receiver))
                index += 1
                continue
            if kind == "method_reflect":
                target, receiver, method = payload  # type: ignore[misc]
                body.append(MethodReflect(target, receiver, method))
                index += 1
                continue
            return tuple(body), index
        _raise_if_malformed_phase5_directive(
            sentence,
            source=source_text or sentence,
            sentence_start=0,
        )
        body.append(parse_sentence(sentence, facade=facade, source_text=source_text))
        index += 1
    return tuple(body), index


def _raise_if_malformed_phase5_directive(
    sentence: str,
    *,
    source: str,
    sentence_start: int,
) -> None:
    tokens = _directive_tokens(sentence)
    if not tokens:
        return
    directive = _PHASE5_DIRECTIVE_PREFIXES.get(tokens[0])
    if directive is None:
        return
    span = span_at(source, sentence_start, sentence_start + len(sentence))
    raise ParseError(
        f"Malformed {directive} directive: {sentence!r}",
        hint="Check directive syntax and required operands before the sentence terminator.",
        span=span,
        original_script=_script_label(source),
    )


def _is_marker_sentence(sentence: str, markers: set[str]) -> bool:
    tokens = _directive_tokens(sentence)
    return bool(tokens) and tokens[0] in markers


def _directive_tokens(sentence: str) -> list[str]:
    tokens: list[str] = []
    for token in re.split(r"[\s,;]+", sentence):
        if not token:
            continue
        if re.match(r"^(\.\./|\./|@)", token):
            cleaned = token.strip(";:!?।")
        else:
            cleaned = token.strip(".,;:!?।")
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _roles_by_type(items: Iterable[Analysis]) -> dict[Role, list[Analysis]]:
    roles: dict[Role, list[Analysis]] = {}
    for item in items:
        if item.role is None:
            continue
        roles.setdefault(item.role, []).append(item)
    return roles


def _single(roles: dict[Role, list[Analysis]], role: Role) -> Analysis:
    matches = roles.get(role, [])
    if len(matches) != 1:
        raise ParseError(
            f"Expected exactly one {role.value} participant, found {len(matches)}",
            hint="Check that the participant has the vibhakti required by the verb frame.",
        )
    return matches[0]


def _frame_role(frame: VerbFrame, attribute: str) -> Role:
    role = getattr(frame, attribute)
    if role is None:
        raise ParseError(f"Verb frame {frame.surface!r} is missing {attribute}")
    return role


def _validate_verb_analysis(verb: Analysis, frame: VerbFrame) -> None:
    mismatches: list[str] = []
    for field in ("lemma", "person", "number", "lakara", "pada"):
        expected = getattr(frame, field)
        actual = getattr(verb, field)
        if actual != expected:
            expected_text = expected.value if hasattr(expected, "value") else expected
            actual_text = actual.value if hasattr(actual, "value") else actual
            mismatches.append(f"{field}={actual_text!r}, expected {expected_text!r}")
    if mismatches:
        raise ParseError(f"{verb.surface!r} does not match its verb frame: {', '.join(mismatches)}")


_CLASS_SECTION_MARKERS = frozenset(
    {
        "metoda",
        "śailī",
        "shaili",
        "sthira",
        "varga-metoda",
        "vargametoda",
        "guṇa",
        "guna",
        "abhāvya",
        "abhavya",
        "mudrita",
        "miśra",
        "misra",
        "sādhayati",
        "sadhayati",
        "adhivarga",
        "adhi-varga",
        "saha",
        "paribaddha",
    }
)

_VISIBILITY_PREFIXES = {
    "gopita": "private",
    "gopitam": "private",
    "rakṣita": "protected",
    "rakshita": "protected",
    "prakāśya": "public",
    "prakashya": "public",
}


def _parse_class_decl(tokens: list[str]) -> ClassDecl | None:
    """Parse vargaḥ declaration with inheritance, visibility, and method sections."""

    name = tokens[1]
    idx = 2
    base_class: str | None = None
    if idx < len(tokens) and tokens[idx] in {"uttarāt", "uttarat", "uttarad"}:
        if idx + 1 >= len(tokens):
            return None
        base_class = tokens[idx + 1]
        idx += 2

    type_param: str | None = None
    if idx < len(tokens) and len(tokens[idx]) == 1 and tokens[idx].isalpha():
        peek = tokens[idx + 1] if idx + 1 < len(tokens) else ""
        if peek in _CLASS_SECTION_MARKERS or peek in _VISIBILITY_PREFIXES or peek in _BUILTIN_TYPE_HINTS:
            type_param = tokens[idx]
            idx += 1
        elif idx + 2 < len(tokens) and tokens[idx + 2] in _BUILTIN_TYPE_HINTS:
            type_param = tokens[idx]
            idx += 1

    trait_bounds: list[tuple[str, str]] = []
    if type_param and idx < len(tokens) and tokens[idx] in {"paribaddha", "paribaddhah"}:
        if idx + 1 < len(tokens):
            trait_bounds.append((type_param, tokens[idx + 1]))
            idx += 2

    fields, field_visibility, consumed = _parse_class_fields(tokens[idx:])
    idx += consumed
    methods: list[str] = []
    static_methods: list[str] = []
    class_methods: list[str] = []
    computed: list[str] = []
    mixins: list[str] = []
    trait_impls: list[str] = []
    composition: list[str] = []
    metaclass: str | None = None
    abstract = False
    sealed = False

    while idx < len(tokens):
        marker = tokens[idx]
        if marker in {"metoda", "śailī", "shaili"}:
            idx += 1
            while idx < len(tokens) and tokens[idx] not in _CLASS_SECTION_MARKERS:
                methods.append(_identifier_from_token(tokens[idx]))
                idx += 1
            continue
        if marker == "sthira":
            idx += 1
            if idx < len(tokens) and tokens[idx] in {"metoda", "śailī", "shaili"}:
                idx += 1
            while idx < len(tokens) and tokens[idx] not in _CLASS_SECTION_MARKERS:
                static_methods.append(_identifier_from_token(tokens[idx]))
                idx += 1
            continue
        if marker in {"varga-metoda", "vargametoda"}:
            idx += 1
            while idx < len(tokens) and tokens[idx] not in _CLASS_SECTION_MARKERS:
                class_methods.append(_identifier_from_token(tokens[idx]))
                idx += 1
            continue
        if marker in {"guṇa", "guna"}:
            idx += 1
            while idx < len(tokens) and tokens[idx] not in _CLASS_SECTION_MARKERS:
                computed.append(_identifier_from_token(tokens[idx]))
                idx += 1
            continue
        if marker in {"abhāvya", "abhavya"}:
            abstract = True
            idx += 1
            continue
        if marker == "mudrita":
            sealed = True
            idx += 1
            continue
        if marker in {"miśra", "misra"}:
            idx += 1
            while idx < len(tokens) and tokens[idx] not in _CLASS_SECTION_MARKERS:
                mixins.append(tokens[idx])
                idx += 1
            continue
        if marker in {"sādhayati", "sadhayati"}:
            if idx + 1 < len(tokens):
                trait_impls.append(tokens[idx + 1])
                idx += 2
            continue
        if marker in {"adhivarga", "adhi-varga"}:
            if idx + 1 < len(tokens):
                metaclass = tokens[idx + 1]
                idx += 2
            continue
        if marker == "saha":
            if idx + 2 < len(tokens):
                composition.append(tokens[idx + 2])
                idx += 3
            continue
        break

    if not fields and not methods and not static_methods and not class_methods:
        return None
    return ClassDecl(
        name,
        type_param,
        fields,
        tuple(methods),
        tuple(field_visibility),
        tuple(static_methods),
        tuple(class_methods),
        base_class,
        tuple(mixins),
        tuple(trait_impls),
        tuple(trait_bounds),
        abstract,
        sealed,
        tuple(computed),
        metaclass,
        tuple(composition),
    )


def _parse_class_fields(
    tokens: list[str],
) -> tuple[tuple[tuple[str, str], ...], tuple[tuple[str, str], ...], int]:
    fields: list[tuple[str, str]] = []
    visibility: list[tuple[str, str]] = []
    idx = 0
    vis = "public"
    while idx < len(tokens):
        if tokens[idx] in _CLASS_SECTION_MARKERS:
            break
        if tokens[idx] in _VISIBILITY_PREFIXES:
            vis = _VISIBILITY_PREFIXES[tokens[idx]]
            idx += 1
            continue
        if idx + 1 >= len(tokens):
            break
        if tokens[idx + 1] not in _BUILTIN_TYPE_HINTS and tokens[idx + 1] not in _VISIBILITY_PREFIXES:
            if tokens[idx + 1] in _CLASS_SECTION_MARKERS:
                break
        field_name = _identifier_from_token(tokens[idx])
        field_type = tokens[idx + 1]
        fields.append((field_name, field_type))
        if vis != "public":
            visibility.append((field_name, vis))
        idx += 2
        vis = "public"
    return tuple(fields), tuple(visibility), idx


def _parse_type_field_pairs(tokens: list[str]) -> tuple[tuple[str, str], ...]:
    """Parse alternating field_name type_name tokens."""
    if len(tokens) < 2 or len(tokens) % 2 != 0:
        return ()
    return tuple((tokens[i], tokens[i + 1]) for i in range(0, len(tokens), 2))


def _parse_trait_methods(
    tokens: list[str],
) -> tuple[tuple[str, tuple[str, ...], str | None], ...]:
    """Parse method_name [param_types...] return_type triples from token tail."""
    methods: list[tuple[str, tuple[str, ...], str | None]] = []
    idx = 0
    while idx < len(tokens):
        method_name = _identifier_from_token(tokens[idx])
        idx += 1
        params: list[str] = []
        while idx < len(tokens) and tokens[idx] not in _BUILTIN_TYPE_HINTS:
            if tokens[idx] == "→" or tokens[idx] in {"->", "iti"}:
                idx += 1
                continue
            if idx + 1 < len(tokens) and tokens[idx + 1] in {"→", "->"}:
                break
            params.append(tokens[idx])
            idx += 1
        return_type = tokens[idx] if idx < len(tokens) else None
        if return_type in {"→", "->"}:
            return_type = tokens[idx + 1] if idx + 1 < len(tokens) else None
            idx += 2
        elif return_type:
            idx += 1
        methods.append((method_name, tuple(params), return_type))
    return tuple(methods)


_BUILTIN_TYPE_HINTS = frozenset(
    {
        "i32",
        "i64",
        "u32",
        "f64",
        "f32",
        "text",
        "bool",
        "bytes",
        "void",
        "list",
        "hash_map",
    }
)


def _parse_function_params(
    tokens: list[str],
) -> tuple[tuple[str, ...], tuple[Value | None, ...], str | None, tuple[str | None, ...]]:
    """Parse params with optional defaults, type hints, and trailing variadic (...name)."""
    if not tokens:
        return (), (), None, ()
    params: list[str] = []
    defaults: list[Value | None] = []
    param_types: list[str | None] = []
    variadic_param: str | None = None
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith("..."):
            variadic_param = _identifier_from_token(tok[3:])
            i += 1
            continue
        if tok.startswith("("):
            # collect tokens until )
            group = [tok]
            while i < len(tokens) - 1 and ")" not in tok:
                i += 1
                tok = tokens[i]
                group.append(tok)
            joined = " ".join(group).strip("()")
            names = [_identifier_from_token(n.strip()) for n in re.split(r"[\s,]+", joined) if n.strip()]
            # encode as __destruct__name1__name2
            params.append("__destruct__" + "__".join(names))
            defaults.append(None)
            param_types.append(None)
        else:
            param_type: str | None = None
            if "=" in tok:
                raw_name, _, raw_default = tok.partition("=")
                name = _identifier_from_token(raw_name)
                default = _value_from_tokens([raw_default])
            else:
                name = _identifier_from_token(tok)
                default = None
                if i + 1 < len(tokens) and tokens[i + 1] in _BUILTIN_TYPE_HINTS:
                    param_type = tokens[i + 1]
                    i += 1
            params.append(name)
            defaults.append(default)
            param_types.append(param_type)
        i += 1
    return tuple(params), tuple(defaults), variadic_param, tuple(param_types)


def _default_import_name(module_path: str) -> str:
    cleaned = module_path.replace("\\", "/").rstrip("/")
    if "/" in cleaned:
        cleaned = cleaned.rsplit("/", 1)[-1]
    if "." in cleaned:
        cleaned = cleaned.rsplit(".", 1)[-1]
    return cleaned


def _value_from(item: Analysis) -> Value:
    if item.value is not None:
        return Literal(item.value)
    return Reference(item.lemma)
