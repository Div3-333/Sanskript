# Generated Feature Matrix

_Generated at 2026-05-27T12:44:21+00:00 by `tools/generate_feature_matrix.py`._

Total features: **306**.

## Status summary

| Status | Count |
| --- | ---: |
| complete | 2 |
| foundation | 182 |
| partial | 70 |
| planned | 52 |

## Bytecode opcodes

| Opcode | Status | VM | Compiler | Yantra | Tests | Examples |
| --- | --- | --- | --- | --- | --- | --- |
| push_int | foundation | yes | yes | yes | 8 | 0 |
| push_text | foundation | yes | yes | yes | 5 | 0 |
| push_bool | foundation | yes | yes | yes | 2 | 0 |
| text_concat | foundation | yes | yes | yes | 3 | 0 |
| text_len | foundation | yes | yes | yes | 4 | 0 |
| text_get | foundation | yes | yes | yes | 3 | 0 |
| text_slice | foundation | yes | yes | yes | 3 | 0 |
| text_contains | foundation | yes | yes | yes | 7 | 0 |
| list_new | foundation | yes | yes | yes | 5 | 0 |
| list_append | foundation | yes | yes | yes | 7 | 0 |
| list_len | foundation | yes | yes | yes | 6 | 0 |
| list_get | foundation | yes | yes | yes | 5 | 0 |
| list_map | foundation | yes | yes | yes | 3 | 0 |
| list_filter | foundation | yes | yes | yes | 2 | 0 |
| list_reduce | foundation | yes | yes | yes | 2 | 0 |
| list_all | foundation | yes | yes | yes | 2 | 0 |
| list_scan | foundation | yes | yes | yes | 4 | 0 |
| list_zip | foundation | yes | yes | yes | 4 | 0 |
| list_enumerate | foundation | yes | yes | yes | 4 | 0 |
| list_any | foundation | yes | yes | yes | 4 | 0 |
| list_comprehension | foundation | yes | yes | yes | 4 | 0 |
| immutable_list_new | foundation | yes | yes | yes | 3 | 0 |
| immutable_list_append | foundation | yes | yes | yes | 4 | 0 |
| immutable_list_len | planned | — | — | — | 3 | 0 |
| immutable_list_get | planned | — | — | — | 3 | 0 |
| lazy_iter_new | foundation | yes | yes | yes | 4 | 0 |
| lazy_iter_next | foundation | yes | yes | yes | 4 | 0 |
| generator_new | foundation | yes | yes | yes | 4 | 0 |
| generator_next | foundation | yes | yes | yes | 4 | 0 |
| generator_yield | foundation | yes | yes | yes | 4 | 0 |
| pipeline_chain | foundation | yes | yes | yes | 4 | 0 |
| result_bind | foundation | yes | yes | yes | 4 | 0 |
| data_query | foundation | yes | yes | yes | 4 | 0 |
| rule_register | foundation | yes | yes | yes | 3 | 0 |
| rule_invoke | foundation | yes | yes | yes | 4 | 0 |
| memo_call | planned | — | — | yes | 3 | 0 |
| map_new | foundation | yes | yes | yes | 5 | 0 |
| map_set | foundation | yes | yes | yes | 6 | 0 |
| map_get | foundation | yes | yes | yes | 7 | 0 |
| map_contains | foundation | yes | yes | yes | 5 | 0 |
| record_new | foundation | yes | yes | yes | 3 | 0 |
| record_set | foundation | yes | yes | yes | 3 | 0 |
| record_get | foundation | yes | yes | yes | 3 | 0 |
| record_contains | foundation | yes | yes | yes | 2 | 0 |
| class_new | foundation | yes | yes | yes | 3 | 0 |
| method_call | foundation | yes | yes | yes | 4 | 0 |
| push_bigint | partial | yes | — | yes | 3 | 0 |
| push_bytes | foundation | yes | yes | yes | 3 | 0 |
| byte_new | partial | yes | — | yes | 2 | 0 |
| byte_len | partial | yes | — | yes | 2 | 0 |
| byte_get | partial | yes | — | yes | 2 | 0 |
| bytearray_new | partial | yes | — | yes | 3 | 0 |
| bytearray_set | partial | yes | — | yes | 2 | 0 |
| bytearray_get | partial | yes | — | yes | 2 | 0 |
| tuple_new | foundation | yes | yes | yes | 8 | 0 |
| tuple_get | foundation | yes | yes | yes | 6 | 0 |
| set_new | foundation | yes | yes | yes | 7 | 0 |
| set_add | foundation | yes | yes | yes | 7 | 0 |
| set_contains | partial | yes | — | yes | 2 | 0 |
| set_len | partial | yes | — | yes | 5 | 0 |
| deque_new | foundation | yes | yes | yes | 4 | 0 |
| deque_push_back | partial | yes | — | yes | 3 | 0 |
| deque_push_front | partial | yes | — | yes | 3 | 0 |
| deque_pop_back | partial | yes | — | yes | 3 | 0 |
| deque_pop_front | partial | yes | — | yes | 3 | 0 |
| deque_len | partial | yes | — | yes | 3 | 0 |
| option_none | foundation | yes | yes | yes | 5 | 0 |
| option_some | foundation | yes | yes | yes | 6 | 0 |
| option_is_some | partial | yes | — | yes | 2 | 0 |
| option_unwrap | partial | yes | — | yes | 4 | 0 |
| result_ok | foundation | yes | yes | yes | 5 | 0 |
| result_err | foundation | yes | yes | yes | 5 | 0 |
| result_is_ok | foundation | yes | yes | yes | 2 | 0 |
| result_unwrap_ok | foundation | yes | yes | yes | 4 | 0 |
| result_unwrap_err | foundation | yes | yes | yes | 4 | 0 |
| text_grapheme_len | partial | yes | — | yes | 8 | 0 |
| float_is_nan | partial | yes | — | yes | 4 | 0 |
| float_is_inf | partial | yes | — | yes | 4 | 0 |
| opaque_new | partial | yes | — | yes | 3 | 0 |
| array_new | partial | yes | — | yes | 4 | 0 |
| slice_view | partial | yes | — | yes | 3 | 0 |
| push_float | foundation | yes | yes | yes | 3 | 0 |
| heap_alloc | foundation | yes | yes | yes | 4 | 0 |
| heap_store | foundation | yes | yes | yes | 4 | 0 |
| heap_load | foundation | yes | yes | yes | 4 | 0 |
| heap_free | foundation | yes | yes | yes | 3 | 0 |
| unsafe_enter | foundation | yes | yes | yes | 4 | 0 |
| unsafe_exit | foundation | yes | yes | yes | 4 | 0 |
| load_name | foundation | yes | yes | yes | 6 | 0 |
| store_name | foundation | yes | yes | yes | 7 | 0 |
| add | complete | yes | yes | yes | 76 | 1 |
| subtract | foundation | yes | yes | yes | 7 | 0 |
| multiply | foundation | yes | yes | yes | 10 | 0 |
| divide | foundation | yes | yes | yes | 7 | 0 |
| compare_eq | foundation | yes | yes | yes | 3 | 0 |
| compare_ne | foundation | yes | yes | — | 2 | 0 |
| compare_lt | foundation | yes | yes | yes | 2 | 0 |
| compare_gt | foundation | yes | yes | — | 2 | 0 |
| compare_le | foundation | yes | yes | — | 2 | 0 |
| compare_identity | foundation | yes | yes | — | 2 | 0 |
| push_nil | foundation | yes | yes | — | 2 | 0 |
| scope_enter | foundation | yes | yes | — | 3 | 0 |
| scope_exit | foundation | yes | yes | — | 3 | 0 |
| break_loop | partial | yes | — | — | 2 | 0 |
| continue_loop | partial | yes | — | — | 2 | 0 |
| defer_push | partial | yes | — | — | 3 | 0 |
| defer_run | partial | yes | — | — | 3 | 0 |
| match_eq | foundation | yes | yes | — | 2 | 0 |
| match_tuple_len | partial | yes | — | — | 2 | 0 |
| match_record_has | partial | yes | — | — | 2 | 0 |
| emit | foundation | yes | yes | yes | 15 | 0 |
| jump | foundation | yes | yes | yes | 8 | 0 |
| jump_if_zero | foundation | yes | yes | yes | 3 | 0 |
| call | foundation | yes | yes | yes | 42 | 0 |
| tail_call | foundation | yes | yes | yes | 3 | 0 |
| push_func | foundation | yes | yes | — | 2 | 0 |
| return | foundation | yes | yes | yes | 124 | 0 |
| pop | foundation | yes | yes | yes | 18 | 0 |
| halt | foundation | yes | yes | yes | 10 | 0 |
| throw | foundation | yes | yes | yes | 5 | 0 |
| panic | foundation | yes | yes | yes | 7 | 0 |
| try_begin | foundation | yes | yes | yes | 4 | 0 |
| try_end | foundation | yes | yes | yes | 3 | 0 |

