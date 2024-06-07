# Like Basic
The simple and user-friendly Basic interpreter.

https://github.com/KajizukaTaichi/UEC-Basic/assets/122075081/6c551cdc-1586-4144-b4ba-882be778da18


# Example code
Let's write this Like Basic program on your REPL.
```basic
00 PRINT "Guess Game\n"
10 RAND SEED
20 LET SEED = round(SEED * 100)
30 PRINT "Please guess seed value: "
40 INPUT GUESS
50 IF int(GUESS) < SEED THEN 60 ELSE 80
60 PRINT "Too small\n"
70 GOTO 30
80 IF int(GUESS) > SEED THEN 90 ELSE 110
90 PRINT "Too big\n"
100 GOTO 30
110 PRINT "Great!\n"
```
