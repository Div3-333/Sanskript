import unittest

from sanskript.bytecode import Instruction, OpCode
from sanskript.compiler import compile_source
from sanskript.vm import SanskriptVM


class NativeLanguageLevelTests(unittest.TestCase):
    def test_surakshita_expressions_and_less_than_loops(self) -> None:
        program = compile_source(
            """
            gaṇitam phale śūnya.
            punaḥ phala nyūnam pañca.
            gaṇitam phale phala yoga eka.
            antam.
            gaṇakaḥ phalaṃ darśayati.
            darśanam phala bhāga pañca.
            """
        )

        self.assertIn(Instruction(OpCode.COMPARE_LT), program.instructions)
        self.assertEqual(SanskriptVM().execute(program), ["5", "1"])

    def test_surakshita_list_index_and_length_source_forms(self) -> None:
        program = compile_source(
            """
            samūhaḥ phale.
            yojanam phale pañca.
            yojanam phale daśa.
            samūhāharaṇam mūlya phale eka.
            gaṇakaḥ mūlyaṃ darśayati.
            parimāṇam mūlya phale.
            gaṇakaḥ mūlyaṃ darśayati.
            """
        )

        self.assertIn(Instruction(OpCode.LIST_GET), program.instructions)
        self.assertIn(Instruction(OpCode.LIST_LEN), program.instructions)
        self.assertEqual(SanskriptVM().execute(program), ["10", "2"])

    def test_rakshita_source_controls_heap_inside_unsafe_region(self) -> None:
        program = compile_source(
            """
            rakṣitam.
            arakṣitaḥ adhikāraḥ ārabhyate.
            avakāśaḥ sthāna eka.
            smṛtisthāpanam sthāna pañca.
            smṛtyāharaṇam phala sthāna.
            smṛtimokṣaḥ sthāna.
            arakṣitaḥ adhikāraḥ samāpyate.
            gaṇakaḥ phalaṃ darśayati.
            """
        )

        self.assertEqual(program.safety_tier, "rakshita")
        self.assertIn(Instruction(OpCode.UNSAFE_ENTER), program.instructions)
        self.assertIn(Instruction(OpCode.HEAP_ALLOC), program.instructions)
        self.assertEqual(SanskriptVM().execute(program), ["5"])


if __name__ == "__main__":
    unittest.main()
