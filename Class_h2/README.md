

 # 1. More Capabilities
In this exercise, we added functions to the `lgl_interpreter.py` file to implement the functionality required in Exercise 1
of Assignment 2, such as multiplication, division, power, printing, while loop, creating a new array of fixed length, etc.
We create a file named `example_operations.gsc` to input the structures to implement functionality required in the exercise and can be executed 
from the terminal using the command: `python lgl_interpreter.py example_operations.gsc`.


`lgl_interpreter.py` file includes three parts, they are Helper Functions,Execution Functions and Operation Functions.

- **Helper Functions**:
  - `do_function`：is designed to transform function definitions in the LGL language into a list containing parameters 
  and the function body, which can be stored in the environment for subsequent use. 
  - `do_call_function`:handles function calls in the LGL language, it evaluates the function name, and executes the function body within a local environment frame.
  - `envs_set`:is used to set the value of a variable in the current environment frame.
  - `envs_get`:is used to retrieve the value of a variable by searching through the environment stack.
  - `do_set`:handles the assignment of values to variables or instance attributes in the LGL language. 
  - `do_get`: handles variable retrieval and function calls in the LGL language.When making a function call,
  it sets up a local environment frame,executes the function body, and then removes the 
  local environment frame.
  - `get_instance_variable`:provides a mechanism to retrieve the value of a variable within the context of a specific instance,raises an error if the variable is not found.
  - `get_instance_attribute`：traverses the environment stack, considering only scopes associated with the specified instance, and raises an error if the attribute is not found.
  - `do_sequence`:iterates through each operation, executes it using the `do()` function, stores the results, and prints the formatted output of each operation using the `format_output()`. The results of all operations are then returned as a list.
  - `get_localframe_instance_variable`:facilitates the retrieval of instance variable values by searching through the environment stack for the specified instance and variable names. If the variable is found, its value is returned; 
  otherwise, an error is raised.
  - `format_output`: to format the output of operations

- **Execution Functions**: 
  - `main()`: reads the LGL program from the file specified in the command-line arguments and executes it using the `do(envs,args)` function.
  - `do()`: serves as the interpreter's core, handling the evaluation of LGL expressions and the execution of corresponding operations, allowing the LGL program to be executed within the specified environment (envs).

Operation Functions are core for this exercise,the implementation process of each function will be explained in great detail.

## 1.1 Multiplication

The `do_multiplication` function is takes two parameters, a and b, 
and returns their product when invoked. 

## 1.2 Division

The `do_division` function is takes two parameters, a and b, checks that b is not zero and returns the quotient when invoked. 

## 1.3 Power

The `do_power` function takes two parameters, a (base) and b exponent, and returns the result of a raised to the power of b. 

## 1.4 Print

The `do_print` function takes a list of parameters and prints the result of the concatenation . The function doesn't explicitly return a value ,it prints to the console, and returns an empty string ''.

## 1.5 While loop
 `do_while()` function takes 4 parameters, namely : counter variable,comparison operator,value to which the counter variable is compared, statement to be executed in the body of the function.


## 1.6 Array
### 1.6.1 Creating a new array of fixed size
The `do_create_array()` takes one parameter `size`and  creates an empty array of the specified size

### 1.6.2 Getting the value at position i of an array
The `do_get_array_index` function takes two parameters: array and index.The body of the function retrieves the value at the specified index i of the array.

### 1.6.3 Setting the value at position i of an array to a new value
The `do_set_array_index`  function takes three parameters: array, index, and new_value. The body of the function sets the value at the specified index i of the array to the new value.


## 1.7 Dictionary
### 1.7.1 Creating a new dictionary

The`do_create_dict`  takes no parameters (an empty list []) and, when called, returns a new dictionary with the specified(0,2,4,..) number of key and value pairs in the .gsc file

### 1.7.2 Getting the value of a key

The `do_get_dict_key`function takes two parameters: a dictionary and the name of a key which is used to retrieve the value for that specific key stored in the dictionary.

### 1.7.3 Setting the value of a key to a new value

In `do_set_dict_key`function takes three parameters: 
a dictionary, a key, and a new value to set the value of the specified key in the dictionary to the new value.

### 1.7.4 Merging two dictionaries

The`do_merge_dict` function takes two parameters:dict1 and dict2 and combines the dictionaries obtained from the environment. If dict2 has a corresponding key in dict1 the value for the specified key is updated to the value in dict2 for the merged dictionary.The merged dictionary is then returned.We used the update operator instead of | for merging dictionaries as they have the same functionality, but | needs Python 3.9 or higher to run.

The result:
```
#1 Multiplication: the result of 1*2 is: 2
 
#2 Division: the result of 1/2 is: 0.5
 
#3 Power: the result of 1^2 is: 1
 
#4 While: 
---- While start ----- 
Loop Counter: 
0
Loop Counter: 
1
Loop Counter: 
2
Loop Counter: 
3
Loop Counter: 
4
Loop Counter: 
5
---- While end ----- 
 
#5 Arrays:
Create an empty array named myarray with two values:  [None, None]
Update myarray 2nd position with 2: [None, 2]
Update myarray 1st position with 1: [1, 2]
get myarray 2nd position value: 2
 
#5 Dictionaries:
Create an dictionary named mydict with two tuples: {'key1': 1, 'key2': 2}
Getting the value of key1 from mydict: 1
Setting the value of key1 from mydict to 100: {'key1': 100, 'key2': 2}
Create another dictionary named mydict1 with two tuples: {'key2': 1, 'key3': 2}
Merging two dictionaries mydict and mydict1 (implement the | operator of Python): {'key1': 100, 'key2': 1, 'key3': 2}
```

