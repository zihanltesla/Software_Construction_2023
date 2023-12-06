# 1. Unit Testing
### A. To test the Assembler
In `test_assembler.py`file, we utilized `pytest` framework to conduct tests for `assembler.py`
- Setting up different simple .as files which contains the 11 different operations seperately, and store them inside `/.as` folder
- We manually calculted the machine codes and write them inside the test cases for comparison
- By using 3 different tests to cover the three assembler files and each of them will generate a .mx file inside `/.mx` folder
- You can check the covering by running:
```python
 pip install pytest==7.1.2 
 pip install pytest-cov==3.0.0 
 pytest --cov
```
or
```python 
 pytest --cov=assembler --cov-report term-missing
```
to check the missing lines.

### B. To test the Virtual Machine
The `test_vm.py` file runs a given program in machine code and capture the output produced by VM. 
The meaning of unit testing is to assume that each component works independently to ensure that when testing one component, other components are working properly. 
***We assume the assembler is correct***, first of all, if there is no guarantee that the assembler is running correctly, then when the VM test fails, ***it is difficult to determine whether the problem lies in the VM or the Assembler***. This increases the difficulty of diagnosing and fixing problems. Secondly whenever a VM's test fails, we need to ***additionally check the Assembler's output*** to determine whether the error is caused by the VM or Assembler.

- Use `test_vm_success()` test case to test the functionality of the VM by using the .mx file produced by tests of assembler. It runs the VM, captures the output, and then checks if the expected output of virsual machine for example `>> 9` is present in the captured output.

- Use `test_vm_lack_memory.py()` test case to verify whether there will crash when RAM exceeded.

- Use `test_vm_instruction_not_found_error()` test case to verify whether there will a asserionerror when the instruction is unknown.

- You can check the covering report by running:

```python 
 pytest --cov=vm --cov-report term-missing
```
to check the missing lines, here we covered all the lines except the main function.

---

# 2. Disassembler
To solve this problem, we modified the file `disassemble.py` and add a file named 'test_disassemble.py' in the `exercise_2` folder.
`disassemble.py` is used to perform disassembly of machine codes into assembly instructions and also test the functionalities of it.
## A. Applying disassembler
- Use the line below which will generate a corresponding .as file as output_file.as, in this assembler file, it discribes the behavior of counting up a number to 3. Our disassembler can handle normal operations as well as label with operations.
```python
python3 disassemble.py input_file.mx output_file.as
``` 
- `_get_machine_codes`: Reads lines of machine codes and validates their length.
- `_disassemble_codes`: Processes the machine codes to generate assembly instructions.
- `_decode_instruction`: Extracts operation code and arguments from machine codes.
- `_find_labels`: Find lables from the machine code by detecting "beq" and "bne".
- `_format_instruction`: Formats the decoded instructions into readable assembly language.
- `_assemble_instruction`: Constructs assembly instruction based on format and operation.


## B. Test disassembler

### 1. Test Disassemble

- **Description**: This test verifies that valid machine codes are correctly disassembled into the expected assembly instructions which we design in assember sections. We will be using `pytest-cov` whcih mentioned in the linked aticle to measure the code coverage.

```python
 pytest --cov=disassemble --cov-report term-missing
``` 
### 2. Test Disassemble Invalid Length

- **Description**: This test checks the disassembler's response to machine codes with invalid lengths. It ensures that a `ValueError` is raised for machine codes that do not meet the expected length requirements, here we disgned a code with length `7` which will trigger the error
- **Invalid Machine Code**: `0000002`
- **Expected Exception**: `ValueError`

### 3. Test Disassemble Invalid Operation

- **Description**: This test is designed to verify the handling of unknown operation codes by the disassembler. It confirms that a `ValueError` is raised for machine codes with unrecognized operation codes, here `22` is an unknow operatioon
- **Invalid Machine Code**: `000022`
- **Expected Exception**: `ValueError`

### 4. Test Disassemble Invalid Instruction (hlt with non-zero arguments)

- **Description**: This test ensures that the disassembler raises an exception when the `hlt` instruction (which should not have any arguments) is provided with non-zero arguments.
- **Invalid Machine Code**: `100001`
- **Expected Exception**: `AssertionError`

### 5. Test Disassemble Invalid Instruction (prr with two non-zero arguments)

