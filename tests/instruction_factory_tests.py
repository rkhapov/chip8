import unittest
from parser.instruction_factory import InstructionFactory
from instructions.cls_instruction import ClsInstruction


class InstructionFactoryTests(unittest.TestCase):
    def test_from_opcode_creates_right_cls(self):
        factory = InstructionFactory()

        sut = factory.from_opcode(bytearray([0x00, 0xE0]))

        self.assertTrue(isinstance(sut, ClsInstruction))
        self.assertTrue(sut.arg_constant is None)
        self.assertTrue(sut.arg_registers == [])
