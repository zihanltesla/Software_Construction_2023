# Increment value in a register
ldc R0 7
prr R0
inc R0      #increase the value of R0 by one which will be 8
prr R0
ldc R1 10
prr R1
dec R1      #decrease the value of R1 by one which will be 9
prr R1
hlt
