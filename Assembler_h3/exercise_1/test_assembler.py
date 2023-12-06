import pytest
import sys
import os
import sys

script_dir = os.path.dirname(__file__)  # Path to the directory
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir+"/vm")

from assembler import Assembler

# This function is used to read the assembler code from the .as file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# This function is used to write the out of assembler to the .mx file
def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for line in data:
            file.write(f"{line}\n")

# This function is to generate the test code from the .as and specify the location of storing the .mx files
def generate_test_env(instruction_name):

    #Self-designed assembler file for testing
    assembly_input_path = f"as/{instruction_name}.as"
    assembly_input=read_file(assembly_input_path)

    #Produce one .mx file for storing the assembler result
    test_output_path = f"mx/{instruction_name}.mx"
    
    return assembly_input, test_output_path

# Test operations: "add", "hlt", "ldc", "prr"
expected_output_add_hlt = ['050102', '040202', '020106', '00010a', '000001']
assembly_input_add_hlt, test_output_add_hlt = generate_test_env("add_hlt")

@pytest.mark.parametrize("assembly_input, expected_output,test_output_path", [
    (assembly_input_add_hlt, expected_output_add_hlt,test_output_add_hlt ),
])
def test_assemble_add_hlt(assembly_input, expected_output,test_output_path):

    assembler = Assembler()
    result = assembler.assemble(assembly_input)
    try:
        assert result == expected_output
    except AssertionError as e:
        print(f"Error during add_hlt test: {e}")
        raise
    
    with open(test_output_path, 'w') as file:
        for line in result:
            file.write(f"{line}\n")

# Test operations: "sub", "hlt", "ldc", "prr", "cpy", "beq"
expected_output_cpy_beq_sub = ['010102', '010202', '020304', '00030a', '010307', '030308', '000001']
assembly_input_cpy_beq_sub, test_output_cpy_beq_sub = generate_test_env("cpy_beq_sub")
@pytest.mark.parametrize("assembly_input, expected_output,test_output_path", [
    (assembly_input_cpy_beq_sub, expected_output_cpy_beq_sub,test_output_cpy_beq_sub ),
])
def test_assemble_cpy_beq_sub(assembly_input, expected_output,test_output_path):

    assembler = Assembler()
    result = assembler.assemble(assembly_input)
    try:
        assert result == expected_output
    except AssertionError as e:
        print(f"Error during cpy_beq_sub test: {e}")
        raise
    with open(test_output_path, 'w') as file:
        for line in result:
            file.write(f"{line}\n")
          

# Test operations: "sub", "hlt", "ldc", "prr", "str", "prm", "bne"
expected_output_ldc_ldr_prm_prr_bne_str = ['020002', '010102', '010202', '020005', '00020b', '010303', '00030a', '010307', '060309', '000001']
assembly_input_ldc_ldr_prm_prr_bne_str, test_output_ldc_ldr_prm_prr_bne_str = generate_test_env("ldc_ldr_prm_prr_bne_str")
@pytest.mark.parametrize("assembly_input, expected_output,test_output_path", [
    (assembly_input_ldc_ldr_prm_prr_bne_str, expected_output_ldc_ldr_prm_prr_bne_str,test_output_ldc_ldr_prm_prr_bne_str ),
])
def test_assemble_ldc_ldr_prm_prr_bne_str(assembly_input, expected_output,test_output_path):

    assembler = Assembler()
    result = assembler.assemble(assembly_input)
    try:
        assert result == expected_output
    except AssertionError as e:
        print(f"Error during ldc_ldr_prm_prr_bne_str test: {e}")
        raise
    with open(test_output_path, 'w') as file:
        for line in result:
            file.write(f"{line}\n")