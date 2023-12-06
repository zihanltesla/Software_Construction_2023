import json
import pprint
import random
import os
import argparse
import csv
import datetime


# ----------Global Variables---------------
TRACED_FUNCTIONS = ['get_cube_power', 'add_cubes','square','circle','Shape']
tracing_enabled = False
trace_file = None

# ----------Implementatioin of 3rd question---------------
# This is a decorator realized from chapter 9 which can be used to wrap around the function that executes other functions
def trace(func):
    """
    A decorator for tracing the function

    Decorate:
            1. If the tracing function is "do_call_instance_method":
                Which means we want to see the instance_name as well as the runned methods
                so we set the name in log as "{instance_name}{method_name}"

            2. If the tracing function is "do_instantiation":
                We want to trace whcih instance is constructed by which class, and with
                which name, so we set as {instance_name}_{class_name}_instantiation
            3. If the tracing function is "do_addition":
                We set the tracing name as the function name itself.

    call_id: For the tracing id we combine the timestamp and random number from 1000-9999 to 
            ensure the uniqueness.

    """

    def wrapper_trace(*args, **kwargs):
        global tracing_enabled, trace_file
        func_name = args[1][0]
        func_name_log = func.__name__

        # For decorating different functions logging name appear in the .log file
        if func_name_log == "do_call_instance_method" and len(args) > 1:
            instance_name = args[1][0]
            method_name = args[1][1]
            func_name_log = f"{instance_name}{method_name}"

        elif func_name_log == "do_call_parent_methods" and len(args) > 1:
            class_name = args[1][0]
            class_name=class_name.lower()
            method_name = args[1][1]
            func_name_log = f"{class_name}{method_name}"

        elif func_name_log == "do_call_function" and len(args) > 1:
            function_name = args[1][0]
            func_name_log = f"{function_name }"

        # Create a unique call ID using a combination of a timestamp and a random number
        timestamp = datetime.datetime.now().strftime("%f")
        random_part = random.randint(10000, 99999)
        call_id = f"{timestamp}{random_part}"

        # Check if tracing is enabled and log the function call
        if func_name in TRACED_FUNCTIONS:
            # Log start of the function call
            if tracing_enabled:
                with open(trace_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([call_id, func_name_log, 'start', datetime.datetime.now().isoformat()])

            # Execute the function
            result = func(*args, **kwargs)

            # Log end of the function call
            if tracing_enabled:
                with open(trace_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([call_id, func_name_log, 'stop', datetime.datetime.now().isoformat()])

        else:
            # If not a traced function, just execute it
            result = func(*args, **kwargs)

        return result

    wrapper_trace.__name__ = func.__name__
    wrapper_trace.__doc__ = func.__doc__
    return wrapper_trace



# ---from funcs-demo in session 4 ---
def do_function(envs,args):
    """
    Args: [parameters, func_body]

    Output: ["function",params,body]

    """
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["function",params,body]

# Call function
@trace
def do_call_function(envs,args):

    """
    This function is to call the operation with "function", in our case, we have achieved the same
    functionality inside instance by using do_call_instance_method, if we want to set a function inside
    .gsc file we can use it.

    """

    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs,arg) for arg in arguments]
    func = envs_get(envs,name)
    assert isinstance(func,list)
    assert func[0] == "function"
    func_params = func[1]
    assert len(func_params) == len(values)
    local_frame = dict(zip(func_params,values))
    envs.append(local_frame)
    body = func[2]
    result = do(envs,body)
    envs.pop()
    return result

def envs_get(envs, name):
    assert isinstance(name, str), f"Expected name to be a string, got {type(name)}"
    for e in reversed(envs):
        if name in e:
            return e[name]
    assert False, f"Unknown variable name {name}"

def envs_set(envs,name,value):
    assert isinstance(name,str)
    envs[-1][name] = value

