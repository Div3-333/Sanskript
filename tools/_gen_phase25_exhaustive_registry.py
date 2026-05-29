"""One-shot generator for phase25_exhaustive_registry AST builders (dev tooling)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from tools.phase0_common import ast_statement_nodes  # noqa: E402

# fmt: off
BUILDERS = {
    "AlgebraicTypeDecl": "Program((), algebraic_types=(AlgebraicTypeDecl('Opt', ('Some', 'None')),))",
    "Assert": "Program((Assert(Literal(1)),))",
    "Assign": "Program((Assign('x', Literal(1)),))",
    "Bind": "Program((Bind('x', Literal(1)),))",
    "Block": "Program((Block(_BODY),))",
    "Break": "Program((While(_COND, (Break(),)),))",
    "Call": "Program((Call('f'),), functions=_FN)",
    "ClassMethodCall": "Program((ClassNew('obj', 'C'), ClassMethodCall('out', 'C', 'm')), classes=_CLS, functions=_FN_OOP)",
    "ClassNew": "Program((ClassNew('obj', 'C'),), classes=_CLS)",
    "ClassReflect": "Program((ClassReflect('out', 'C'),), classes=_CLS)",
    "ConstDecl": "Program((ConstDecl('K', Literal(1)),))",
    "Continue": "Program((While(_COND, (Continue(),)),))",
    "CountedFor": "Program((CountedFor('i', Literal(0), Literal(1), (Display(Reference('i')),))),)",
    "DataQuery": "Program((ListInit('rows'), DataQuery('hits', 'rows', 'score', 'gt4')), functions=_FN)",
    "Decrease": "Program((Assign('x', Literal(2)), Decrease('x', Literal(1)), Display(Reference('x'))))",
    "Defer": "Program((Defer((Display(Literal(1)),)), Display(Literal(2))))",
    "DestructureAssign": "Program((DestructureAssign(('a', 'b'), TupleLiteral((Literal(1), Literal(2)))),))",
    "Display": "Program((Display(Literal(1)),))",
    "FieldContains": "Program((RecordInit('r', ('k',)), FieldContains('out', 'r', 'k')))",
    "FieldGet": "Program((RecordInit('r', ('k',)), FieldSet('r', 'k', Literal(1)), FieldGet('out', 'r', 'k')))",
    "FieldSet": "Program((RecordInit('r', ('k',)), FieldSet('r', 'k', Literal(1))))",
    "ForEach": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ForEach('v', 'xs', (Display(Reference('v')),))))",
    "ForEachDestructure": "Program((ListInit('xs'), ListAppend('xs', TupleLiteral((Literal(1), Literal(2)))), ForEachDestructure(('a', 'b'), 'xs', (Display(Reference('a')),))))",
    "ForwardDecl": "Program((ForwardDecl('x'), Assign('x', Literal(1))))",
    "FunctionDef": "Program((), functions=(FunctionDef('f', (Return(Literal(1)),)),))",
    "GeneratorNew": "Program((GeneratorNew('g', 'gen'),), functions=_GEN_FN)",
    "GeneratorNext": "Program((GeneratorNew('g', 'gen'), GeneratorNext('out', 'g')), functions=_GEN_FN)",
    "GenericRecordDecl": "Program((), generic_records=(GenericRecordDecl('Box', ('T',), ('value',)),))",
    "Guard": "Program((Guard(_COND, (Display(Literal(1)),))))",
    "HeapAlloc": "Program((HeapAlloc('addr', Literal(4)),), safety_tier='arakshita')",
    "HeapFree": "Program((HeapAlloc('addr', Literal(4)), HeapFree('addr')), safety_tier='arakshita')",
    "HeapLoad": "Program((HeapAlloc('addr', Literal(4)), HeapStore('addr', Literal(9)), HeapLoad('out', 'addr')), safety_tier='arakshita')",
    "HeapStore": "Program((HeapAlloc('addr', Literal(4)), HeapStore('addr', Literal(9))), safety_tier='arakshita')",
    "If": "Program((If(_COND, (Display(Literal(1)),), (Display(Literal(0)),))))",
    "ImmutableListAppend": "Program((ImmutableListInit('xs'), ImmutableListAppend('xs', Literal(1))))",
    "ImmutableListInit": "Program((ImmutableListInit('xs'),))",
    "Increase": "Program((Assign('x', Literal(1)), Increase('x', Literal(2)), Display(Reference('x'))))",
    "InfiniteLoop": "Program((InfiniteLoop((Break(),)),))",
    "InstanceFinalize": "Program((ClassNew('obj', 'C'), InstanceFinalize('obj')), classes=_CLS, functions=_FN_OOP)",
    "Invariant": "Program((Invariant(_COND),))",
    "LazyIterNew": "Program((LazyIterNew('it', 'xs'), ListInit('xs'), ListAppend('xs', Literal(1))))",
    "LazyIterNext": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), LazyIterNew('it', 'xs'), LazyIterNext('out', 'it')))",
    "ListAll": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListAll('out', 'xs', 'is_one')), functions=_FN)",
    "ListAny": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListAny('out', 'xs', 'is_one')), functions=_FN)",
    "ListAppend": "Program((ListInit('xs'), ListAppend('xs', Literal(1))))",
    "ListComprehension": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListComprehension('out', 'xs', 'double')), functions=_FN)",
    "ListEnumerate": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListEnumerate('out', 'xs')))",
    "ListFilter": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListFilter('out', 'xs', 'is_one')), functions=_FN)",
    "ListGet": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListGet('out', 'xs', Literal(0))))",
    "ListInit": "Program((ListInit('xs'),))",
    "ListLength": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListLength('out', 'xs')))",
    "ListMap": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListMap('out', 'xs', 'double')), functions=_FN)",
    "ListReduce": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListReduce('out', 'xs', 'add_pair', Literal(0))), functions=_FN)",
    "ListScan": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListScan('out', 'xs', 'add_pair', Literal(0))), functions=_FN)",
    "ListZip": "Program((ListInit('a'), ListInit('b'), ListAppend('a', Literal(1)), ListAppend('b', Literal(2)), ListZip('out', 'a', 'b')))",
    "MapContains": "Program((MapInit('m'), MapPut('m', Literal(1), Literal(2)), MapContains('out', 'm', Literal(1))))",
    "MapGet": "Program((MapInit('m'), MapPut('m', Literal(1), Literal(2)), MapGet('out', 'm', Literal(1))))",
    "MapInit": "Program((MapInit('m'),))",
    "MapPut": "Program((MapInit('m'), MapPut('m', Literal(1), Literal(2))))",
    "Match": "Program((Match(Literal(1), (MatchArm(PatternLiteral(Literal(1)), (Display(Literal(1)),)),))))",
    "MatchExpr": "Program((MatchExpr('out', Literal(1), (MatchArm(PatternLiteral(Literal(1)), (Assign('out', Literal(1)),)),))))",
    "MemoFunction": "Program((), functions=(MemoFunction(FunctionDef('mf', (Return(Literal(1)),))),))",
    "MethodCall": "Program((ClassNew('obj', 'C'), MethodCall('out', 'obj', 'm')), classes=_CLS, functions=_FN_OOP)",
    "MethodReflect": "Program((MethodReflect('out', 'C', 'm'),), classes=_CLS)",
    "Multiply": "Program((Assign('x', Literal(2)), Multiply('x', Literal(3)), Display(Reference('x'))))",
    "NewtypeDecl": "Program((), newtypes=(NewtypeDecl('UserId', 'i32'),))",
    "Panic": "Program((Panic('boom'),))",
    "Phase3Bind": "Program((Phase3Bind('x', 'i32', Literal(1)),))",
    "PipelineChain": "Program((ListInit('xs'), ListAppend('xs', Literal(1)), PipelineChain('out', 'xs', ('double',))), functions=_FN)",
    "Pop": "Program((Pop(Literal(1)),))",
    "PostCondition": "Program((PostCondition(_COND),))",
    "PreCondition": "Program((PreCondition(_COND),))",
    "Propagate": "Program((Propagate('err'),))",
    "PropertyGet": "Program((ClassNew('obj', 'C'), PropertyGet('out', 'obj', 'p')), classes=_CLS, functions=_FN_OOP)",
    "RecordInit": "Program((RecordInit('r', ('k',)),))",
    "RecordTypeDecl": "Program((), record_types=(RecordTypeDecl('Point', (('x', 'i32'), ('y', 'i32'))),))",
    "ResultBind": "Program((Assign('r', Literal(1)), ResultBind('out', 'r', 'wrap')), functions=_FN)",
    "Return": "Program((), functions=(FunctionDef('f', (Return(Literal(1)),)),))",
    "RuleDecl": "Program((), functions=(FunctionDef('when_true', (Return(Literal(1)),), params=('ctx',)), FunctionDef('then_same', (Return(Literal(1)),), params=('ctx',))), rules=(RuleDecl('r', 'when_true', 'then_same'),))",
    "RuleInvoke": "Program((RuleInvoke('out', 'r', Literal(1)),), functions=(FunctionDef('when_true', (Return(Literal(1)),), params=('ctx',)), FunctionDef('then_same', (Return(Literal(1)),), params=('ctx',))), rules=(RuleDecl('r', 'when_true', 'then_same'),))",
    "StaticMethodCall": "Program((StaticMethodCall('out', 'C', 'sm'),), classes=_CLS, functions=_FN_OOP)",
    "TextConcat": "Program((TextConcat('out', TextLiteral('a'), TextLiteral('b')),))",
    "TextContains": "Program((TextContains('out', TextLiteral('ab'), TextLiteral('a')),))",
    "TextGet": "Program((TextGet('out', TextLiteral('ab'), Literal(0)),))",
    "TextLength": "Program((TextLength('out', TextLiteral('ab')),))",
    "TextSlice": "Program((TextSlice('out', TextLiteral('abcd'), Literal(1), Literal(2)),))",
    "Throw": "Program((Throw('err'),))",
    "TraitDecl": "Program((), traits=(TraitDecl('T', ('m',)),))",
    "TraitImpl": "Program((), traits=(TraitDecl('T', ('m',)),), trait_impls=(TraitImpl('C', 'T', (FunctionDef('m', (Return(Literal(1)),)),)),))",
    "TryCatch": "Program((TryCatch((Throw('e'),), 'e', (Display(Literal(1)),))))",
    "TypeAliasDecl": "Program((), type_aliases=(TypeAliasDecl('I', 'i32'),))",
    "TypeConvert": "Program((TypeConvert('out', Literal(1), 'i32', 'text')))",
    "TypeReflect": "Program((TypeReflect('out', 'i32'),))",
    "UnsafeEnter": "Program((UnsafeEnter(), Display(Literal(1)), UnsafeExit()))",
    "UnsafeExit": "Program((UnsafeEnter(), UnsafeExit(), Display(Literal(1))))",
    "Until": "Program((Assign('x', Literal(0)), Until(CompareEq(Reference('x'), Literal(1)), (Increase('x', Literal(1)),))))",
    "While": "Program((While(_COND, (Display(Literal(1)),))))",
    "Yield": "Program((GeneratorNew('g', 'gen'), Yield(Literal(1))), functions=_GEN_FN)",
}
# fmt: on

nodes = ast_statement_nodes()
missing = [n for n in nodes if n not in BUILDERS]
if missing:
    raise SystemExit(f"missing builders: {missing}")

lines = [
    '"""Phase 25 minimal AST programs — one per Statement union member."""',
    "",
    "from __future__ import annotations",
    "",
    "from collections.abc import Callable",
    "",
    "from .ast import *  # noqa: F403",
    "from .ast import Program",
    "",
    "_BODY = (Display(Literal(1)),)",
    "_COND = CompareEq(Literal(1), Literal(1))",
    "_FN = (",
    "    FunctionDef('f', (Return(Literal(1)),)),",
    "    FunctionDef('double', (Return(BinaryValue('multiply', Reference('x'), Literal(2))),), params=('x',), param_types=('i32',)),",
    "    FunctionDef('is_one', (Return(CompareEq(Reference('x'), Literal(1))),), params=('x',), param_types=('i32',)),",
    "    FunctionDef('add_pair', (Return(BinaryValue('add', Reference('a'), Reference('b'))),), params=('a', 'b'), param_types=('i32', 'i32')),",
    "    FunctionDef('wrap', (Return(Literal(1)),), params=('ctx',), param_types=('text',)),",
    ")",
    "_GEN_FN = (FunctionDef('gen', (Yield(Literal(1)), Return(Literal(0))),),)",
    "_CLS = (ClassDecl('C', None, (('p', 'i32'),), ('m', 'sm')),)",
    "_FN_OOP = _FN + (FunctionDef('m', (Return(Literal(1)),), params=('self',)), FunctionDef('sm', (Return(Literal(1)),), params=()))",
    "",
    "AST_PROGRAM_BUILDERS: dict[str, Callable[[], Program]] = {",
]
for name in sorted(BUILDERS):
    lines.append(f'    "{name}": lambda: {BUILDERS[name]},')
lines.append("}")
lines.extend(
    [
        "",
        "",
        "def build_ast_program(node_name: str) -> Program:",
        '    """Return minimal Program exercising one AST statement node."""',
        "    try:",
        "        return AST_PROGRAM_BUILDERS[node_name]()",
        "    except KeyError as exc:",
        '        raise KeyError(f"No AST smoke builder for {node_name!r}") from exc',
    ]
)
print("\n".join(lines))
