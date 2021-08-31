# Forest
Forest is a Reverse Engineering challenge available at the following link : `https://crackmes.one/crackme/60f31f1d33c5d42814fb3381`.

It was made by [MKesenHeimer](https://crackmes.one/user/MKesenheimer), and to me it looks like a pretty easy challenge.

![image](https://user-images.githubusercontent.com/61102077/131456805-29d3d8c2-99ec-4784-8e8f-5a968a5e53e1.png)

## Let's Start Reversing
You can download the `crackme` and we're ready to roll.

### File Informations
We're going to check first what type of file we're dealing with and what security are enabled.
```bash
$ file forest
forest: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=3cec36018b4f8638a3f4c1156b074988c0227980, for GNU/Linux 4.4.0, not stripped
```

You can see it's a `64 Bit` Binary and it hasn't been stripped of it's `symbols`, this going to make are analysis a lot more easier, it also uses `ld-linux-x86-64.so.2.` as interpreter.



We're also going to use `checksec` on our file, we're not doing any binary exploitation, but it's always a good idea to check for securities enabled on a binary before starting to analyze it.
```bash
$ checksec ./forest
[*] '/home/spacek9/CrackMe/Forest/forest'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

```

### Let's start reversing
Okay so we're now ready, we are going to use `GDB` with the plugin `PWNDBG` or `GEF` if you prefer, to try and understand our program code, which will be assembly.

*Note that we're doing reverse engineering, for this reason we'll avoid using any decompilers and will stick to disassemblers*.
```bash
$ gdb ./forest
pwndbg> info functions
pwndbg> disass main
```

Alright we first take a look at our program functions with the command `info functions`, we then found a single function that looks interesting to us `main`.
We then disassemble this function using the `disass main` function.

Let's take a look at our code... I'm going to try and comment everyline with what actually happens.
```asm
Dump of assembler code for function main:
   0x0000000000001080 <+0>:     sub    rsp,0x28                           ; We make place on our stack
   0x0000000000001084 <+4>:     lea    rdi,[rip+0xf7d]        # 0x2008    ; We move a string stored at [rip+0xf7d] or 0x2008 if you prefer into rdi
   0x000000000000108b <+11>:    mov    rax,QWORD PTR fs:0x28              ; This is a stack protection
   0x0000000000001094 <+20>:    mov    QWORD PTR [rsp+0x18],rax           ; Still the stack protection
   0x0000000000001099 <+25>:    xor    eax,eax                            ; Still the stack protection
   0x000000000000109b <+27>:    call   0x1030 <puts@plt>                  ; Print the value we moved into rdi
   0x00000000000010a0 <+32>:    lea    rdi,[rip+0xfee]        # 0x2095    ; Move a string stored at [rip+0xfee] or 0x2095 if you prefer into rdi
   0x00000000000010a7 <+39>:    xor    eax,eax                            ; We clear the value into eax, to store our next function call return value
   0x00000000000010a9 <+41>:    call   0x1050 <printf@plt>                ; Call to printf with the string we just moved into rdi
   0x00000000000010ae <+46>:    xor    eax,eax                            ; Clear the return value of our printf function call out of eax
   0x00000000000010b0 <+48>:    lea    rsi,[rsp+0xa]                      ; Move our String Buffer into rsi
   0x00000000000010b5 <+53>:    lea    rdi,[rip+0xff0]        # 0x20ac    ; Move the format specifier located at [rip+0xff0] or 0x20ac if you prefer into rdi
   0x00000000000010bc <+60>:    call   0x1060 <__isoc99_scanf@plt>        ; We call scanf with rsi and rdi as arguments (rsi == our buffer && rdi == format specifier)
   0x00000000000010c1 <+65>:    cmp    BYTE PTR [rsp+0xa],0x72            ; Compare the first character of at [rsp+0xa] with `r` (0x72 or 114)
   0x00000000000010c6 <+70>:    jne    0x10dc <main+92>                   ; If the values are not equal we jump end and the program with fail message
   0x00000000000010c8 <+72>:    movsx  ax,BYTE PTR [rsp+0xb]              ; We move the second value of our string into ax
   0x00000000000010ce <+78>:    mov    edx,0xa                            ; We move 0xa (10) into edx
   0x00000000000010d3 <+83>:    idiv   dl                                 ; We divide ax with dl
   0x00000000000010d5 <+85>:    movzx  eax,ah                             ; We move the remainder into eax
   0x00000000000010d8 <+88>:    sub    al,0x1                             ; We compare the remainder of ([rsp+0xb] % 10 == 1)
   0x00000000000010da <+90>:    je     0x1105 <main+133>                  ; If the remainder was one, we jump to the next set of instruction in the program, else we fail.
   0x00000000000010dc <+92>:    lea    rdi,[rip+0xf85]        # 0x2068    ; This is the Fail string that we move into rdi
   0x00000000000010e3 <+99>:    xor    eax,eax                            ; Clear eax for return value
   0x00000000000010e5 <+101>:   call   0x1050 <printf@plt>                ; Call printf with the string we just moved into rdi
   0x00000000000010ea <+106>:   mov    rax,QWORD PTR [rsp+0x18]           ; Stack Canary   
   0x00000000000010ef <+111>:   sub    rax,QWORD PTR fs:0x28              ; Stack Canary
   0x00000000000010f8 <+120>:   jne    0x1199 <main+281>                  ; Stack Canary Jump
   0x00000000000010fe <+126>:   xor    eax,eax                            ; Stack Canary
   0x0000000000001100 <+128>:   add    rsp,0x28                           ; Adjust stack
   0x0000000000001104 <+132>:   ret                                       ; Program end
   0x0000000000001105 <+133>:   movsx  eax,BYTE PTR [rsp+0xc]             ; Move the third character of our input into eax
   0x000000000000110a <+138>:   pxor   xmm0,xmm0                          ; We call a pxor, why pxor ? Because MMX Instruction Set uses P as a prefix before each of his operations.
   0x000000000000110e <+142>:   cvtsi2sd xmm0,eax                         ; cvtsi2sd stands for convert scalar integer to scalar double, we basically transform a decimal into a double usin MMX Floating Point Registers.
   0x0000000000001112 <+146>:   call   0x1070 <sqrt@plt>                  ; We call square root on our third character double value
   0x0000000000001117 <+151>:   mulsd  xmm0,QWORD PTR [rip+0xf99]        # 0x20b8   ; multiply xmm0 with value at [rip+0xf99]
   0x000000000000111f <+159>:   ucomisd xmm0,QWORD PTR [rip+0xf99]        # 0x20c0  ; ucomisd is defined to compare two doubles. It will indicate that they are one of four things: unordered, equal, greater than or less than. 
   0x0000000000001127 <+167>:   jp     0x10dc <main+92>                   ; Fail the program is Parity flag was enabled by the last instruction
   0x0000000000001129 <+169>:   jne    0x10dc <main+92>                   ; Fail the program if the result weren't equal
   0x000000000000112b <+171>:   movzx  eax,BYTE PTR [rsp+0xd]             ; Move the first character at [rsp+0xd] into eax and zero extend the rest
   0x0000000000001130 <+176>:   sub    eax,0x1                            ; substract our character by 0x1
   0x0000000000001133 <+179>:   cmp    al,0x71                            ; compare it to al this can be traducted to (rsp[0xd] - 1 <= 0x71)
   0x0000000000001135 <+181>:   ja     0x10dc <main+92>                   ; Fail the program if (rsp[0xd] -1 > 0x71)
   0x0000000000001137 <+183>:   cmp    BYTE PTR [rsp+0xe],0x69            ; Compare (rsp[0xe] with 0x69)
   0x000000000000113c <+188>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x000000000000113e <+190>:   cmp    BYTE PTR [rsp+0xf],0x64            ; Compare (rsp[0xf] with 0x64)
   0x0000000000001143 <+195>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x0000000000001145 <+197>:   cmp    BYTE PTR [rsp+0x10],0x69           ; Compare (rsp[0x10] with 0x69)
   0x000000000000114a <+202>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x000000000000114c <+204>:   cmp    BYTE PTR [rsp+0x11],0x6e           ; Compare (rsp[0x11] with 0x6e)
   0x0000000000001151 <+209>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x0000000000001153 <+211>:   cmp    BYTE PTR [rsp+0x12],0x67           ; Compare (rsp[0x12] with 0x67)
   0x0000000000001158 <+216>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x000000000000115a <+218>:   cmp    BYTE PTR [rsp+0x13],0x68           ; Compare (rsp[0x13] with 0x68)
   0x000000000000115f <+223>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x0000000000001165 <+229>:   cmp    BYTE PTR [rsp+0x14],0x6f           ; Compare (rsp[0x14] with 0x6f)
   0x000000000000116a <+234>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x0000000000001170 <+240>:   cmp    BYTE PTR [rsp+0x15],0x6f           ; Compare (rsp[0x15] with 0x6f)
   0x0000000000001175 <+245>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x000000000000117b <+251>:   cmp    BYTE PTR [rsp+0x16],0x64           ; Compare (rsp[0x16] with 0x64)
   0x0000000000001180 <+256>:   jne    0x10dc <main+92>                   ; If they are not equal, FAIL THE PROGRAM
   0x0000000000001186 <+262>:   lea    rdi,[rip+0xeab]        # 0x2038    ; MOVE SUCCESS STRING INTO RDI
   0x000000000000118d <+269>:   xor    eax,eax                            ; Clear return value for following function call
   0x000000000000118f <+271>:   call   0x1050 <printf@plt>                ; Print our Win Message
   0x0000000000001194 <+276>:   jmp    0x10ea <main+106>                  ; Jump to main+106 which is our program end
   0x0000000000001199 <+281>:   call   0x1040 <__stack_chk_fail@plt>
End of assembler dump.

```

Okay so take your time to read what each instruction does, if you do not understand an instruction go download the Intel Manual and search for that instruction inside the manual.
If you understand what the program is doing, you should not have any problem reversing it.

### Let's write a script and win this challenge
I wrote the following script while making the challenge and it worked pretty fine to me, if you say it's ugly i totally understand i was making it for efficiency not for beauty...
Anyway here's the code i made to win that challenge :

```py
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


# ./forest <<<$(python3 solve.py)
```

And that's it i hope you were able to figure out how the program works, if you did not keep reading the assembly dump with all the comments i made.