def do_set(envs, args):

    """
    This function is to set value the target. of the target the attribute of the instance,
    it will find the instance first and set the value inside the attributes dictionary.

    Args: [target, value]

    """
    assert len(args) == 2
    assert isinstance(args[0], str)
    target = args[0]

    # Check whether is to set a value to the variable，like 'mySquare.area'
    if '.self_attribute.' in target:
        instance_name, attribute_name = target.split('.self_attribute.', 1) 
        # If the value we want to set is a list of formats, caculated first
        if isinstance(args[1], list):
            value = do(envs, args[1])

        # If only one value, get it directly
        else:
            # get the value of the instance value directly from local frame
            value = get_localframe_instance_variable(envs, instance_name, args[1])

        # Find the instance and set the value inside.
        instance_dict = envs_get(envs, instance_name)

        # Because we set the attriibute of the instance at the 3rd list
        attributes_dict = instance_dict["attributes"]
        attributes_dict[attribute_name] = value
    else:
        # If not to set the value to the atttributes to the instance 
        # just write the value to the envs
        value = do(envs, args[1])
        envs_set(envs, target, value)
    return value

#do_get
def do_get(envs, args):

    """
    This function is to get value from the target from the environment.

    Args: [target]
    
    """
    assert len(args) > 0, "Expected at least one argument for 'get'"

    # if the input number is only one then get the value from the envs directly
    if len(args) == 1 and isinstance(args[0], str):
        return envs_get(envs, args[0])
    
    # If the input number is multiple, in our case we proposed it as a function call
    elif len(args) > 1:
        func_name = args[0]
        func_args = args[1]

        # to check the functoin name is a string, and the args is list[]
        assert isinstance(func_name, str), "Function name must be a string"
        assert isinstance(func_args, list), "Function arguments must be a list"
        # print(func_args)

        # Recursive call the do function for the arguments
        evaluated_args = [do(envs, arg) for arg in func_args]

        # Get the function defination from envs
        func_def = envs_get(envs, func_name)
        assert isinstance(func_def, list) and func_def[0] == "function", f"'{func_name}' is not a function"
        
        # Get the parameters and function body from the function
        _, func_params, func_body = func_def
        assert len(func_params) == len(evaluated_args), "Incorrect number of arguments provided for function"

        # To create a local frame for usage for function in the future
        local_env = {"function": func_name, **dict(zip(func_params, evaluated_args))}
        envs.append(local_env)

        result = do(envs, func_body)
        envs.pop()
        return result
    else:
        raise ValueError("Incorrect usage of 'get'")


# ----------Implementatioin of 1st question---------------

# 1.1 Multiplication
def do_mulplication(envs, args):
    assert len(args) == 2  # assert there are two arguments
    left_value = do(envs, args[0])  # compute first args
    right_value = do(envs, args[1])  # compute 2nd
    return left_value * right_value  # return results

# 1.2 Division
def do_division(envs, args):
    assert len(args) == 2  # assert there are two arguments
    left_value = do(envs, args[0])  # compute the first argument
    right_value = do(envs, args[1])  # compute the second argument
    assert right_value != 0, "Division by zero error"  # check for division by zero
    return left_value / right_value  # return the result

# 1.3 Power
def do_power(envs, args):
    assert len(args) == 2  # assert there are two arguments
    base_value = do(envs, args[0])  # compute the base
    exponent_value = do(envs, args[1])  # compute the exponent
    return base_value ** exponent_value  # return the result

# 2. Print
def do_print(env, args):
    args = [do(env, a) for a in args]
    print(*args)
    return ''

# Addition(help function)
@trace
def do_addition(envs, args):
    assert len(args) == 2  # assert there are two arguments
    left_value = do(envs, args[0])  # compute first args
    right_value = do(envs, args[1])  # compute 2nd
    return left_value + right_value  # return results

# 3. While
def do_while(envs, args):
    # Function executes a statement in its body as long as condition in the counter remains TRUE
    # Input: [counter_var,comparison_operator,counter_comparison_val, statement]
    assert len(args) == 4
    assert isinstance(args[1],str) #comparator
    assert isinstance(args[2],int)
    assert isinstance(args[3],list)
    if args[1] == "eq":
        while do(envs, args[0]) == args[2]:
            do(envs, args[3])
    elif args[1] == "neq":
        while do(envs, args[0]) != args[2]:
            do(envs, args[3])
    elif args[1] == "gteq":
        while do(envs, args[0]) >= args[2]:
            do(envs, args[3])
    elif args[1] == "lteq":
        while do(envs, args[0]) <= args[2]:
            do(envs, args[3])
    elif args[1] == "lt":
        while do(envs, args[0]) < args[2]:
            do(envs, args[3])
    elif args[1] == "gt":
        while do(envs, args[0]) > args[2]:
            do(envs, args[3])
    else:
        assert False, f'Invalid comparison input: Unknown operator "{args[1]}"'