- **Description**: This test checks for the correct handling of invalid instructions, specifically the `prr` instruction with two non-zero arguments, which is not allowed.
- **Invalid Machine Code**: `01110a`
- **Expected Exception**: `AssertionError`


---

# 3. New features and Problems - Assembler
## 3.1 Increment and Decrement

Using:
```python
python3 assembler.py example_3_1.as output_3_1.mx
python3 vm.py output_3_1.mx -
```
Add instructions inc and dec to our assembly language that add one to the value of a register and subtract one from the value of a register

**inc** and **dec** instructions, with respective hexadecimal codes and format "r-" were added to the file: `architecture.py` . In addition in `vm.py` file lines for implementing the instructions were also included - which increased and decreased the value by 1 in the respective register.

## 3.2 Swap values

Using:
```python
python3 assembler.py example_3_2.as output_3_2.mx
python3 vm.py output_3_2.mx -
```
Add instruction swp R1 R2 that swaps the values in R1 and R2 without affecting the values in other registers.

**swp** instruction with a corresponding hexadecimal code and format "r-" were added to the file: `architecture.py`  . In addition in `vm.py` file lines for implementing the instructions were also included - which swapped the values across two registers using a temporary variable but this could be done directly too.

## 3.3 Reverse array in place

Using:
```python
python3 arrays.py example_3_3.as output_3_3.mx
python3 vm.py output_3_3.mx -
```

Write an assembly language program that starts with:<br>
• the base address of an array in one word <br>
• the length of the array N in the next word <br>
• N values immediately thereafter and reverses the array in place<br>

We load the length of the array at the start into register R1 and then the same value needs to be loaded into R1 inside the Verification step. We can change the value loaded in R1 to an even number ( ex. 4) to store an array whose length is odd as the index begins at 0, or an odd number (ex. 5) to store an array whose length is even

We use two pointers which point to the position at the begining **(front)** of the array and one at the end **(back)**. At the end of each iteration we compute the difference of the two pointers and if it is non-zero we increment the front pointer by one(+1) and decrement the back pointer by one(-1) and swap values in place. <br>
1. Odd length strings: The pointers coincide on the element at the middle of the string and the loop for swapping breaks using the **bne** condition <br>
2. Even length strings: The pointers go past each other and when their difference is -1 we break out of the loop using the **beq** condition <br>



# 4. New features - Debugger
## 4.1. Show Memory Range
To solve this problem, we modified the 'vm_extend.py' in the `debugger/`folder. 

In the 'vm_extend.py' file, the `_do_memory()` method is modified. 
- First, the user is prompted to enter the first address on the command line, and the value entered for the first time is stored in an address list. 
- Then the user is asked whether he/she needs to enter the second address value, the user can enter Y/YES or N/No (regardless of case). 
- If the user enters 'y', the user is prompted to enter the second address and adds it to the address list. 
- Determine the length of the address list:
  - If The length is equal to 1, converting the address to an integer, then display the value stored at the given address in hexadecimal format.
  - If the length is equal to 2, set the first value as the start address and set the second value as the end address, then display memory contents within the specified address range in hexadecimal format.
  - If the input(s) is invalid, show an alert "Invalid input format. Provide one or two addresses."

To test this feature,you can follow those steps:
- `cd debugger`
- `debugger % python vm_break.py count_up.mx`
- `000000 [bcdeimqrsw]> m` you can instead 'm' with any number of distinct leading characters of `memory`
- `Memory range,Enter an address: `: enter the address you want to show the value
- `Do you want to enter another address? (Y/N):`: if you want to show all the memory between two addresses,you can enter 'Y'/'yes', regardless of case. Otherwise,you can enter 'No'/'N'.
- `Enter another address: ` enter the end address
- show the values of address.


## 4.2 Breakpoint Addresses
To solve this problem,we modified the 'vm_break.py' in the `debugger/`folder. 

In the file 'vm_break.py',we modified the`_do_add_breakpoint()`method and `_do_clear_breakpoint()`method.

`_do_add_breakpoint()` is to add a breakpoint when user specifies an address.
- Prompting users for providing the address need to set breakpoint
- Checking if the provided address is valid within the Ram length,if the address is invalid,display message "invalid address"
- Setting breakpoint at the specified address:
  - checking whether there is already a breakpoint at the address, if yes, show message "Breakpoint already set at address".
  - If there is no breakpoint at the address,checking whether the instruction at the specified memory address is not already representing
  a breakpoint.If not, storing the original instruction in breaks dictionary,set the instruction at the address to be a breakpoint.
  - Displaying the message: Breakpoint set at address.

