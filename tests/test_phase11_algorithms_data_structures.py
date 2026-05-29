"""Phase 11 algorithms and data-structures coverage."""

from __future__ import annotations

import random
import unittest

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.compiler import compile_program_to_ir, lower_ir_to_bytecode
from sanskript.errors import RuntimeSanskriptError
from sanskript.parser import parse_program
from sanskript.runtime_values import NIL
from sanskript.stdlib_core import call_native_function, list_native_functions
from sanskript.vm import SanskriptVM


class Phase11RegistryTests(unittest.TestCase):
    def test_alg_namespace_registered(self) -> None:
        self.assertTrue(any(name.startswith("std.alg.") for name in list_native_functions()))


class Phase11UnitTests(unittest.TestCase):
    def test_sort_stable_and_binary_search(self) -> None:
        self.assertEqual(call_native_function("std.alg.sort", [[5, 1, 3], "asc"]), [1, 3, 5])
        rows = [
            {"k": 2, "id": "a"},
            {"k": 1, "id": "b"},
            {"k": 2, "id": "c"},
        ]
        out = call_native_function("std.alg.stable_sort_by", [rows, "k", "asc"])
        self.assertEqual([row["id"] for row in out], ["b", "a", "c"])
        self.assertEqual(call_native_function("std.alg.binary_search", [[1, 3, 5, 8], 5]), 2)
        self.assertEqual(call_native_function("std.alg.binary_search", [[1, 3, 5, 8], 6]), -1)
        self.assertEqual(call_native_function("std.alg.binary_search", [[1, 2, 2, 2, 3], 2]), 1)

    def test_graph_algorithms(self) -> None:
        graph = {"a": ["b", "c"], "b": ["d"], "c": [], "d": []}
        self.assertEqual(call_native_function("std.alg.graph.bfs", [graph, "a"]), ["a", "b", "c", "d"])
        self.assertEqual(call_native_function("std.alg.graph.dfs", [graph, "a"]), ["a", "b", "d", "c"])
        dag = {"parse": ["type"], "type": ["lower"], "lower": []}
        self.assertEqual(
            call_native_function("std.alg.graph.topological_sort", [dag]),
            ["parse", "type", "lower"],
        )
        self.assertEqual(
            call_native_function("std.alg.graph.schedule_passes", [dag]),
            ["parse", "type", "lower"],
        )
        weighted = {
            "a": [["b", 1], ["c", 4]],
            "b": [["c", 2]],
            "c": [],
        }
        distances = call_native_function("std.alg.graph.dijkstra", [weighted, "a"])
        self.assertEqual(distances["c"], 3.0)

    def test_tree_heap_priority_and_dp(self) -> None:
        tree = {
            "value": 2,
            "left": {"value": 1, "left": None, "right": None},
            "right": {"value": 3, "left": None, "right": None},
        }
        self.assertEqual(call_native_function("std.alg.tree.traverse", [tree, "in"]), [1, 2, 3])
        pushed = call_native_function("std.alg.heap.push", [[3, 5], 1])
        popped = call_native_function("std.alg.heap.pop", [pushed])
        self.assertEqual(popped["value"], 1)
        tasks = [
            {"task": "lint", "priority": 2, "arrival": 0},
            {"task": "build", "priority": 1, "arrival": 0},
        ]
        self.assertEqual(call_native_function("std.alg.priority.schedule", [tasks]), ["build", "lint"])
        self.assertEqual(call_native_function("std.alg.dp.lcs_length", ["sanskrit", "sansar"]), 5)
        self.assertEqual(call_native_function("std.alg.dp.knapsack_01", [7, [[3, 4], [4, 5], [2, 3]]]), 9)

    def test_string_trie_suffix_and_interval(self) -> None:
        self.assertEqual(call_native_function("std.alg.string.kmp_search", ["bananaband", "anab"]), 3)
        trie = call_native_function("std.alg.trie.build", [["rama", "ravi"]])
        self.assertTrue(call_native_function("std.alg.trie.contains", [trie, "rama"]))
        self.assertFalse(call_native_function("std.alg.trie.contains", [trie, "ra"]))
        self.assertEqual(call_native_function("std.alg.suffix.array", ["banana"]), [5, 3, 1, 0, 4, 2])
        hits = call_native_function("std.alg.interval.query", [[[0, 2], [3, 5], [4, 8]], 4])
        self.assertEqual(hits, [[3, 5], [4, 8]])
        tree = call_native_function("std.alg.interval.tree_build", [[[0, 2], [3, 5], [4, 8]]])
        self.assertEqual(call_native_function("std.alg.interval.tree_query", [tree, 4]), [[3.0, 5.0], [4.0, 8.0]])

    def test_union_find_bitset_bloom(self) -> None:
        uf = call_native_function("std.alg.union_find.run", [5, [[0, 1], [3, 4]], [[0, 1], [1, 2], [3, 4]]])
        self.assertEqual(uf["connected"], [True, False, True])
        bitset = call_native_function("std.alg.bitset.new", [4])
        bitset = call_native_function("std.alg.bitset.set", [bitset, 2, True])
        self.assertTrue(call_native_function("std.alg.bitset.test", [bitset, 2]))
        bloom = call_native_function("std.alg.bloom.new", [32, 3])
        bloom = call_native_function("std.alg.bloom.add", [bloom, "agni"])
        self.assertTrue(call_native_function("std.alg.bloom.maybe_contains", [bloom, "agni"]))

    def test_matrix_vector_numeric_opt_parser_and_deterministic(self) -> None:
        mat = call_native_function("std.alg.matrix.mul", [[[1, 2], [3, 4]], [[2, 0], [1, 2]]])
        self.assertEqual(mat, [[4.0, 4.0], [10.0, 8.0]])
        self.assertEqual(call_native_function("std.alg.vector.dot", [[1, 2, 3], [4, 5, 6]]), 32.0)
        self.assertEqual(call_native_function("std.alg.vector.norm", [[3, 4]]), 5.0)
        area = call_native_function("std.alg.numeric.integrate_trapezoid", [[[0, 0], [1, 1], [2, 0]]])
        self.assertEqual(area, 1.0)
        self.assertEqual(call_native_function("std.alg.opt.gradient_descent_step", [10, 4, 0.5]), 8.0)

        token = call_native_function("std.alg.parser.match_text", ["nama"])
        seq = call_native_function("std.alg.parser.seq", [[token]])
        run = call_native_function("std.alg.parser.run", [seq, ["nama"]])
        self.assertTrue(run["ok"])
        choice = call_native_function(
            "std.alg.parser.choice",
            [[call_native_function("std.alg.parser.match_text", ["agni"]), token]],
        )
        run_choice = call_native_function("std.alg.parser.run", [choice, ["nama"]])
        self.assertTrue(run_choice["ok"])
        self.assertEqual(run_choice["parsed"], ["nama"])
        self.assertEqual(
            call_native_function(
                "std.alg.deterministic.unique",
                [[3, "3", 1, True, [1, 2], {"a": 1}, [1, 2], {"a": 1}, False]],
            ),
            [False, True, 1, 3, "3", [1, 2], {"a": 1}],
        )

    def test_negative_paths(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.sort", [[1, 2], "up"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.binary_search", [[3, 1, 2], 2])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.graph.dijkstra", [{"a": [["b", -1]], "b": []}, "a"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.graph.topological_sort", [{"a": ["b"], "b": ["a"]}])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.numeric.integrate_trapezoid", [[[1, 1]]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.interval.tree_build", [[[5, 4]]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.graph.schedule_passes", [{"a": ["b"], "b": ["a"]}])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.bloom.add", [{"size": 0, "hashes": 2, "bits": []}, "agni"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.bloom.maybe_contains", [{"size": 4, "hashes": 2, "bits": [True]}, "agni"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.priority.schedule", [[{"task": "lint", "priority": -1, "arrival": 0}]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.priority.schedule", [[{"task": "lint", "priority": 0, "arrival": -1}]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.alg.parser.seq", [[{"kind": "unknown"}]])

    def test_dijkstra_handles_undeclared_neighbor_as_leaf(self) -> None:
        graph = {"a": [["b", 1]], "c": []}
        distances = call_native_function("std.alg.graph.dijkstra", [graph, "a"])
        self.assertEqual(distances["a"], 0.0)
        self.assertEqual(distances["b"], 1.0)
        self.assertEqual(distances["c"], NIL)

    def test_deterministic_unique_distinguishes_scalar_types_and_nil(self) -> None:
        values = [True, 1, False, 0, NIL, NIL, "1", 1.0]
        unique = call_native_function("std.alg.deterministic.unique", [values])
        self.assertEqual(sum(1 for item in unique if item is True), 1)
        self.assertEqual(sum(1 for item in unique if item is False), 1)
        self.assertEqual(sum(1 for item in unique if isinstance(item, int) and not isinstance(item, bool) and item == 1), 1)
        self.assertEqual(sum(1 for item in unique if isinstance(item, int) and not isinstance(item, bool) and item == 0), 1)
        self.assertEqual(sum(1 for item in unique if item is NIL), 1)
        self.assertIn("1", unique)
        self.assertIn(1.0, unique)

    def test_deterministic_unique_permutation_invariance(self) -> None:
        rng = random.Random(7321)
        base = [
            {"k": 1, "v": [2, 3]},
            [1, 2],
            "agni",
            7,
            True,
            NIL,
            {"v": [2, 3], "k": 1},
            [1, 2],
            "agni",
        ]
        expected = call_native_function("std.alg.deterministic.unique", [base])
        for _ in range(30):
            trial = list(base)
            rng.shuffle(trial)
            got = call_native_function("std.alg.deterministic.unique", [trial])
            self.assertEqual(got, expected)


class Phase11VmSourceRoundTripTests(unittest.TestCase):
    @staticmethod
    def _compile(source: str) -> BytecodeProgram:
        parsed = parse_program(source)
        return lower_ir_to_bytecode(compile_program_to_ir(parsed))

    def test_vm_bytecode_calls_algorithms(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.LIST_NEW),
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.PUSH_TEXT, "asc"),
                Instruction(OpCode.CALL, "std.alg.sort"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["[2, 3, 4]"])

    def test_source_to_bytecode_to_vm_roundtrip(self) -> None:
        source = """
        samūhaḥ a.
        yojanam a 3.
        yojanam a 4.
        āhvānam std.alg.vector.norm a darśayati.
        """
        bytecode = self._compile(source)
        call_targets = [
            inst.operand
            for inst in bytecode.instructions
            if inst.opcode == OpCode.CALL
        ]
        self.assertIn("std.alg.vector.norm", call_targets)
        self.assertEqual(SanskriptVM().execute(bytecode), ["5.0"])

    def test_vm_bytecode_roundtrip_with_deterministic_unique(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.LIST_NEW),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.CALL, "std.alg.deterministic.unique"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["[1, 2, 3]"])

    def test_parser_ast_emits_qualified_alg_call(self) -> None:
        parsed = parse_program("āhvānam std.alg.vector.dot samūhaḥ 1 2 samūhaḥ 3 4 darśayati.")
        display_stmt = parsed.statements[0]
        call_expr = display_stmt.value
        self.assertEqual(call_expr.name, "dot")
        self.assertEqual(call_expr.module, "std.alg.vector")

    def test_compiler_lowers_multiple_phase11_calls(self) -> None:
        source = """
        samūhaḥ saṅkhyāḥ.
        yojanam saṅkhyāḥ 3.
        yojanam saṅkhyāḥ 4.
        yojanam saṅkhyāḥ 1.
        yojanam saṅkhyāḥ 2.
        āhvānam std.alg.vector.norm saṅkhyāḥ darśayati.
        āhvānam std.alg.deterministic.unique saṅkhyāḥ darśayati.
        """
        bytecode = self._compile(source)
        call_targets = [inst.operand for inst in bytecode.instructions if inst.opcode == OpCode.CALL]
        self.assertIn("std.alg.vector.norm", call_targets)
        self.assertIn("std.alg.deterministic.unique", call_targets)
        output = SanskriptVM().execute(bytecode)
        self.assertAlmostEqual(float(output[0]), 5.477225575051661, places=5)
        self.assertEqual(output[1], "[1, 2, 3, 4]")


if __name__ == "__main__":
    unittest.main()