## Source constructs (AST)

| Construct | Status | Parser | Tests | Examples |
| --- | --- | --- | --- | --- |
| AlgebraicTypeDecl | partial | parse_sentence / parse_program | 2 | 0 |
| Assert | foundation | parse_sentence / parse_program | 16 | 0 |
| Assign | foundation | parse_sentence → assignment / nidhāna | 20 | 0 |
| Bind | complete | parse_sentence / parse_program | 9 | 1 |
| Block | foundation | parse_sentence / parse_program | 5 | 0 |
| Break | foundation | parse_sentence / parse_program | 6 | 0 |
| Call | foundation | parse_sentence → āhvāna | 24 | 0 |
| ClassMethodCall | foundation | parse_sentence / parse_program | 6 | 0 |
| ClassNew | foundation | parse_sentence / parse_program | 6 | 0 |
| ClassReflect | foundation | parse_sentence / parse_program | 6 | 0 |
| ConstDecl | foundation | parse_sentence / parse_program | 5 | 0 |
| Continue | foundation | parse_sentence / parse_program | 6 | 0 |
| CountedFor | foundation | parse_sentence / parse_program | 6 | 0 |
| DataQuery | foundation | parse_sentence / parse_program | 5 | 0 |
| Decrease | foundation | parse_sentence → hrasva | 5 | 0 |
| Defer | foundation | parse_sentence / parse_program | 6 | 0 |
| DestructureAssign | partial | parse_sentence / parse_program | 2 | 0 |
| Display | foundation | parse_sentence → darśana | 19 | 0 |
| FieldContains | foundation | parse_sentence / parse_program | 5 | 0 |
| FieldGet | foundation | parse_sentence / parse_program | 6 | 0 |
| FieldSet | foundation | parse_sentence / parse_program | 8 | 0 |
| ForEach | foundation | parse_sentence / parse_program | 6 | 0 |
| ForEachDestructure | foundation | parse_sentence / parse_program | 5 | 0 |
| ForwardDecl | foundation | parse_sentence / parse_program | 3 | 0 |
| FunctionDef | foundation | parse_program → vidhāna | 11 | 0 |
| GeneratorNew | foundation | parse_sentence / parse_program | 5 | 0 |
| GeneratorNext | foundation | parse_sentence / parse_program | 4 | 0 |
| GenericRecordDecl | partial | parse_sentence / parse_program | 4 | 0 |
| Guard | foundation | parse_sentence / parse_program | 5 | 0 |
| HeapAlloc | foundation | parse_sentence → kṣetra-ārambha | 5 | 0 |
| HeapFree | foundation | parse_sentence / parse_program | 4 | 0 |
| HeapLoad | foundation | parse_sentence / parse_program | 4 | 0 |
| HeapStore | foundation | parse_sentence / parse_program | 5 | 0 |
| If | foundation | parse_sentence → yadi | 15 | 0 |
| ImmutableListAppend | foundation | parse_sentence / parse_program | 6 | 0 |
| ImmutableListInit | foundation | parse_sentence / parse_program | 6 | 0 |
| Increase | foundation | parse_sentence → vṛddhi | 10 | 0 |
| InfiniteLoop | foundation | parse_sentence / parse_program | 6 | 0 |
| InstanceFinalize | foundation | parse_sentence / parse_program | 6 | 0 |
| Invariant | foundation | parse_sentence / parse_program | 4 | 0 |
| LazyIterNew | foundation | parse_sentence / parse_program | 5 | 0 |
| LazyIterNext | foundation | parse_sentence / parse_program | 4 | 0 |
| ListAll | foundation | parse_sentence / parse_program | 6 | 0 |
| ListAny | foundation | parse_sentence / parse_program | 6 | 0 |
| ListAppend | foundation | parse_sentence / parse_program | 8 | 0 |
| ListComprehension | foundation | parse_sentence / parse_program | 6 | 0 |
| ListEnumerate | foundation | parse_sentence / parse_program | 6 | 0 |
| ListFilter | foundation | parse_sentence / parse_program | 6 | 0 |
| ListGet | foundation | parse_sentence / parse_program | 5 | 0 |
| ListInit | foundation | parse_sentence → samūha-ārambha | 8 | 0 |
| ListLength | foundation | parse_sentence / parse_program | 5 | 0 |
| ListMap | foundation | parse_sentence / parse_program | 6 | 0 |
| ListReduce | foundation | parse_sentence / parse_program | 6 | 0 |
| ListScan | foundation | parse_sentence / parse_program | 6 | 0 |
| ListZip | foundation | parse_sentence / parse_program | 6 | 0 |
| MapContains | foundation | parse_sentence / parse_program | 5 | 0 |
| MapGet | foundation | parse_sentence / parse_program | 5 | 0 |
| MapInit | foundation | parse_sentence → kośa-ārambha | 5 | 0 |
| MapPut | foundation | parse_sentence / parse_program | 5 | 0 |
| Match | foundation | parse_sentence / parse_program | 7 | 0 |
| MatchExpr | foundation | parse_sentence / parse_program | 5 | 0 |
| MemoFunction | partial | parse_sentence / parse_program | 2 | 0 |
| MethodCall | foundation | parse_sentence / parse_program | 6 | 0 |
| MethodReflect | foundation | parse_sentence / parse_program | 6 | 0 |
| Multiply | foundation | parse_sentence → guṇana | 4 | 0 |
| NewtypeDecl | foundation | parse_sentence / parse_program | 5 | 0 |
| Panic | foundation | parse_sentence / parse_program | 7 | 0 |
| Phase3Bind | foundation | parse_sentence / parse_program | 4 | 0 |
| PipelineChain | foundation | parse_sentence / parse_program | 6 | 0 |
| Pop | foundation | parse_sentence / parse_program | 4 | 0 |
| PostCondition | foundation | parse_sentence / parse_program | 4 | 0 |
| PreCondition | foundation | parse_sentence / parse_program | 4 | 0 |
| Propagate | foundation | parse_sentence / parse_program | 6 | 0 |
| PropertyGet | foundation | parse_sentence / parse_program | 6 | 0 |
| RecordInit | foundation | parse_sentence → vastu-ārambha | 7 | 0 |
| RecordTypeDecl | foundation | parse_sentence / parse_program | 5 | 0 |
| ResultBind | foundation | parse_sentence / parse_program | 5 | 0 |
| Return | foundation | parse_sentence → pratyāgama | 21 | 0 |
| RuleDecl | foundation | parse_sentence / parse_program | 4 | 0 |
| RuleInvoke | foundation | parse_sentence / parse_program | 5 | 0 |
| StaticMethodCall | foundation | parse_sentence / parse_program | 6 | 0 |
| TextConcat | foundation | parse_sentence → vākya-saṃyoga | 5 | 0 |
| TextContains | foundation | parse_sentence / parse_program | 5 | 0 |
| TextGet | foundation | parse_sentence / parse_program | 5 | 0 |
| TextLength | foundation | parse_sentence / parse_program | 5 | 0 |
| TextSlice | foundation | parse_sentence / parse_program | 5 | 0 |
| Throw | foundation | parse_sentence / parse_program | 8 | 0 |
| TraitDecl | partial | parse_sentence / parse_program | 5 | 0 |
| TraitImpl | partial | parse_sentence / parse_program | 4 | 0 |
| TryCatch | foundation | parse_sentence / parse_program | 5 | 0 |
| TypeAliasDecl | foundation | parse_sentence / parse_program | 5 | 0 |
| TypeConvert | foundation | parse_sentence / parse_program | 5 | 0 |
| TypeReflect | foundation | parse_sentence / parse_program | 5 | 0 |
| UnsafeEnter | foundation | parse_sentence → arakṣita-praveśa | 4 | 0 |
| UnsafeExit | foundation | parse_sentence → arakṣita-nirgama | 4 | 0 |
| Until | foundation | parse_sentence / parse_program | 6 | 0 |
| While | foundation | parse_sentence → yāvat | 8 | 0 |
| Yield | foundation | parse_sentence / parse_program | 5 | 0 |