`_do_clear_breakpoint()` is to clear the breakpoint at a specified address.
- Prompting users for providing the address need to clear breakpoint
- Checking if the provided address is valid within the Ram length,if the address is invalid,display message "invalid address"
- Checking whether a breakpoint exists at the address:
  - if there is a breakpoint,remove the breakpoint from the breaks dictionary, then display the message indicating successful breakpoint clearance.
  - if there is not a breakpoint, display message: No breakpoint set at address.


To test this feature,you can follow those steps:
- `cd debugger`
- `debugger % python vm_break.py count_up.mx`
- `000000 [bcdeimqrsw]> b`: you can instead 'b' with any number of distinct leading characters of `break`,to add breakpoint command.
- `Enter address to set breakpoint:` enter the address need to set a breakpoint, if set breakpoint successfully, you can see a message "Breakpoint already set at address"

After setting a breakpoint at a specific address, when use 'run' command to run a program,before the address that have set a breakpoint, we should run the program step by step.
and we can the result of each step.


- `000000 [bcdeimqrsw]> c`: you can instead 'c' with any number of distinct leading characters of `clear`,to clear breakpoint command
- `Enter address to clear breakpoint:` enter the address need to clear a breakpoint. if the breakpoint is cleared, you will see a message "Breakpoint cleared at address ", if there is no breakpoint, you will see a message "No breakpoint set at address XX"

## 4.3 Command Completion
To solve this problem, we modified the 'vm_extend.py' in the `debugger/`folder. In the file,we added a `find_matched_command()` and modified the `interact()` method.

`find_matched_command()` is used to find the matched command based on the input.
- the `input_command` as argument.
- Convert the input command to lowercase
- Initialize `matched_cmd` variable to None
- Iterate through the handlers to find a command that starts with the input_command,
if found,Update `matched_cmd` with the matching command.
- if no command matches the input_command, display a message "No command matches"
- return `matched_cmd`

`interact()`: in this method, we used the `find_matched_command()` to find a matched command based on the user's input, then 
execute the corresponding command method.


To test this feature,you can follow those steps(Take the `memory` command as an example):
- `cd debugger`
- `debugger % python vm_break.py count_up.mx`
- `000000 [bcdeimqrsw]> ME`: you can instead `ME` with any number of distinct leading characters of `memory`,
regardless of case.

Of course, you can test with other command.

## 4.4 Watchpoints
To solve the problem, we modified the 'vm_extend.py' in the `debugger/`folder. In the file, we
added `_do_add_watchpoint()` and `_do_edit_value()` method, modified `__init__()`.

in `__init__()`, initialize watchpoint as an empty dictionary, in the `handlers` dictionary,add a command to set a watchpoint 
and a command to change the value of a given address.

`_do_add_watchpoint()` is used to add a watchpoint at a specified address.
- Prompt the user to enter the address to set a watchpoint
- Checking if the address is already in the watchpoints dictionary.
  - if yes, display a message "Watchpoint already set at address".
  - if not, store the initial value present at the address in the `watchpoints` dictionary. Display message "Watchpoint set at address".
  

`_do_edit_value()` is used to change the value of a specified address.
- Prompt the user to enter the address that needs to be set to a new value.
- Prompt the user to enter the new value to set to the address.
- Set the new value to the specified address in RAM.
- Check whether there is a watchpoint triggered at the address. If the address matches a watchpoint address and the RAM value is not the same as the watchpoint value, then halt the VM and display a message"Watchpoint triggered at address".

To test this feature,you can follow those steps:
- `cd debugger`
- `debugger % python vm_break.py count_up.mx`
- `000000 [bcdeimqrsw]> w`: you can instead 'w' with any number of distinct leading characters of `watchpoint`,to add watchpoint command,regardless of case.
- `Enter address to set watchpoint:` enter the address need to set watchpoint
- `000000 [bcdeimqrsw]> e`:you can instead 'e' with any number of distinct leading characters of `edit`,to do_edit_value command, regardless of case.
- `Enter address that need to set a new value:` Enter the address that need to set a new value.
- `Enter the new value that need to set to the address:`Enter new value to the specified address.
- if the address is set with a watchpoint, a message is displayed"Watchpoint triggered at address xx" and VM halt.


