"""Phase 25 minimal AST programs â€” one per Statement union member."""

from __future__ import annotations

from collections.abc import Callable

from .ast import *  # noqa: F403
from .ast import Program

_BODY = (Display(Literal(1)),)
_COND = CompareEq(Literal(1), Literal(1))
_FN = (
    FunctionDef('f', (Return(Literal(1)),)),
    FunctionDef('double', (Return(BinaryValue('multiply', Reference('x'), Literal(2))),), params=('x',), param_types=('i32',)),
    FunctionDef('is_one', (Return(Literal(1)),), params=('x',), param_types=('i32',)),
    FunctionDef('add_pair', (Return(BinaryValue('add', Reference('a'), Reference('b'))),), params=('a', 'b'), param_types=('i32', 'i32')),
    FunctionDef('wrap', (Return(Literal(1)),), params=('ctx',), param_types=('text',)),
    FunctionDef('gt4', (Return(Literal(1)),), params=('x',), param_types=('i32',)),
    FunctionDef('always_true', (Return(Literal(1)),), params=('x',), param_types=('i32',)),
)
_GEN_FN = (FunctionDef('gen', (Yield(Literal(1)), Return(Literal(0))),),)
_CLS = (
    ClassDecl(
        'C',
        None,
        (('p', 'i32'),),
        ('m',),
        static_methods=('sm',),
        class_methods=('make',),
        computed_properties=('p',),
    ),
)
_FN_OOP = _FN + (
    FunctionDef('m', (Return(Literal(1)),), params=('self',)),
    FunctionDef('sm', (Return(Literal(0)),), params=()),
    FunctionDef('C__static__sm', (Return(Literal(0)),), params=()),
    FunctionDef('C__make', (Return(Reference('n')),), params=('cls', 'n')),
)

