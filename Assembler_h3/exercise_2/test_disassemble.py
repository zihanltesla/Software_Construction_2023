import pytest
import disassemble


def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# test whether it can handle the normal machine codes
def test_disassemble_successful():
    machine_codes = ['000002', '030102', '00000a', '010202', '020006', '010204', '000207', '020209', '000001']
    expected_output = ['ldc R0 0', 'ldc R1 3', '@loop0:', 'prr R0', 'ldc R2 1', 'add R0 R2', 'cpy R2 R1', 'sub R2 R0', 'bne R2 @loop0', 'hlt']
    disassembler = disassemble.Disassembler()
    result = disassembler.disassemble(machine_codes)
    assert result == expected_output

# test whether it can raise an error when the length exceed the limit of code_width defined
def test_disassemble_invalid_length():
    machine_codes = ['0000002']
    disassembler = disassemble.Disassembler()
    with pytest.raises(ValueError, match="Invalid machine code length"):
        disassembler.disassemble(machine_codes)

# Test whether it can raise an error when the operation is not recognized
def test_disassemble_invalid_operation():
    machine_codes = ['000022']
    disassembler = disassemble.Disassembler()
    with pytest.raises(ValueError, match="Unknown opcode:"):
        disassembler.disassemble(machine_codes)


#simulate “hlt” with arguments non-zero
def test_disassemble_invalid_instruction():
    machine_codes = ['100001']
    disassembler = disassemble.Disassembler()
    with pytest.raises(AssertionError, match="Argument should be zero for operation with format '--'"):
        disassembler.disassemble(machine_codes)

#simulate “prr” with two arguments and two arguments are non-zero
def test_disassemble_invalid_instruction():
    machine_codes = ['01110a']
    disassembler = disassemble.Disassembler()
    with pytest.raises(AssertionError, match="Argument should be zero for operation with format 'r-'"):
        disassembler.disassemble(machine_codes)

