import os
import sys

script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir + "/vm")

from architecture import OP_SHIFT, OP_MASK, OPS, OP_WIDTH

# [class]
class Disassembler:
    def disassemble(self, lines):
        machine_codes = self._get_machine_codes(lines)
        labels = self._find_labels(machine_codes)
        assembly_instructions = self._disassemble_codes(machine_codes, labels)
        return assembly_instructions

    # Reads lines of machine codes and validates their length.
    def _get_machine_codes(self, lines):
        machine_codes = []
        for line in lines:
            line = line.strip()
            if len(line) != OP_WIDTH: 
                raise ValueError(f"Invalid machine code length")
            machine_codes.append(int(line, 16))
        return machine_codes
    
    #  Find lables from the machine code by detecting "beq" and "bne"
    def _find_labels(self, machine_codes):
        labels = {}
        for address, code in enumerate(machine_codes):
            op, _, target_line = self._decode_instruction(code)

             # the operation code for "beq" and "bne"
            if op in [0x8, 0x9]:  
                if target_line not in labels:
                    labels[target_line] = f"@loop{len(labels)}"
        return labels


    
    # Processes the machine codes to generate assembly instructions.
    def _disassemble_codes(self, machine_codes, labels):
        assembly_instructions = []
        for address, code in enumerate(machine_codes):
            if address in labels:
                assembly_instructions.append(f"{labels[address]}:")

            op, arg0, arg1 = self._decode_instruction(code)
            instruction = self._format_instruction(op, arg0, arg1, labels, address)
            assembly_instructions.append(instruction)
        return assembly_instructions

    # Extracts operation code and arguments from machine codes.
    def _decode_instruction(self, code):
        op = code & OP_MASK
        code >>= OP_SHIFT
        arg0 = code & OP_MASK
        code >>= OP_SHIFT
        arg1 = code & OP_MASK
        return op, arg0, arg1

    # Formats the decoded instructions into readable assembly language.
    def _format_instruction(self, op, arg0, arg1, labels, current_address):
        for op_name, op_info in OPS.items():
            if op_info['code'] == op:
                fmt = op_info['fmt']
                if op in [0x8, 0x9]:
                    target_label = labels.get(arg1, f"@loop{arg1}")
                    return f"{op_name} R{arg0} {target_label}"
                return self._assemble_instruction(fmt, op_name, arg0, arg1)
        raise ValueError(f"Unknown opcode: {op:02x}")


    # Constructs assembly instruction based on format and operation.
    def _assemble_instruction(self, fmt, op_name, arg0, arg1):
        if fmt == '--':
            assert arg0 == 0, "Argument should be zero for operation with format '--'"
            assert arg1 == 0, "Argument should be zero for operation with format '--'"
            return op_name
        elif fmt == 'r-':
            assert arg1 == 0, "Argument should be zero for operation with format 'r-'"
            return f"{op_name} R{arg0}"
        elif fmt == 'rr':
            return f"{op_name} R{arg0} R{arg1}"
        elif fmt == 'rv':
            return f"{op_name} R{arg0} {arg1}"
    # [/class]

def main(disassembler_cls):
    assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input_file.mx output_file.as"
    with open(sys.argv[1], 'r') as reader:
        lines = reader.readlines()

    disassembler = disassembler_cls()
    assembly_instructions = disassembler.disassemble(lines)

    with open(sys.argv[2], 'w') as writer:
        for instruction in assembly_instructions:
            writer.write(instruction + '\n')

if __name__ == "__main__":
    main(Disassembler)
