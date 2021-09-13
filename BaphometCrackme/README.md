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
   0x000000000000081e <+52>:    mov    DWORD PTR [rbp-0x4b0],0x0                             ;                                            
   0x0000000000000828 <+62>:    mov    DWORD PTR [rbp-0x490],0x89                                                                                           
   0x0000000000000832 <+72>:    mov    DWORD PTR [rbp-0x48c],0xbb                                                                                           
   0x000000000000083c <+82>:    mov    DWORD PTR [rbp-0x488],0x800                                                                                          
   0x0000000000000846 <+92>:    mov    DWORD PTR [rbp-0x484],0x0                                                                                            
   0x0000000000000850 <+102>:   mov    DWORD PTR [rbp-0x4ac],0x0                                                                                            
   0x000000000000085a <+112>:   mov    DWORD PTR [rbp-0x4a8],0x0                                                                                            
   0x0000000000000864 <+122>:   lea    rdi,[rip+0xaec]        # 0x1357                                                                                      
   0x000000000000086b <+129>:   call   0x670 <puts@plt>                                                                                                     
   0x0000000000000870 <+134>:   lea    rdi,[rip+0xb01]        # 0x1378                                                                                      
   0x0000000000000877 <+141>:   call   0x670 <puts@plt>                                                                                                     
   0x000000000000087c <+146>:   lea    rdi,[rip+0xb3d]        # 0x13c0                                                                                      
   0x0000000000000883 <+153>:   call   0x670 <puts@plt>                                                                                                     
   0x0000000000000888 <+158>:   lea    rdi,[rip+0xb9c]        # 0x142b                                                                                      
   0x000000000000088f <+165>:   mov    eax,0x0                                                                                                              
   0x0000000000000894 <+170>:   call   0x6a0 <printf@plt>                                                                                                   
   0x0000000000000899 <+175>:   lea    rax,[rbp-0x170]                                                                                                      
   0x00000000000008a0 <+182>:   mov    rsi,rax                                                                                                              
   0x00000000000008a3 <+185>:   lea    rdi,[rip+0xb95]        # 0x143f
   0x00000000000008aa <+192>:   mov    eax,0x0
   0x00000000000008af <+197>:   call   0x6b0 <__isoc99_scanf@plt>

```
