# write down a program for opening a file and writing "I Love Letsupgrade" and closeit, and read it back again,and then append some data to it and close it
# answer
f = open("temp.txt", "w")
f.write("I Love Letsupgrade!")
f.close()

f = open("temp.txt", "r")
print(f.read())

f = open("temp.txt", "a")
f.write("Now the file has more content!")
f.close()


# Write a Function Which can Return a Factorial of any number as int,given in the argument
# answer

# change the value for a different result
num = 7

# To take input from the user
#num = int(input("Enter a number: "))

factorial = 1

# check if the number is negative, positive or zero
if num < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif num == 0:
   print("The factorial of 0 is 1")
else:
   for i in range(1,num + 1):
       factorial = factorial*i
   print("The factorial of",num,"is",factorial)