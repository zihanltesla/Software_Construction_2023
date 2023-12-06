ldc R1 1
ldc R2 1
cpy R3 R2    #R3=1 copy the value of R2 to R3    

print: 
    prr R3   
    sub R3 R1               
    beq R3 @print
hlt