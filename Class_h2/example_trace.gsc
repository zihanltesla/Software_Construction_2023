[
    "sequence",
    ["print","Step 1: Define get_cube_power function: ",
    ["set", "get_cube_power",
        ["function", ["x"],
            ["power", ["get", "x"], 3]
        ]
    ]],

    ["print","Step 2: Define add_cubes function: ",
    ["set", "add_cubes",
        ["function", ["a", "b"],
            ["addition", ["call_function", "get_cube_power", ["get","a"]], ["call_function", "get_cube_power", ["get","b"]]]
        ]
    ]],

    ["print","Step 3: Run add_cubes returns: ",["call_function", "add_cubes", 2, 2]]

]