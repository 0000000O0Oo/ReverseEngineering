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