# 2. An Object System
To complete this exercise,we put our solution in `lgl_interpreter.py` file and `example_class.gsc` file.
## 2.1`lgl_interpreter.py`
  We define an object system according to the assignment define. 
### 2.1.1 `do_class`
This function is for defining a class. It takes a list of arguments , including class name, attributes, methods, and an optional parent class.
- First, we standardize our method format through `do_function`.All methods are in the format of ["funktion", params, body], other value like class name of attributes will be set like:
```
class_dict = {
              'attributes': attributes,
              'methods': {},
              'parent': inherits
              }
```
- Then we check whether there is a parent class. If the parent class's method_name is same as the the currently set method_name, it will automatically updated and the parent class methods will also append to the children class, the attributes of the parent class will be inherited.

### 2.1.2 `do_instantiation`
- This function is for instantiating instances based on a defined class, if there is parent class and the user input for init_args_parent is not empty, then this function will run the `_new` constructor of parent class.
And then if there is also a constructor inside the instance, it will also be runned accordingly.

### 2.1.3 `do_call_instance_method` 
- This function is to call the instance's method or constructor from the methods dictionary of the instance

### 2.1.4 `do_call_parent_methods` 
- This function is to call the method or constructor from the methods dictionary of the instance's parent class.

### 2.1.5 `get_instance_attribute`
- This function is for finding the attributes of an instance.

### 2.1.6 Helper Functions
- `replace_self_in_expr`：this is a  helper function for `do_call_instance_method` to replace occurrences of "self." with 
"instance_name.self_attribute." in expressions.
- `get_localframe_instance_variable`：this is a helper function for getting a variable from the local environment frame by instance_name.

## 2.2 `example_class.gsc` 
In this file, we define classes, instantiate objects, and then perform method calls on those objects.
- We define three classes:a "Shape" class with `_new` and `_density` methods,a "Square" class that inherits from "Shape" with `_new` and `_area` methods.
a "Circle" class that inherits from "Shape" with `_new` and `_area` methods.
- Creating a new Square object named "square" with side=3 and name='sq' and a new Circle object named "circle" with radius=2 and name='ci' by using both the constructors of their class and parent class
- Calling instance `_area` method of the `square` object and the `_area` method of the `circle` object.
- Calculating the sum of the densities of the two objects using their parent class `_density` methods.

- Result:
```
| Function Name | Num. of calls | Total Time (ms)  |  Average Time (ms)  |
|---------------+----------------+-------------------+----------------------|
| shape_new     |       2       |      0.376       |        0.188        |
| square_new    |       1       |      0.706       |        0.706        |
| circle_new    |       1       |      0.358       |        0.358        |
| square_area   |       1       |      0.130       |        0.130        |
| circle_area   |       1       |      0.135       |        0.135        |
| shape_density |       2       |      0.236       |        0.118        |
```
# 3. Tracing
This exercise involves three files, they are `lgl_interpreter.py`,`example_trace.gsc` and `reporting.py`.
- `lgl_interpreter.py`is used to parse `example_trace.gsc`, execute the defined function calls, and log each traced function call to a log file when tracing is enabled.Tracing is achieved by adding a decorator trace to specified function calls. When enabled, it records the start and end timestamps of functions and writes this information to a CSV-formatted log file.
- `example_trace.gsc`serves as a test for the tracing capabilities of the interpreter. It defines two function calls: `add_cubes` and `get_cube_power`.
- `reporting.py` is used to parse the trace log and generating a report. It reads the log file, calculates the number of calls,total execution time and average execution time for each traced function, and prints this information in tabular form.

Now we are going to explain our solution detailly.
## 3.1 `lgl_interpreter.py`
- Import modules and define global variables. At first, importing necessary module.Notably, `csv` for handing CSV files and `datetime` for managing dates and times. Then defining a global dictionary to hold the function call IDs.
- Define a trace decorator 
  - 1) Defining a decorator called `trace` used for tracking function calls.This decorator takes a function(`func`) as an argument. 
  - 2) It defines an inner function `wrapper_trace` thar will be used to wrap the original function.
  - 3) `wrapper_trace` takes any number of positional and keyword arguments (*args and **kwargs).It extracts the function name from the second argument and generates a random call_id.
  - 4) The decorator then checks if the function should be traced based on whether its name is in `TRACED_FUNCTIONS`.If the function is in `TRACED_FUNCTIONS`, it logs the start of the function call to the trace file, then executes the original function (func) and captures its result. If tracing is enabled, it logs the end of the function call to the trace file.
  - 5) If the function is not in TRACED_FUNCTIONS, it directly executes the original function without tracing.
  - 6) The name and docstring of the `wrapper_trace` function are set to match the original function.
- Initialization of Trace File. If tracing is enabled, it opens the trace file in write mode, initializes a CSV writer, and writes the header row.
- Decorate functions with `@trace` decorator
## 3.2 `example_trace.gsc`
In the file, defining two functions `get_cube_power`and `add_cubes`, then calls the`add_cubes` function.

```
| Function Name  | Num. of calls | Total Time (ms)  |  Average Time (ms)  |
|----------------+----------------+-------------------+-------------------|
| get_cube_power |       2       |      0.405       |        0.203        |
| add_cubes      |       1       |      1.005       |        1.005        |
```
## 3.3 `reporting.py`
- `parse_log()`:parses the trace log file, calculating the number of calls, total time, and average time for each function.
- `print_report()`:prints a formatted report table based on the aggregated data.
- Command-line usage:The script checks if it's executed from the command line with the correct number of arguments. It takes the trace file name as a command-line argument.
- Execution: When run from the command line, it reads the specified trace log file, parses it, aggregates the data, and prints a report table.


