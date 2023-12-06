ldc R0 2
ldc R1 1
ldc R2 1

#copy the value of R0 to R3
str R0 R2                  #change the memory at location 1 to 3
prm R2                     # check whether change successfully
ldr R3 R1                  # set the value at memory location1 to regiser 3

print: 
    prr R3 
    sub R3 R1               
    bne R3 @print          #if R3 not equal to 0 continue
hlt