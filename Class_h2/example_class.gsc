[
    "sequence",
    ["print", "------- Class Define -------- "],
    ["print", "Step 1: Define a Shape class: ",
    [
        "set", "Shape",
        [
            "class",
            "Shape",
            [],
            [
                ["_new", ["name"], [["set", "self.name", "name"]]],
                ["_density", ["weight"],  ["division", ["get","weight"],"self.area"]]
            ]
        ]
    ]
    ],
    ["print", "Step 2: Define a Square class: ",
    [
        "set", "Square",
        [
            "class",
            "Square",
            [], 
            [
                ["_new", ["side"], [["set", "self.side", "side"]]],
                ["_area", [], [["set", "self.area",["mulplication", "self.side","self.side" ]]]]
            ],
            "Shape"
        ]
    ]
    ],
    ["print", "Step 3: Define a Circle class: ",
    [
        "set", "Circle",
        [
            "class",
            "Circle",
            [],
            [
                ["_new", ["radius"], [["set", "self.radius", "radius"]]],
                ["_area", [], [["set", "self.area",["mulplication", 3.1415926,["mulplication", "self.radius","self.radius"] ]]]]
            ],
            "Shape"
        ]
    ]
    ],
    ["print", "------- Object Instantiation -------- "],

    ["print","Step 4. Create a new Square object with side=3 and name=‘sq’:",["instantiation", "square", "Square",[["sq"]], [[3]]]],
    ["print","Step 5: Create a new Circle object with radius=2 and name=‘ci’:",["instantiation", "circle", "Circle",[["ci"]], [[2]]]],

    ["print", "------- Instance Methods Call -------- "],
    ["print","Step 6: We call the _area function of Object1 it returns:",["call_instance_method", "square","_area","", [],[]]],
    ["print","Step 7: We call the _area function of Object2 it returns:",["call_instance_method", "circle", "_area","", [],[]]],
    ["print","Step 8: The sum of the densities of the two objects is :", ["addition", ["call_parent_methods","Shape","_density", "square",[5]], ["call_parent_methods","Shape","_density", "circle",[5]]]]
]
