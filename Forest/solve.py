import string
import math

SEC_VAL = ""
ALPHABEST = string.printable                        # The ALPHABEST contains all printable ASCII Characters
for i in ALPHABEST:                                 # We the loop on these characters to find our second value
    if ord(i) % 10 == 1:                            # If the ordinal of our character modulo 10 is == 1, we now we found a good value so we can break and use this character
        SEC_VAL = i         
        break

THIRD_VAL = ""
for i in ALPHABEST:                                 # Another loop in ALPHABEST to find our third value
    if math.sqrt(float(ord(i))) * 5.0 == 50.0:      # If the square root of our character as a double * 5.0 is == 50.0 we know we have a good value so we can break and use it.
        THIRD_VAL = i                               # We set THIRD_VAL to i
        break                                       # And we Break


FOURTH_VAL = ""                                     # Time for FOURTH VAL
for i in ALPHABEST:                                 # Another Loop into Every ASCII Printable Characters
    if ord(i) - 1 <= 0x71:                          # If the ordinal of our character -i <= 0x71 we found a good character and set our fourth value to it
        FOURTH_VAL = i                              # set FOURTH_VAL = i
        break                                       # break

def FLIP(value):                                    # Here i defined a function to turn hexadecimal characters into ASCII a little bit quicker
    return bytes.fromhex(value).decode("ASCII")

FLAG = "A"* 13                                      # Our flag should contain 13 characters this is the size we deduced while reversing our program
LFLAG = list(FLAG)                                  # We make a list of our flag to modify each character more easily

LFLAG[0] = 'r'                                      # We know the first character is 
LFLAG[1] = SEC_VAL                                  # ASSIGN VALUE
LFLAG[2] = THIRD_VAL                                # ASSIGN VALUE
LFLAG[3] = FOURTH_VAL                               # ASSIGN VALUE
LFLAG[4] = FLIP("69")                               # Start Flipping hex to str
LFLAG[5] = FLIP("64")                               # ...
LFLAG[6] = FLIP("69")                               # ...
LFLAG[7] = FLIP("6e")                               # ...
LFLAG[8] = FLIP("67")
LFLAG[9] = FLIP("68")
LFLAG[10] = FLIP("6f")
LFLAG[11] = FLIP("6f")
LFLAG[12] = FLIP("64")
print(''.join(LFLAG), end='')