## Type catalog entries (implemented / partial)

| Type | Catalog impl | Status | Tests |
| --- | --- | --- | ---: |
| bool | partial | partial | 89 |
| byte | partial | partial | 25 |
| i8 | partial | partial | 4 |
| i16 | partial | partial | 2 |
| i32 | partial | partial | 16 |
| i64 | partial | partial | 4 |
| isize | partial | partial | 3 |
| u8 | partial | partial | 1 |
| u16 | partial | partial | 1 |
| u32 | partial | partial | 10 |
| u64 | partial | partial | 3 |
| usize | partial | partial | 2 |
| f64 | partial | partial | 4 |
| text | partial | partial | 125 |
| complex128 | partial | partial | 0 |
| decimal | partial | partial | 6 |
| bigint | partial | partial | 5 |
| optional | partial | partial | 40 |
| result | partial | partial | 47 |
| tuple | partial | partial | 89 |
| enum | partial | partial | 42 |
| array | partial | partial | 5 |
| slice | partial | partial | 6 |
| list | partial | partial | 100 |
| stack | partial | partial | 16 |
| queue | partial | partial | 5 |
| deque | partial | partial | 10 |
| hash_map | partial | partial | 3 |
| ordered_map | partial | partial | 3 |
| hash_set | partial | partial | 0 |
| bytes | partial | partial | 21 |
| bytearray | partial | partial | 5 |
| callable | partial | partial | 12 |
| object | partial | partial | 32 |
| module | partial | partial | 50 |
| class_instance | partial | partial | 2 |
