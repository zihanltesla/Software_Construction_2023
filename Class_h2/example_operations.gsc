[
    "sequence",
    ["print","#1 Multiplication: the result of 1*2 is:",["mulplication", 1, 2]],
    ["print", " "],

    ["print","#2 Division: the result of 1/2 is:",["division", 1, 2]],
    ["print", " "],

    ["print","#3 Power: the result of 1^2 is:",["power", 1,2]],
    ["print", " "],

    ["set", "counter",0],
    ["print", "#4 While: "],
    ["print", "---- While start ----- "],
    ["while",["get","counter"],"lteq",5,
            [
                "sequence",
                ["print", "Loop Counter: "],
                ["print",["get", "counter"]],
                ["set","counter",["addition",["get", "counter"],1]]
            ]
    ],
    ["print", "---- While end ----- "],
    ["print", " "],

    ["print", "#5 Arrays:"],
    ["print","Create an empty array named myarray with two values: ",["set", "myarray",["create_array", 2]]],
    ["print", "Update myarray 2nd position with 2:",["set_array_index", ["get", "myarray"], 1,2]],
    ["print", "Update myarray 1st position with 1:",["set_array_index", ["get", "myarray"], 0,1]],
    ["print", "get myarray 2nd position value:",["get_array_index", ["get", "myarray"], 1]],
    ["print", " "],

    ["print", "#5 Dictionaries:"],
    ["print", "Create an dictionary named mydict with two tuples:",["set", "mydict",["create_dict","key1",1,"key2",2]]],
    ["print", "Getting the value of key1 from mydict:",["get_dict_key",["get", "mydict"],"key1"]],
    ["print", "Setting the value of key1 from mydict to 100:",["set_dict_key",["get", "mydict"],"key1",100]],
    ["print", "Create another dictionary named mydict1 with two tuples:",["set", "mydict1",["create_dict","key2",1,"key3",2]]],
    ["print", "Merging two dictionaries mydict and mydict1 (implement the | operator of Python):",["merge_dict",["get", "mydict"],["get", "mydict1"]]]
]
