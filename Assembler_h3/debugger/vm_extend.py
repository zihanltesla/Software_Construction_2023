import sys

from architecture import VMState
from vm_step import VirtualMachineStep


class VirtualMachineExtend(VirtualMachineStep):
    # [init]
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(reader, writer)
        self.watchpoints = {}
        self.handlers = {
            # "d": self._do_disassemble,
            "disassemble": self._do_disassemble,
            # "i": self._do_ip,
            "ip": self._do_ip,
            # "m": self._do_memory,
            "memory": self._do_memory,
            # "q": self._do_quit,
            "quit": self._do_quit,
            # "r": self._do_run,
            "run": self._do_run,
            # "s": self._do_step,
            "step": self._do_step,
            "watchpoint": self._do_add_watchpoint,
            "edit": self._do_edit_value
        }
    # [/init]

    # [interact]
    def interact(self, addr):
        # Generate the prompt by extracting the first character of each command and sorting them
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        # Flag to control the interaction loop
        interacting = True

        # Interaction loop
        while interacting:
            try:
                # Display the prompt and read user input
                command = self.read(f"{addr:06x} [{prompt}]> ")

                # Check if the input is empty and continue to next iteration
                if not command:
                    continue
                else:
                    # Find a matched command based on the user input
                    matched_cmd = self.find_matched_command(command)
                    if matched_cmd:
                        # Execute the corresponding command method
                        interacting = self.handlers[matched_cmd](self.ip)
                    else:
                        # If no matching command found, display an 'Unknown command' message
                        self.write(f"Unknown command {command}")

            except EOFError:
                # Set the VM state to FINISHED in case of EOFError and exit the interaction loop
                self.state = VMState.FINISHED
                interacting = False

    # [/interact]

    def _do_disassemble(self, addr):
        self.write(self.disassemble(addr, self.ram[addr]))
        return True

    def _do_ip(self, addr):
        self.write(f"{self.ip:06x}")
        return True

    # [memory]
    def _do_memory(self,addr):
        # 4.1  Show Memory Range
        # self.show()
        # Prompt the user to enter the first address and store it in a list
        user_input1 = self.read("Memory range,Enter an address: ").strip()
        addr = [user_input1]

        # Ask the user if they want to enter another address ('Y' for yes, 'N' for no)
        add_second_address = self.read("Do you want to enter another address? (Y/N): ").strip().upper()

        # If the user chooses to enter another address ('Y' for yes), prompt and add it to the address list
        if add_second_address.startswith('Y'):
            user_input2 = self.read("Enter another address: ").strip()
            addr.append(user_input2)

        if len(addr) == 1:
            # User input contains a single address
            addr = int(addr[0], 16)  # Convert the address to an integer
            # Display the value stored at the given address in hexadecimal format
            self.write(f"{addr:06x}: {self.ram[addr]:06x}")

        elif len(addr) == 2:
            # User input contains two addresses: start and end of the range
            start_address = int(addr[0], 16)  # Convert the start address to an integer
            end_address = int(addr[1], 16)  # Convert the end address to an integer
            # Display memory contents within the specified address range
            for adr in range(start_address, end_address + 1):
                # Display each memory address and its corresponding value in hexadecimal format
                self.write(f"{adr:06x}: {self.ram[adr]:06x}")
        else:
            # Invalid input format if not a single address or two addresses are provided
            self.write("Invalid input format. Provide one or two addresses.")

        return True
    # [/memory]

    def _do_quit(self, addr):
        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr):
        self.state = VMState.RUNNING
        return False

    # [step]
    def _do_step(self, addr):
        self.state = VMState.STEPPING
        return False
    # [/step]

    # [add_watchpoint]
    def _do_add_watchpoint(self, addr):
        # Prompt the user to enter the address to set a watchpoint
        addr = self.read("Enter address to set watchpoint:").strip()
        addr = int(addr, 16)  # Convert the address to an integer

        # Check if the address is not already in the watchpoints dictionary
        if addr not in self.watchpoints:
            self.watchpoints[addr] = self.ram[addr]  # Store the initial value at the address
            print(f"Watchpoint set at address {addr:06x}")
            return True
        else:
            print(f"Watchpoint already set at address {addr:06x}")
    # [/add_watchpoint]
    #
    def _do_edit_value(self,addr):
        # Prompt the user to enter the address that needs to be set to a new value
        addr = self.read("Enter address that need to set a new value:").strip()
        addr = int(addr, 16)  # Convert the address to an integer

        # Prompt the user to enter the new value to set to the address
        new_value = self.read("Enter the new value that need to set to the address:").strip()
        new_value = int(new_value,16)

        # Set the new value to the specified address in RAM
        self.ram[addr] = new_value

        # Check whether there is a watchpoint triggered at the address
        for w_addr, w_value in self.watchpoints.items():
            # If the address matches a watchpoint address and the RAM value is not the same as the watchpoint value
            if w_addr == addr and self.ram[addr] != w_value:
                print(f"Watchpoint triggered at address {addr:06x}")
                self.state = VMState.STEPPING  # Halt the VM
        return True


    #Find the matched comand based on the input
    def find_matched_command(self, input_command):
        # Convert the input command to lowercase
        input_command = input_command.lower()
        # Initialize matched_cmd variable to None
        matched_cmd = None
        # Iterate through the handlers to find a command that matches the input_command
        for cmd in self.handlers:
            # Check if the current command starts with the input_command
            if cmd.startswith(input_command):
                # Update matched_cmd with the matching command
                matched_cmd = cmd
                # Exit the loop when a match is found
                break

        # If no command matches the input_command, display a message
        if matched_cmd is None:
            self.write(f"No command matches '{input_command}'.")
        # Return the matched command (or None if no match is found)
        return matched_cmd


if __name__ == "__main__":
    VirtualMachineExtend.main()