# 4. Arrays

# 4.1 Creating a new array of fixed size
def do_create_array(envs, args):
    assert len(args) == 1, 'Invalid Input, Correct Usage Syntax: ["create_array", size]'
    size = do(envs, args[0])
    assert isinstance(size, int) and size > 0, 'Array size must be a positive integer'
    return [None] * size  # Create a new array with specified size, initially filled with None

# 4.2 Getting the value at position i of an array
def do_get_array_index(envs, args):
    assert len(args) == 2, 'Invalid Input, Correct Usage Syntax: ["get_array_index", array, index]'
    array = do(envs, args[0]) #actual array being assigned to the variable
    index = do(envs, args[1])
    assert isinstance(array, list) and isinstance(index, int), 'Error: Invalid arguments received'
    assert 0 <= index < len(array), 'Index out of bounds'
    return array[index]  # Get value at specified index in the array

# 4.3 Setting the value at position i of an array to a new value
def do_set_array_index(envs, args):
    assert len(args) == 3, 'Invalid Input, Correct Usage Syntax: ["set_array_index", array, index, value]'
    array = do(envs, args[0])
    index = do(envs, args[1])
    value = do(envs, args[2])
    assert isinstance(array, list) and isinstance(index, int), 'Error: Invalid arguments received'
    assert 0 <= index < len(array), 'Error: Index out of bounds'
    array[index] = value  # Set value at specified index in the array
    return array  # Returns the modified array


# 5. Dictionaries
# 5.1 Creating a new dictionary
def do_create_dict(envs, args):
    assert len(args)%2 == 0,"Dictionary creation requires an even number of arguments ie key value pairs"
    new_dic = {}
    for i in range(0,len(args),2):
        key = do(envs,args[i])
        value = do(envs,args[i+1])
        new_dic[key] = value
    return new_dic

# 5.2 Getting the value of a key
def do_get_dict_key(envs, args):
    assert len(args) == 2, 'Invalid Input, Correct Usage Syntax: ["get_dict_key", dict, key]'
    dictionary = do(envs, args[0])
    key = do(envs, args[1])
    assert isinstance(dictionary, dict), 'Error: Invalid arguments'
    return dictionary.get(key, None)  # Returns None if key is not present

# 5.3 Setting the value of a key to a new value
def do_set_dict_key(envs, args):
    assert len(args) == 3, 'Invalid Input, Correct Usage Syntax: ["set_dict_key", dict, key, value]'
    dictionary = do(envs, args[0])
    key = do(envs, args[1])
    value = do(envs, args[2])
    assert isinstance(dictionary, dict), 'Error: Invalid arguments'
    dictionary[key] = value
    return dictionary  # Optionally return the modified dictionary

# 5.4 Merging two dictionaries (i.e, implement the | operator of Python)
def do_merge_dict(envs, args):
    assert len(args) == 2, 'Invalid Input, Correct Usage Syntax: ["merge_dict", "dict1", "dict2"]'
    dict1 = do(envs, args[0])  # Retrieve the first dictionary
    dict2 = do(envs, args[1])  # Retrieve the second dictionary
    assert isinstance(dict1, dict), f"First argument must be a dictionary, got {type(dict1)}"
    assert isinstance(dict2, dict), f"Second argument must be a dictionary, got {type(dict2)}"
    
    # Use the update() method to merge dict2 into dict1
    dict1.update(dict2)  #Update has same functionality as pipe(|), except | is only compatible with Python 3.9 upwards
    
    return dict1  # Return the updated dict1



# ----------Implementation of 2nd question---------------

