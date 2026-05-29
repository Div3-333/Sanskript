# Phase 11 Algorithms And Data Structures

Phase 11 extends the standard library with deterministic, VM-callable algorithm helpers under the `std.alg.*` namespace. These functions run through the same source -> parser -> AST -> compiler -> bytecode -> VM pipeline as all other native calls.

## Runtime entry points

- Sorting and search: `std.alg.sort`, `std.alg.stable_sort_by`, `std.alg.binary_search`
- Graphs: `std.alg.graph.bfs`, `std.alg.graph.dfs`, `std.alg.graph.dijkstra`, `std.alg.graph.topological_sort`, `std.alg.graph.schedule_passes`
- Trees/heaps/scheduling: `std.alg.tree.traverse`, `std.alg.heap.push`, `std.alg.heap.pop`, `std.alg.priority.schedule`
- Dynamic programming: `std.alg.dp.lcs_length`, `std.alg.dp.knapsack_01`
- Text indexing/search: `std.alg.string.kmp_search`, `std.alg.trie.build`, `std.alg.trie.contains`, `std.alg.suffix.array`
- Interval indexing: `std.alg.interval.query`, `std.alg.interval.tree_build`, `std.alg.interval.tree_query`
- Set/connectivity/probabilistic: `std.alg.union_find.run`, `std.alg.bitset.new`, `std.alg.bitset.set`, `std.alg.bitset.test`, `std.alg.bloom.new`, `std.alg.bloom.add`, `std.alg.bloom.maybe_contains`
- Numeric helpers: `std.alg.matrix.mul`, `std.alg.vector.dot`, `std.alg.vector.norm`, `std.alg.numeric.integrate_trapezoid`, `std.alg.opt.gradient_descent_step`
- Parser combinators and deterministic iteration: `std.alg.parser.match_text`, `std.alg.parser.seq`, `std.alg.parser.choice`, `std.alg.parser.run`, `std.alg.deterministic.unique`

## Source usage

Natural source calls use qualified names:

- `āhvānam std.alg.vector.norm a darśayati.`

Both lower to bytecode `CALL std.alg.*` opcodes and execute through the VM native dispatch.

## Determinism guarantees

- Topological ordering uses stable lexical tie-breaking for zero-indegree nodes.
- Deterministic unique extraction normalizes hashable forms and emits a total order across mixed primitive/structured values.
- Priority scheduling ties by arrival and task identity to avoid host-order nondeterminism.
- Binary search is left-biased for duplicate runs (returns first matching index).

## Compiler-pass graph helper

`std.alg.graph.schedule_passes` is the compiler-facing graph helper for pass dependency DAGs. It validates acyclicity and returns a deterministic topological pass order.

## Migration notes

| Host concept | Sanskript Phase 11 helper |
|--------------|----------------------------|
| `sorted(xs)` / `list.sort()` | `std.alg.sort` |
| Stable key sort (`sorted(xs, key=...)`) | `std.alg.stable_sort_by` |
| `bisect_left` lookup | `std.alg.binary_search` |
| BFS/DFS worklists | `std.alg.graph.bfs`, `std.alg.graph.dfs` |
| Dijkstra shortest paths | `std.alg.graph.dijkstra` |
| Compiler DAG pass ordering | `std.alg.graph.schedule_passes` |
| Binary tree walk helpers | `std.alg.tree.traverse` |
| `heapq` push/pop | `std.alg.heap.push`, `std.alg.heap.pop` |
| Disjoint-set union (DSU) | `std.alg.union_find.run` |
| Membership bit arrays | `std.alg.bitset.*` |
| Bloom membership filter | `std.alg.bloom.*` |
| Matrix multiply / vector norms | `std.alg.matrix.mul`, `std.alg.vector.*` |
| Trapezoid integration | `std.alg.numeric.integrate_trapezoid` |
| One-step gradient update | `std.alg.opt.gradient_descent_step` |
| Parser-combinator token matching | `std.alg.parser.*` |

## Limits

- `std.alg.binary_search` requires sorted ascending input and raises on unsorted data.
- `std.alg.graph.dijkstra` rejects negative edges.
- Bloom filters are probabilistic; false positives are possible.
- Interval tree helpers currently support point queries.
- `std.alg.priority.schedule` requires non-negative `arrival` and `priority`.
