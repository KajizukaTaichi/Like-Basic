# Like Basic
The simple and user-friendly Basic interpreter.


https://github.com/KajizukaTaichi/Like-Basic/assets/122075081/5a6624ed-12e3-414a-a479-22c87f3115a1



# Example code
Let's write this Like Basic program on your REPL.
```basic
10 ON ERROR 130
20 PRINT "Guess Game\n"
30 LET SEED = ROUND(RAND() * 100)
40 LET GUESS = INT(INPUT("Please guess seed value: "))
50 IF GUESS < SEED THEN 60 ELSE 80
60 PRINT "Too small\n"
70 GOTO 40
80 IF GUESS > SEED THEN 90 ELSE 110
90 PRINT "Too big\n"
100 GOTO 40
110 PRINT "Great!\n"
120 EXIT
130 PRINT "Invaild value\n"
140 GOTO 40
```