# Define the classes
def do_class(envs, args):
    """
    Class definition

    Args:  ["class","classname",[class_attributes],
                [        
                    ["func_name1", ["func1_var"], [func1_body],
                    ["func_name2", ["func2_var"], [func2_body],
                                ...
                ],
            parent_class]

    Returns: 
            Create our class based on the parameters. 
            1. First, we standardize our method format through do_function.
               All methods are in the format of ["function", params, body], other value like class name
               of attributes will be set like:
                   class_dict = {
                                    'attributes': attributes,
                                    'methods': {},
                                    'parent': inherits
                                }
            2. Then we check whether there is a parent class.
               If the parent class's method_name is same as the the currently 
               set method_name, it will automatically updated and the parent class methods will
               also append to the children class, the attributes of the parent class 
               will be inherited.
        
        eg:
        {   'attributes': [],
            'methods': {'area': ['function',[],[['set','self.area',['mulplication',3.1415926,['mulplication', 'self.radius', 'self.radius']]]]],
                        'density': ['function',['weight'],['division', ['get', 'weight'], 'self.area']],
                        'new': ['function',['name', 'radius'],[['set', 'self.radius', 'radius'],['set', 'self.name', 'name']]]},
            'parent': 'Shape'} 
    """
    assert len(args) >= 3, "Usage: ['class', class_name, [attributes], [methods], optional(inherits)]"
    class_name, attributes, methods = args[:3]
    inherits = args[3] if len(args) > 3 else None

    # Define the format of the class in the envs.
    class_dict = {
        'attributes': attributes,
        'methods': {},
        'parent': inherits
    }
    
    for method in methods:
        func_name = method[0]
        func_args = method[1]
        func_body = method[2] if len(method) > 2 else []
        class_dict['methods'][func_name] = do_function(envs, [func_args, func_body])

    #If there is parent class, add the methods or update the methods.
    if inherits:
        parent_class = envs_get(envs, inherits)
        parent_attributes, parent_methods = parent_class['attributes'], parent_class['methods']
        
        # Combine attributes and methods with parent's if inheritance is present
        class_dict['attributes'] = list(set(attributes + parent_attributes))
        for method in parent_methods:
            if method not in class_dict['methods']:
                class_dict['methods'][method] = parent_methods[method]

    # Set the class in the environment
    envs_set(envs, class_name, class_dict)
    return class_dict


# Create a instance that is object instantiation
def do_instantiation(envs, args):
    """
    Object instantiation, automatically run the constructor '_new' inside the object,

    Args:  ["instance_name", "class_name","parent_class_name",[[parent_class_attributes]], [instance_attributes]]],
           ["instantiation", "square", "Square",[["sq"]], [[3]]]]
            
    Returns:
            example: {'type': 'instanz', 'class': 'Square', 'attributes': {'side': 3, 'name': 'sq'}}
    """
    
    assert len(args) >= 2, "Usage: ['instance', class_name, [init_args]]"
    instance_name, class_name = args[:2]
    init_args_parent = args[2] if len(args) > 2 else []
    init_args = args[3] if len(args) > 3 else []

    # Get the class from the defination of instance
    class_dict = envs_get(envs, class_name)
    parent_class_name = class_dict.get('parent')

    assert isinstance(class_dict, dict) and 'attributes' in class_dict, f"{class_name} is not a class"

    # Obtain the methods and atrribute from the class of this instance
    attributes = class_dict['attributes']
    methods_definitions = class_dict['methods']
    
    # Create the atrributes dict for the instance 
    instance_attributes = {attr: None for attr in attributes}
    instance_info = {'type': 'instanz', 'class': class_name, 'attributes': instance_attributes}

    # Save the defined instance to the envs
    envs_set(envs, instance_name, instance_info)
    constructor = methods_definitions.get('_new')

    #If there is a constructor inside will run it to set the attributes of the objects.
    if constructor:
        constructor_args = [instance_name, '_new', parent_class_name] + init_args + init_args_parent
        result = do_call_instance_method(envs, constructor_args)

    # Check whether there is a constructor of our instance, if there is one, run it.

    return instance_info


