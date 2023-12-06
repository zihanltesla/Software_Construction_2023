import sys

from architecture import OPS, VMState
from vm_extend import VirtualMachineExtend


class VirtualMachineBreak(VirtualMachineExtend):
    # [init]
    def __init__(self):
        super().__init__()
        self.breaks = {}
        self.handlers |= {
            "b": self._do_add_breakpoint,
            "break": self._do_add_breakpoint,
            "c": self._do_clear_breakpoint,
            "clear": self._do_clear_breakpoint,
        }
    # [/init]

    # [show]
    def show(self):
        super().show()
        if self.breaks:
            self.write("-" * 6)
            for key, instruction in self.breaks.items():
                self.write(f"{key:06x}: {self.disassemble(key, instruction)}")
    # [/show]

    # [run]
    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
            instruction = self.ram[self.ip]
            op, arg0, arg1 = self.decode(instruction)

            if op == OPS["brk"]["code"]:
                original = self.breaks[self.ip]
                op, arg0, arg1 = self.decode(original)
                self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)

            else:
                if self.state == VMState.STEPPING:
                    self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)
    # [/run]

    # [add]
    def _do_add_breakpoint(self, addr):
        # Prompt the user for input: provide the address need to set breakpoint
        addr = self.read("Enter address to set breakpoint: ").strip()
        addr = int(addr, 16)


        # Check if the provided address is valid within the RAM length
        if addr >= len(self.ram) or addr < 0:
            # Display message if the address is invalid
            self.write("invalid address")
            # Exit the method if the address is invalid
            return False

        # Set breakpoint at the specified address
        # Check if the address doesn't have a breakpoint already set
        if addr not in self.breaks:
            # Check if the instruction at the address is not already a breakpoint
            if self.ram[addr] != OPS["brk"]["code"]:
                # Store the original instruction in breaks dictionary
                self.breaks[addr] = self.ram[addr]
                # Set the instruction at the address to be a breakpoint
                self.ram[addr] = OPS["brk"]["code"]
                # Display message indicating successful breakpoint set
                self.write(f"Breakpoint set at address {addr:06x}")
            # else:
            #     # Display message if a breakpoint is already set at the address
            #     self.write(f"Breakpoint already set at address {addr:06x}")
        else:
            # Display message if a breakpoint is already set at the address
            self.write(f"Breakpoint already set at address {addr:06x}")
        # Return True to indicate the operation was completed successfully
        return True
    # [/add]

    # [clear]
    def _do_clear_breakpoint(self, addr):
        # Prompt the user for input: provide the address need to set breakpoint
        addr = self.read("Enter address to clear breakpoint: ").strip()
        addr = int(addr, 16)

        # Check if the provided address is valid within the RAM length
        if addr >= len(self.ram) or addr < 0:
            # Display message for an invalid address
            self.write("Invalid address provided.")
            return False

        # Clear breakpoint at the specified address
        # Check if a breakpoint exists at the address
        if addr in self.breaks:
            # Restore the original instruction at the breakpoint address
            self.ram[addr] = self.breaks[addr]
            # Remove the breakpoint from the breaks dictionary
            del self.breaks[addr]
            # Display message indicating successful breakpoint clearance
            self.write(f"Breakpoint cleared at address {addr:06x}")
        else:
            # Display message if no breakpoint is set at the address
            self.write(f"No breakpoint set at address {addr:06x}")
        return True  # Return True to indicate the operation was completed successfully
    # [/clear]

if __name__ == "__main__":
    VirtualMachineBreak.main()
