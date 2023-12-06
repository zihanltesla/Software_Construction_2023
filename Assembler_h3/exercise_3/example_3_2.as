# Swap values in a register
ldc R0 7   # Initialize first register with value of 7
prr R0
ldc R1 10  # Initialize second register with value of 10
prr R1
swp R0 R1  # Swap the two registers' value
prr R0      
prr R1
hlt
