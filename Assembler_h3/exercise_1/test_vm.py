import pytest
import io
from contextlib import redirect_stdout
import sys
import os

script_dir = os.path.dirname(__file__)  # Path to the directory
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir+"/vm")

from vm import VirtualMachine
from architecture import OP_SHIFT,RAM_LEN,OPS

# This function runs the VM with a given program file and captures the output.
def run_vm_and_capture_output(file_path):
    vm = VirtualMachine()
    
    # Read the machine code from the file
    with open(file_path, 'r') as file:
        machine_code = [int(line.strip(), 16) for line in file if line.strip()]

    vm.initialize(machine_code)
    f = io.StringIO()
    with redirect_stdout(f):
        vm.run()
    output = f.getvalue()
    f.close()
    return output.strip()

#Test case1: 
# test virtual machine with normal usage
def test_vm_success():
    # Specify the path to your add.mx file
    file_path_add_hlt = "mx/add_hlt.mx"
    file_path_cpy_beq_sub = "mx/cpy_beq_sub.mx"
    file_path_ldc_ldr_prm_prr_bne_str = "mx/ldc_ldr_prm_prr_bne_str.mx"

    # Run the VM and capture the output.
    output_add_hlt = run_vm_and_capture_output(file_path_add_hlt)
    output_cpy_beq_sub = run_vm_and_capture_output(file_path_cpy_beq_sub)
    output_ldc_ldr_prm_prr_bne_str = run_vm_and_capture_output(file_path_ldc_ldr_prm_prr_bne_str)

    # The expected output is the printout of register R1, which should contain 9 (5+4).
    expected_output_add_hlt = ">> 9"
    # The expected output is the printout of register R3, the result should be 1 to 0 by substration(1,0)
    expected_output_cpy_beq_sub = ">> 1\n>> 0"
    # The expected output is the printout of memory value pointed by R2(2), and result from 2 to 1 by for loop(2,1)
    expected_output_ldc_ldr_prm_prr_bne_str = ">> 2\n>> 2\n>> 1"

    #Assert the output from common line is same as expected ones
    assert expected_output_add_hlt in output_add_hlt, f"Expected output '{expected_output_add_hlt}', got '{output_add_hlt}'"
    assert expected_output_cpy_beq_sub in output_cpy_beq_sub, f"Expected output '{expected_output_cpy_beq_sub}', got '{output_cpy_beq_sub}'"
    assert expected_output_ldc_ldr_prm_prr_bne_str in output_ldc_ldr_prm_prr_bne_str, f"Expected output '{expected_output_ldc_ldr_prm_prr_bne_str}', got '{output_ldc_ldr_prm_prr_bne_str}'"

#Test case2: 
# Out-of-memory error
def test_vm_out_of_memory_error():

    ldc_instruction = (OPS["ldc"]["code"] << OP_SHIFT) | 0x0000
    machine_code = [ldc_instruction for _ in range(RAM_LEN + 1)]

    vm = VirtualMachine()
    
    # Pytest to check whether the assertionerror "Program too long" been raised  
    with pytest.raises(AssertionError, match="Program too long"):
        vm.initialize(machine_code)

#Test case3:
# Instruction-not-found error
def test_vm_instruction_not_found_error():

    #.mx file contain "0x11" which is not recorgnized by virtual machine 
    machine_code = [0x11]

    vm = VirtualMachine()

    # Pytest to check whether the assertionerror “Unknown op" been raised  
    with pytest.raises(AssertionError, match="Unknown op"):
        vm.initialize(machine_code)
        vm.run()





