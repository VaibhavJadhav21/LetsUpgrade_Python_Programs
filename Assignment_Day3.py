# Q.1 Use IF ELSE and ELIF to write program in python for your report card.
# Answer-
var = 50
if var == 90 or  var >=90:
   print "you got A+"
   print var
elif var == 80 or var >=80:
   print "You got A"
   print var
elif var == 70 or var >=70:
   print "you got B"
   print var
elif var == 60 or var >=60:
   print "you got E"
   print var   
elif var == 50 or var >=50:
   print "you got E"
   print var
elif var == 40 or var >=40:
   print "you got E"
   print var   
else:
   print "you are fail"
   print var

print "Good bye!"


# Q.2 Use For Loop to Print prime Numbers In Between 1 to 1000
lower = 900
upper = 1000

print("Prime numbers between", lower, "and", upper, "are:")

for num in range(lower, upper + 1):
   # all prime numbers are greater than 1
   if num > 1:
       for i in range(2, num):
           if (num % i) == 0:
               break
       else:
           print(num)


# Q3-Write a Program To Print the Tables from 1,10 using Nested For Loop
i=1
for i in range(1,10):
    print("i =", i, ":")
    for j in range(1, 10):
        print (i*j)

    
# Q-4 Write a program to print X Prime Number Using While Loop starting From 0,and Take Input Of x From the User
Number = int(input(" Please Enter any Number: "))
count = 0

for i in range(2, (Number//2 + 1)):
    if(Number % i == 0):
        count = count + 1
        break

if (count == 0 and Number != 1):
    print(" %d is a Prime Number" %Number)
else:
    print(" %d is not a Prime Number" %Number)        