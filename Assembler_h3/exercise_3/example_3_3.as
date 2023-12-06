ldc R0 0  #base address
ldc R1 5  #length of an array

# Create a new array for reversing
ldc R2 @array
loop:
    str R0 R2
    ldc R3 1
    add R0 R3
    add R2 R3
    cpy R3 R1
    sub R3 R0
    bne R3 @loop

# redirect to the start location for printing
sub R2 R0

# Print the created array
ldc R0 0  
print_loop:
    cpy R3 R2            
    add R3 R0          
    prm R3                 
    inc R0
    cpy R3 R1
    sub R3 R0
    bne R3 @print_loop

    cpy R3 R1
    add R3 R2
    dec R3  

# Strat reversing the array
loop_reverse:

    ldc R0 0   #pointer
    swp R2 R3  # Swap the pointer
    ldr R0 R2  #temporary pointer_1 for front bit
    ldr R1 R3  #temporary pointer_2 for back bit

    str R1 R2  #store back value to the front position
    str R0 R3  #store front value to the back position

    swp R2 R3  # Swap back the pointer
    inc R2  # front pointer move forward      
    dec R3  # back pointer move backward

    cpy R0 R3 #check whether back pointer is still behind front pointer
    sub R0 R2

    inc R0  # this step takes care of even length strings when the diff of front and back pointers is -1
    beq R0 @verification
    dec R0
    bne R0 @loop_reverse #if the back position are larger than the front postion

# Verification that the swap was actually made
verification:
ldc R0 @array
ldc R1 5
loop3:
prm R0
inc R0
dec R1
bne R1 @loop3

hlt
.data
array: 10