# Call the methods of instance
@trace
def do_call_instance_method(envs, args):
    """
    Find methods or constructor from class, and to run the method of 
    this instance from its class's methods dictionaries

    Args:  [instance_name, method_name, parent_class, [parent_class_method_args_list], [method_args_list]]
    e.g. ["square", "_new","Square",[["sq"]], [[3]]]
         ["circle", "_area","", [],[]]]
         
            
    Returns:
            add local frame {"instance": instance_name, **dict(zip(method_params, method_args))} to the environments dict list
            eg. {'instance': 'myCircle', 'weight': 5}
    """
    assert len(args) == 5, "Usage: [instance_name, method_name, parent_class, [parent_class_method_args_list], [method_args_list]]"
    instance_name, method_name,parent_class_name, method_args_list, method_args_parent_list = args
    method_args = method_args_list if isinstance(method_args_list, list) else [method_args_list]
    method_args_parent = method_args_parent_list if isinstance(method_args_list, list) else [method_args_list]

    #If the user set the parent class, like super.(), then we will run the constructor in the parent class
    if parent_class_name and method_args_parent != [[]]:
        class_dict_parent = envs_get(envs,parent_class_name)
        methods_definitions_parent = class_dict_parent['methods']
        parent_constructor = methods_definitions_parent.get('_new')
        if parent_constructor:
            constructor_args_parent = [parent_class_name, '_new', instance_name]  + method_args_parent
            result = do_call_parent_methods(envs, constructor_args_parent)
    
    # Obtain the instance dictionary from environment
    instance_dict = envs_get(envs, instance_name)
    
    # the class and attributes of instance 
    class_name = instance_dict['class']

    # get the information of instance methods
    class_info = envs_get(envs, class_name)
    class_methods = class_info['methods']
    
    method_def = class_methods.get(method_name)
    assert method_def is not None, f"Method {method_name} not found in class {class_name}"
    method_params, method_body = method_def[1], method_def[2]

    #Replace the self. to instance_name.
    new_method_body = [replace_self_in_expr(expr, instance_name) for expr in method_body]
    assert len(method_params) == len(method_args), "Incorrect number of arguments for method"

    # To create a local environment for next step function usage " {'instance': 'myCircle', 'weight': 5}"
    local_env = {"instance": instance_name, **dict(zip(method_params, method_args))}
    envs.append(local_env)
    result = do(envs, new_method_body)
    envs.pop()
    return result


@trace
def do_call_parent_methods(envs, args):
    """
    Find and run the constructor or methods from the parent class for the given instance.

    Args:
        args: [parent_class_name, method_name, instance_name, [method_args_list]]
        e.g. ["Shape","_density", "square",[5]]
            
    Returns:
        Result of the parent class method execution.
    """
    assert len(args) == 4, "Usage: [parent_class_name, method_name, method_args_list]"
    parent_class_name, method_name, instance_name, method_args_list = args
    method_args = method_args_list if isinstance(method_args_list, list) else [method_args_list]
    
    # Get the parent class information
    parent_class_info = envs_get(envs, parent_class_name)
    parent_class_methods = parent_class_info['methods']
    
    # Ensure the method exists
    method_def = parent_class_methods.get(method_name)
    assert method_def is not None, f"Method {method_name} not found in parent class {parent_class_name}"
    method_params, method_body = method_def[1], method_def[2]

    # Replace 'self' with 'instance_name' in the method body
    new_method_body = [replace_self_in_expr(expr, instance_name) for expr in method_body]
    assert len(method_params) == len(method_args), "Incorrect number of arguments for method"

    # Create a local environment with the instance name and method arguments
    local_env = {"instance": instance_name, **dict(zip(method_params, method_args))}
    envs.append(local_env)
    result = do(envs, new_method_body)
    envs.pop()
    
    return result



# Help function for "do_call_instance_method(envs, args)" to change "self.{}" to "instance_name.{}"
def replace_self_in_expr(expr, instance_name):
    # In our design, as we want to set the instances atrributes by using
    # self in .gsc file, but we need tranfer it to the format the .py can recognize here
    # That is, we change "self.{}" to "instance_name.self_attribute.{}", which is convinient for other functions
    # to find the corresponding instance attributes to set or get 
    if isinstance(expr, list):
        return [replace_self_in_expr(sub_expr, instance_name) for sub_expr in expr]
    elif isinstance(expr, str) and 'self.' in expr:
        return expr.replace('self.', f'{instance_name}.self_attribute.')
    else:
        return expr
    
