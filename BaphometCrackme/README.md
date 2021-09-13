# Baphomet CrackMe
Baphomet is a easy cracking challenge provided by crackmes.one (i can't remember if it was from a CTF or Crackmes.one actually...), in this section we'll solve the challenge which is a Linux x64 ELF Executable.

```
                                                         ...
                                      s,                .                    .s
                                       ss,              . ..               .ss
                                       'SsSs,           ..  .           .sSsS'
                                       sSs'sSs,        .   .        .sSs'sSs
                                        sSs  'sSs,      ...      .sSs'  sSs
                                         sS,    'sSs,         .sSs'    .Ss
                                         'Ss       'sSs,   .sSs'       sS'
                                          sSs         ' .sSs'         sSs
                                           sSs       .sSs' ..,       sSs
                                            sS,   .sSs'  .  'sSs,   .Ss
                                            'Ss .Ss'     .     'sSs. ''
                                             sSs '       .        'sSs,
                                         .sS.'sSs        .        .. 'sSs,
                                      .sSs'    sS,     .....     .Ss    'sSs,
                                   .sSs'       'Ss       .       sS'       'sSs,
                                .sSs'           sSs      .      sSs           'sSs,
                             .sSs'____________________________ sSs ______________'sSs,
                          .sSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'.Ss SSSSSSSSSSSSSSSSSSSSSs,
                                                  ...         sS'
                                                   sSs       sSs
                                                    sSs     sSs
                                                     sS,   .Ss
                                                     'Ss   sS'
                                                      sSs sSs
                                                       sSsSs
                                                        sSs
                                                         s
         
 ```
 
## Strings
By using `strings` on the binary we can find some strings that the program will use eventually which are the following
```
- WELCOME, CHILD OF BAPHOMET                                                                                                                                  
- YOU REALLY THINK THAT SACRIFICE A GOAT IS ENOUGH TO JOIN OUR CULT ?                                                                                         
- MOUAHAHAHAHAH YOU MUST FIND THE WAY TO FREE BAPHOMET IF YOU WANT TO BECOME ONE OF HIS CHILDREN                                                              
- GOOD LUCK !                                                                                                                                                 
- TELL US YOUR NAME:                                                                                                                                          
- NOW, WHAT IS THE FORBIDDEN FORMULA ?: 
- Do you think you're a sinner or a saint?
- Do you even think you could see?
- Or would you rather step into my church 
- And go to Hell with me
- CONGRATULATION           
- When the sun turns black at noonday
- And terror flies at night
- When the winds cut like razors
- We shall write your name with blood
```

With strings i can deduce that there is high chance the binary hasn't been stripped from it's symbols, although we can just run `file` and it should tells us wether the binary as been sripped or not.

## Symbols
Let's check if the file has been stripped using the `file` utility
![image](https://user-images.githubusercontent.com/61102077/133049629-9468d490-9365-43c9-b328-b42d04800a38.png)
Like i was saying the file hasn't been stripeed

## GDB
Now we have pretty much all the information we need to start reversing this challenge we can open it in `GDB`.

Let's check the functions our program uses...

![image](https://user-images.githubusercontent.com/61102077/133049935-281ad91e-0aff-47cf-89ab-8028bc085828.png)

Alright we can see the function `main`, this is where we'll start reversing the program, let's `disass` main and you should have the following (the disassembly is quite large so i'm not gonna post the 1300 lines of assembly instructions in here...)
```asm
Dump of assembler code for function main:                                                                                                                   
   0x00000000000007ea <+0>:     push   rbp                                                                                                                       
   0x00000000000007eb <+1>:     mov    rbp,rsp                                                                                                              
   0x00000000000007ee <+4>:     push   rbx                                                                                                                  
   0x00000000000007ef <+5>:     sub    rsp,0x4c8                                                                                                            
   0x00000000000007f6 <+12>:    mov    DWORD PTR [rbp-0x4c4],edi                             ;argc                                                               
   0x00000000000007fc <+18>:    mov    QWORD PTR [rbp-0x4d0],rsi                             ;argv                                                               
   0x0000000000000803 <+25>:    mov    rax,QWORD PTR fs:0x28                                 ;stack canary                                                         
   0x000000000000080c <+34>:    mov    QWORD PTR [rbp-0x18],rax                              ;stack canary
   0x0000000000000810 <+38>:    xor    eax,eax                                               ;stack canary                                                  
   0x0000000000000812 <+40>:    lea    rdi,[rip+0x62f]        # 0xe48                        ;load string at address 0xe48 into rdi                     
   0x0000000000000819 <+47>:    call   0x670 <puts@plt>                                      ;print that string                         
   0x000000000000081e <+52>:    mov    DWORD PTR [rbp-0x4b0],0x0                             ;define a variable at rbp-0x4b0 and put 0 in it (32 bytes)    
   0x0000000000000828 <+62>:    mov    DWORD PTR [rbp-0x490],0x89                            ;define a variable at rbp-0x490 and put 0x89 in it (4 bytes)       
   0x0000000000000832 <+72>:    mov    DWORD PTR [rbp-0x48c],0xbb                            ;define a variable at rbp-0x48c and put 0xbb in it (4 bytes)
   0x000000000000083c <+82>:    mov    DWORD PTR [rbp-0x488],0x800                           ;define a variable at rbp-0x488 and put 0x800 in it (4 bytes)         
   0x0000000000000846 <+92>:    mov    DWORD PTR [rbp-0x484],0x0                             ;define a variable at rbp-0x484 and put 0x0 in it (4 bytes)   
   0x0000000000000850 <+102>:   mov    DWORD PTR [rbp-0x4ac],0x0                             ;define a variable at rbp-0x4ac and put 0x0 in it (4 bytes)     
   0x000000000000085a <+112>:   mov    DWORD PTR [rbp-0x4a8],0x0                             ;define a variable at rbp-0x4a8 and put 0x0 in it (4 bytes)         
   0x0000000000000864 <+122>:   lea    rdi,[rip+0xaec]        # 0x1357                       ;load string at 0x1357 into rdi                                
   0x000000000000086b <+129>:   call   0x670 <puts@plt>                                      ;print the string we just put into rdi                               
   0x0000000000000870 <+134>:   lea    rdi,[rip+0xb01]        # 0x1378                       ;load string at 0x1378 into rdi
   0x0000000000000877 <+141>:   call   0x670 <puts@plt>                                      ;print the string we just put into rdi        
   0x000000000000087c <+146>:   lea    rdi,[rip+0xb3d]        # 0x13c0                       ;load string at 0x13c0 into rdi                
   0x0000000000000883 <+153>:   call   0x670 <puts@plt>                                      ;print the string we just put into rdi                              
   0x0000000000000888 <+158>:   lea    rdi,[rip+0xb9c]        # 0x142b                       ;load string at 0x142b into rdi ()                       
   0x000000000000088f <+165>:   mov    eax,0x0                                               ;mov 0x0 into eax                             
   0x0000000000000894 <+170>:   call   0x6a0 <printf@plt>                                    ;call to printf with no format      
   0x0000000000000899 <+175>:   lea    rax,[rbp-0x170]                                       ;prepare our buffer for the scanf function call                     
   0x00000000000008a0 <+182>:   mov    rsi,rax                                               ;put our buffer that is currently in rax into rsi                
   0x00000000000008a3 <+185>:   lea    rdi,[rip+0xb95]        # 0x143f                       ;load string at 0x143f (%s) into rdi
   0x00000000000008aa <+192>:   mov    eax,0x0                                               ;mov 0x0 into eax
   0x00000000000008af <+197>:   call   0x6b0 <__isoc99_scanf@plt>                            ;get our input

```

Yet the program has been pretty simple, we just load some values and print them, we also declare a couple of variables the program will eventually need
```
[rbp-0x4c4] = argc
[rbp-0x4d0] = argv
[rbp-0x170] = ourInput
[rbp-0x4b0] = 0x0    
[rbp-0x490] = 0x89       
[rbp-0x48c] = 0xbb 
[rbp-0x488] = 0x800          
[rbp-0x484] = 0x0      
[rbp-0x4ac] = 0x0        
[rbp-0x4a8] = 0x0
```
Let's run the program and see in action the instructions we've just detailed
![image](https://user-images.githubusercontent.com/61102077/133056870-f6afaa60-83f7-4aca-a22b-a3edead3daed.png)

We can see all the data that's being print before our `scanf` call in this case i have input `test` to our program, then the program seems to do another `scanf` but this time it asks us `What is the Forbidden Formula ?`

Let's keep disassembling our code to understand much more what our program does, once again we'll go split by split because i don't want to detail 1300 asm instructions in a row for a reverse engineering challenge.
```asm
   0x00005555554008b4 <+202>:   mov    DWORD PTR [rbp-0x4b4],0x0              ;define a new variable at rbp-0x4b4 and put 0x0 in it
   0x00005555554008be <+212>:   jmp    0x555555400965 <main+379>              ;jump to the beginning of a loop that starts at 0x555555400965                   
   0x00005555554008c3 <+217>:   mov    eax,DWORD PTR [rbp-0x4b4]              ;mov our current loop iterator into eax
   0x00005555554008c9 <+223>:   cdqe                                          ;sign extend eax to rax                                
   0x00005555554008cb <+225>:   movzx  eax,BYTE PTR [rbp+rax*1-0x170]         ;[rbp+rax*1-0x170] contains an array and each element is 1 bytes in size, this instruction will take the first character of our input and put it into eax                                                     
   0x00005555554008d3 <+233>:   movsx  eax,al                                 ;mov the character in hex at al into eax                                                                                  
   0x00005555554008d6 <+236>:   mov    DWORD PTR [rbp-0x484],eax              ;mov the character into our [rbp-0x484] double word variable                       
   0x00005555554008dc <+242>:   mov    eax,DWORD PTR [rbp-0x484]              ;mov the character [rbp-0x484] into eax
   0x00005555554008e2 <+248>:   mov    DWORD PTR [rbp-0x4ac],eax              ;mov the character into rbp-0x4ac                                                   
   0x00005555554008e8 <+254>:   mov    DWORD PTR [rbp-0x4b0],0x0              ;mov 0x0 into rbp-0x4b0
   0x00005555554008f2 <+264>:   jmp    0x55555540091f <main+309>              ;start of another loop, so this is a loop inside a loop                      
   0x00005555554008f4 <+266>:   mov    eax,DWORD PTR [rbp-0x490]              ;loop first instruction, it move [rbp-0x490] (0x89) into eax, remember we have defined this variable at the beginning of the program                                                                                
   0x00005555554008fa <+272>:   imul   eax,DWORD PTR [rbp-0x4ac]              ;then we multiply [rbp-0x4ac] (0x00) with eax and store the value in EDX:EAX in this case we won't have to store anything in EDX, remember we have also declared rbp-0x4ac at the beginning of our program                 
   0x0000555555400901 <+279>:   mov    edx,eax                                ;mov our multiplication result into edx                  
   0x0000555555400903 <+281>:   mov    eax,DWORD PTR [rbp-0x48c]              ;mov [rbp-0x48c] (0xbb) into eax we have also declared this variable at the beginning                                    
   0x0000555555400909 <+287>:   add    eax,edx                                ;add edx (our imul result) with eax (0xbb)                                  
   0x000055555540090b <+289>:   cdq                                                                               
   0x000055555540090c <+290>:   idiv   DWORD PTR [rbp-0x488]                                                                                                
   0x0000555555400912 <+296>:   mov    DWORD PTR [rbp-0x4ac],edx
   0x0000555555400918 <+302>:   add    DWORD PTR [rbp-0x4b0],0x1
   0x000055555540091f <+309>:   mov    eax,DWORD PTR [rbp-0x4b4]            ;mov the value at rbp-0x4b4 which is our first loop iterator into eax
   0x0000555555400925 <+315>:   cdqe                                        ;sign extend eax to rax
   0x0000555555400927 <+317>:   movzx  eax,BYTE PTR [rbp+rax*1-0x170]       ;mov the first character of our array into eax and zero extend eax
   0x000055555540092f <+325>:   movsx  eax,al                               ;mov al into eax and sign extend it
   0x0000555555400932 <+328>:   add    eax,0x4a                             ;add 0x4a to our character
   0x0000555555400935 <+331>:   cmp    DWORD PTR [rbp-0x4b0],eax            ;so what happens here we check if our first character + 0x4a is equal to rbp-0x4b0 which is the current loop iterator (second loop) with eax, so we loop until i = (BYTE ourInputFirstCharacter + 0x4a)
   0x000055555540093b <+337>:   jl     0x5555554008f4 <main+266>            ;jump back inside the loop as long as rbp-0x4b0 is less than (BYTE ourInputFirstCharacter + 0x4a)
   0x000055555540093d <+339>:   mov    eax,DWORD PTR [rbp-0x4ac]
   0x0000555555400943 <+345>:   imul   edx,eax,0x29a
   0x0000555555400949 <+351>:   mov    eax,DWORD PTR [rbp-0x4ac]
   0x000055555540094f <+357>:   imul   eax,eax,0x29a
   0x0000555555400955 <+363>:   imul   eax,edx
   0x0000555555400958 <+366>:   add    DWORD PTR [rbp-0x4a8],eax
   0x000055555540095e <+372>:   add    DWORD PTR [rbp-0x4b4],0x1
   0x0000555555400965 <+379>:   mov    eax,DWORD PTR [rbp-0x4b4]          ;mov rbp-0x4b4 which is eq to 0 and is probably a loop counter
   0x000055555540096b <+385>:   movsxd rbx,eax                            ;mov double word at eax into quadword at rbx with sign-extension
   0x000055555540096e <+388>:   lea    rax,[rbp-0x170]                    ;rbp-0x170 is our input and we put it into rax for our call to strlen
   0x0000555555400975 <+395>:   mov    rdi,rax                            ;mov our input into rdi for strlen call
   0x0000555555400978 <+398>:   call   0x555555400680 <strlen@plt>        ;call strlen, rax holds our return value which is the string length of rbp-0x170
   0x000055555540097d <+403>:   cmp    rbx,rax                            ;we compare our current loop iterator number to our strlength
   0x0000555555400980 <+406>:   jb     0x5555554008c3 <main+217>          ;jump inside our loop since our iterator is below strlength 
```