AST_PROGRAM_BUILDERS: dict[str, Callable[[], Program]] = {
    "AlgebraicTypeDecl": lambda: Program((), algebraic_types=(AlgebraicTypeDecl('Opt', ('Some', 'None')),)),
    "Assert": lambda: Program((Bind('x', Literal(5)), Assert(CompareEq(Reference('x'), Literal(5))))),
    "Assign": lambda: Program((Assign('x', Literal(1)),)),
    "Bind": lambda: Program((Bind('x', Literal(1)),)),
    "Block": lambda: Program((Block(_BODY),)),
    "Break": lambda: Program((While(_COND, (Break(),)),)),
    "Call": lambda: Program((Call('f'),), functions=_FN),
    "ClassMethodCall": lambda: Program((ClassMethodCall('c', 'C', 'make', (Literal(3),)),), classes=_CLS, functions=_FN_OOP),
    "ClassNew": lambda: Program((ClassNew('obj', 'C'),), classes=_CLS),
    "ClassReflect": lambda: Program((ClassReflect('out', 'C'),), classes=_CLS),
    "ConstDecl": lambda: Program((ConstDecl('K', Literal(1)),)),
    "Continue": lambda: Program((While(_COND, (Continue(),)),)),
    "CountedFor": lambda: Program((CountedFor('i', Literal(0), Literal(1), (Display(Reference('i')),)),)),
    "DataQuery": lambda: Program((ListInit('rows'), ListAppend('rows', Literal(5)), DataQuery('hits', 'rows', 'score', 'gt4')), functions=_FN),
    "Decrease": lambda: Program((Assign('x', Literal(2)), Decrease('x', Literal(1)), Display(Reference('x')))),
    "Defer": lambda: Program((Defer((Display(Literal(1)),)), Display(Literal(2)))),
    "DestructureAssign": lambda: Program((DestructureAssign(PatternTuple((PatternWildcard(), PatternWildcard())), TupleLiteral((Literal(1), Literal(2)))),)),
    "Display": lambda: Program((Display(Literal(1)),)),
    "FieldContains": lambda: Program((RecordInit('r'), FieldContains('out', 'r', TextLiteral('k')))),
    "FieldGet": lambda: Program((RecordInit('r'), FieldSet('r', TextLiteral('k'), Literal(1)), FieldGet('out', 'r', TextLiteral('k')))),
    "FieldSet": lambda: Program((RecordInit('r'), FieldSet('r', TextLiteral('k'), Literal(1)))),
    "ForEach": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ForEach('v', 'xs', (Display(Reference('v')),)))),
    "ForEachDestructure": lambda: Program((ListInit('xs'), ListAppend('xs', TupleLiteral((Literal(1), Literal(2)))), ForEachDestructure(('a', 'b'), 'xs', (Display(Reference('a')),)))),
    "ForwardDecl": lambda: Program((ForwardDecl('x'), Assign('x', Literal(1)))),
    "FunctionDef": lambda: Program((), functions=(FunctionDef('f', (Return(Literal(1)),)),)),
    "GeneratorNew": lambda: Program((GeneratorNew('g', 'gen'),), functions=_GEN_FN),
    "GeneratorNext": lambda: Program((GeneratorNew('g', 'gen'), GeneratorNext('more', 'val', 'g')), functions=_GEN_FN),
    "GenericRecordDecl": lambda: Program((), generic_records=(GenericRecordDecl('Box', ('T',), ('value',)),)),
    "Guard": lambda: Program((Guard(_COND, (Display(Literal(1)),)),)),
    "HeapAlloc": lambda: Program((HeapAlloc('addr', Literal(4)),), safety_tier='arakshita'),
    "HeapFree": lambda: Program((HeapAlloc('addr', Literal(4)), HeapFree(Reference('addr'))), safety_tier='arakshita'),
    "HeapLoad": lambda: Program((HeapAlloc('addr', Literal(4)), HeapStore(Reference('addr'), Literal(9)), HeapLoad('out', Reference('addr'))), safety_tier='arakshita'),
    "HeapStore": lambda: Program((HeapAlloc('addr', Literal(4)), HeapStore(Reference('addr'), Literal(9))), safety_tier='arakshita'),
    "If": lambda: Program((If(_COND, (Display(Literal(1)),), (Display(Literal(0)),)),)),
    "ImmutableListAppend": lambda: Program((ImmutableListInit('xs'), ImmutableListAppend('ys', 'xs', Literal(1)))),
    "ImmutableListInit": lambda: Program((ImmutableListInit('xs'),)),
    "Increase": lambda: Program((Assign('x', Literal(1)), Increase('x', Literal(2)), Display(Reference('x')))),
    "InfiniteLoop": lambda: Program((InfiniteLoop((Break(),)),)),
    "InstanceFinalize": lambda: Program((ClassNew('obj', 'C'), InstanceFinalize('obj')), classes=_CLS, functions=_FN_OOP),
    "Invariant": lambda: Program((Invariant(_COND),)),
    "LazyIterNew": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), LazyIterNew('it', 'xs'))),
    "LazyIterNext": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), LazyIterNew('it', 'xs'), LazyIterNext('more', 'val', 'it'))),
    "ListAll": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListAll('out', 'xs', 'is_one')), functions=_FN),
    "ListAny": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListAny('out', 'xs', 'is_one')), functions=_FN),
    "ListAppend": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)))),
    "ListComprehension": lambda: Program((ImmutableListInit('n1'), ImmutableListAppend('n2', 'n1', Literal(1)), ListComprehension('out', 'n2', 'always_true', 'double')), functions=_FN),
    "ListEnumerate": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListEnumerate('out', 'xs'))),
    "ListFilter": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListFilter('out', 'xs', 'is_one')), functions=_FN),
    "ListGet": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListGet('out', 'xs', Literal(0)))),
    "ListInit": lambda: Program((ListInit('xs'),)),
    "ListLength": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListLength('out', 'xs'))),
    "ListMap": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListMap('out', 'xs', 'double')), functions=_FN),
    "ListReduce": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListReduce('out', 'xs', 'add_pair', Literal(0))), functions=_FN),
    "ListScan": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), ListScan('out', 'xs', 'add_pair', Literal(0))), functions=_FN),
    "ListZip": lambda: Program((ListInit('a'), ListInit('b'), ListAppend('a', Literal(1)), ListAppend('b', Literal(2)), ListZip('out', 'a', 'b'))),
    "MapContains": lambda: Program((MapInit('m'), MapPut('m', Literal(1), Literal(2)), MapContains('out', 'm', Literal(1)))),
    "MapGet": lambda: Program((MapInit('m'), MapPut('m', Literal(1), Literal(2)), MapGet('out', 'm', Literal(1)))),
    "MapInit": lambda: Program((MapInit('m'),)),
    "MapPut": lambda: Program((MapInit('m'), MapPut('m', Literal(1), Literal(2)))),
    "Match": lambda: Program((Match(Literal(1), (MatchArm(PatternLiteral(Literal(1)), (Display(Literal(1)),)),)),)),
    "MatchExpr": lambda: Program((MatchExpr('out', Literal(1), (MatchArm(PatternLiteral(Literal(1)), (Assign('out', Literal(1)),)),)),)),
    "MemoFunction": lambda: Program((), functions=(FunctionDef('mf', (Return(Literal(1)),), decorators=('smaraṇa',)),)),
    "MethodCall": lambda: Program((ClassNew('obj', 'C'), MethodCall('out', 'obj', 'm')), classes=_CLS, functions=_FN_OOP),
    "MethodReflect": lambda: Program((MethodReflect('out', 'C', 'm'),), classes=_CLS),
    "Multiply": lambda: Program((Assign('x', Literal(2)), Multiply('x', Literal(3)), Display(Reference('x')))),
    "NewtypeDecl": lambda: Program((), newtypes=(NewtypeDecl('UserId', 'i32'),)),
    "Panic": lambda: Program((Panic(TextLiteral('boom')),)),
    "Phase3Bind": lambda: Program((Phase3Bind('x', 'push_int', operand=1),)),
    "PipelineChain": lambda: Program((ListInit('xs'), ListAppend('xs', Literal(1)), PipelineChain('out', 'xs', ('double',))), functions=_FN),
    "Pop": lambda: Program((Pop(Literal(1)),)),
    "PostCondition": lambda: Program((PostCondition(_COND),)),
    "PreCondition": lambda: Program((PreCondition(_COND),)),
    "Propagate": lambda: Program((), functions=(FunctionDef('f', (Phase3Bind('r', 'result_err', value=TextLiteral('err')), Propagate(Reference('r'))),),)),
    "PropertyGet": lambda: Program((ClassNew('obj', 'C', (Literal(1),)), PropertyGet('out', 'obj', 'p')), classes=_CLS, functions=_FN_OOP),
    "RecordInit": lambda: Program((RecordInit('r'),)),
    "RecordTypeDecl": lambda: Program((), record_types=(RecordTypeDecl('Point', (('x', 'i32'), ('y', 'i32'))),)),
    "ResultBind": lambda: Program((Phase3Bind('r', 'result_ok', value=TextLiteral('ok')), ResultBind('out', 'r', 'wrap')), functions=_FN),
    "Return": lambda: Program((), functions=(FunctionDef('f', (Return(Literal(1)),)),)),
    "RuleDecl": lambda: Program((), functions=(FunctionDef('when_true', (Return(Literal(1)),), params=('ctx',)), FunctionDef('then_same', (Return(Literal(1)),), params=('ctx',))), rules=(RuleDecl('r', 'when_true', 'then_same'),)),
    "RuleInvoke": lambda: Program((RuleInvoke('out', 'r', Literal(1)),), functions=(FunctionDef('when_true', (Return(Literal(1)),), params=('ctx',)), FunctionDef('then_same', (Return(Literal(1)),), params=('ctx',))), rules=(RuleDecl('r', 'when_true', 'then_same'),)),
    "StaticMethodCall": lambda: Program((StaticMethodCall('out', 'C', 'sm'),), classes=_CLS, functions=_FN_OOP),
    "TextConcat": lambda: Program((TextConcat('out', TextLiteral('a'), TextLiteral('b')),)),
    "TextContains": lambda: Program((TextContains('out', TextLiteral('ab'), TextLiteral('a')),)),
    "TextGet": lambda: Program((TextGet('out', TextLiteral('ab'), Literal(0)),)),
    "TextLength": lambda: Program((TextLength('out', TextLiteral('ab')),)),
    "TextSlice": lambda: Program((TextSlice('out', TextLiteral('abcd'), Literal(1), Literal(2)),)),
    "Throw": lambda: Program((Throw(TextLiteral('err')),)),
    "TraitDecl": lambda: Program((), traits=(TraitDecl('T', None, (('m', (), 'i32'),)),)),
    "TraitImpl": lambda: Program((), record_types=(RecordTypeDecl('C', (('m', 'i32'),)),), traits=(TraitDecl('T', None, (('m', (), 'i32'),)),), trait_impls=(TraitImpl('C', 'T'),)),
    "TryCatch": lambda: Program((TryCatch((Throw(TextLiteral('e')),), 'e', (Display(Reference('e')),)),)),
    "TypeAliasDecl": lambda: Program((), type_aliases=(TypeAliasDecl('I', 'i32'),)),
    "TypeConvert": lambda: Program(statements=(Bind('raw', Literal(1)), TypeConvert('msg', 'text', Reference('raw')))),
    "TypeReflect": lambda: Program((TypeReflect('out', 'i32'),)),
    "UnsafeEnter": lambda: Program((UnsafeEnter(), Display(Literal(1)), UnsafeExit())),
    "UnsafeExit": lambda: Program((UnsafeEnter(), UnsafeExit(), Display(Literal(1)))),
    "Until": lambda: Program((Assign('x', Literal(0)), Until(CompareEq(Reference('x'), Literal(1)), (Increase('x', Literal(1)),)))),
    "While": lambda: Program((While(_COND, (Display(Literal(1)),)),)),
    "Yield": lambda: Program((), functions=_GEN_FN),
}


def build_ast_program(node_name: str) -> Program:
    """Return minimal Program exercising one AST statement node."""
    try:
        return AST_PROGRAM_BUILDERS[node_name]()
    except KeyError as exc:
        raise KeyError(f"No AST smoke builder for {node_name!r}") from exc