def get_localframe_instance_variable(envs, instance_name, variable_name):
    """
    function for getting the local store data

    Args:  "instance_name", "variable_name"
            
    Returns:
            the variable name from the instance get from the local environment frame by instance_name
            eg. 1. first found {'instance': 'myCircle', 'weight': 5}
                2. find weight value 5 from ‘weight’
    """
    for scope in envs:
        if scope.get('instance') == instance_name:
            return scope.get(variable_name)
    raise ValueError(f"Variable {variable_name} not found for instance {instance_name}")

def get_instance_attribute(envs, instance_name, attribute_name):
    """
    function for findding the attributes of a instance

    Args:  "instance_name", "attribute_name"
            e.g. ["myCirle","name"]
            
    Returns:
            1. First find the instance from the environment
            2. Secondly get the attribute value from the dictionaries of instance
            eg. "ci"
    """
    for env in reversed(envs):
        instance_info = env.get(instance_name)
        if instance_info and instance_info.get('type') == 'instanz':
            attributes_dict = instance_info.get('attributes', {})
            if attribute_name in attributes_dict:
                return attributes_dict[attribute_name]
    raise ValueError(f"Attribute {attribute_name} not found for instance {instance_name}")

# do sequence
def do_sequence(envs, args):
    assert len(args) > 0
    for operation in args:
        result = do(envs, operation)
    return result


def do(envs, expr):
    """
    Function for processing different data type, basically copy from session4,
             but add some new supported datatypes.

    Args: Supported: interger, float, string, list
            
    Returns:
            1. For expression in int and float format it will directly return values themselves
            2. For string:
                2.1 If the string is a attributes of object found by '.self_attribute.',it will
                automatically find the value of it from the instance
                2.2 Otherwise directly return expression
            3. For list:
                3.1 If it is a list of list it will run all the operations sequently and automatically 
                    by every elements of every list inside
                3.2 If it is only one list it will check this list's elements by using recursion.
    """
    if isinstance(expr, int):
        return expr
    
    elif isinstance(expr, float):
        return expr
    
    elif isinstance(expr, str):
            # Check if the string is a reference to an instance's attribute by 
            # checking whether there is a ".self_attribute." in the expression we set before
            if '.self_attribute.' in expr:
                instance_name, attribute_name = expr.split('.self_attribute.', 1)  # Split on the first dot only
                return get_instance_attribute(envs, instance_name, attribute_name)
            else:
                return expr
                
    elif isinstance(expr, list):
        # Check if the first element is an operation
        if expr and isinstance(expr[0], str) and expr[0] in OPERATIONS:
            func = OPERATIONS[expr[0]]
            return func(envs, expr[1:])
        
        # If it's a list of expressions
        elif all(isinstance(e, list) for e in expr):
            result = [do(envs, e) for e in expr]
            return result[0] if isinstance(result, list) and len(result) == 1 else result
        
        else:
            raise ValueError(f"List elements are not valid operations: {expr}") 
        

OPERATIONS = {
    func_name.replace("do_",""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}

def main():
    """
    main function:
                    1. Add parser for slection of tracing function.(e.g. --trace file.log)
                    2. Create an empty environment list for the interpreter.
    """
    global tracing_enabled, trace_file
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='LGL Interpreter with optional tracing.')
    parser.add_argument('source_file', type=str, help='The LGL source file to interpret.')
    parser.add_argument('--trace', type=str, help='The file where the trace log should be written.', metavar='TRACE_FILE', default='')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Check if tracing is enabled and set the trace file
    if args.trace:
        tracing_enabled = True
        trace_file = args.trace
        # If the trace file already exists, remove it to start fresh
        if os.path.exists(trace_file):
            os.remove(trace_file)
        # Create a new trace file and write the header
        with open(trace_file, "w") as f:
            f.write("id,function_name,event,timestamp\n")
    
    # Load the program from the source file and execute
    with open(args.source_file, "r") as source_file:
        program = json.load(source_file)
    envs = [{}]
    result = do(envs, program)


if __name__ == "__main__":
    main()