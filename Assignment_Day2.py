# Q-1 try 5 different function of string in python
# 1)captitalized
var=PYTHON
print(var.capitalize())
#Answer-Python

# 2)lower
var = 'Python'
print (var.lower())
#Answer- python

# 3)upper()
var = 'TechBean'
print (var.upper())
#Answer- TECHBEAN

# 4) swapcase()
var = 'TechBeamers'
print (var.swapcase())
#Answer- tECHbEAMERS

# 5) Title()
var = 'welcome to Python programming'
print (var.title())
#Answer- Welcome To Python Programming





# Q2-try 5 different function of list object in python
# 1)append()
List = ['Mathematics', 'chemistry', 1997, 2000] 
List.append(20544) 
print(List) 
#Answer-['Mathematics', 'chemistry', 1997, 2000, 20544]

# 2)insert()
List = ['Mathematics', 'chemistry', 1997, 2000] 
List.insert(2,10087)      
print(List)  
# Answer-['Mathematics', 'chemistry', 10087, 1997, 2000, 20544]

#3)extend()
List1 = [1, 2, 3] 
List2 = [2, 3, 4, 5] 
List1.extend(List2)		 
print(List1) 
List2.extend(List1) 
print(List2) 
# Answer-1, 2, 3, 2, 3, 4, 5]
# [2, 3, 4, 5, 1, 2, 3, 2, 3, 4, 5]

# 4)sum()
List = [1, 2, 3, 4, 5] 
print(sum(List)) 
# Answer-15

# 5)length()
List = [1, 2, 3, 1, 2, 1, 2, 3, 2, 1] 
print(len(List)) 
#Answer-10





# Q3-Experiment at least 5 default functions of dictonary
myDictionary = {'Key-1': 'Element-1', 'Key-2': 'Element-2', 'Key-3': 'Element-3', 'Key-4': 'Element-4'}
# 1)len()
print(len(myDictionary))
# answer-5

# 2)clear()
myDictionary.clear()
print (myDictionary)
# answer-{}

# 3)values()
print (myDictionary.values())
# answer-{"Element-1", "Element-2", "Element-3", "Element-4", "Element-5"}

# 4)keys()
print  (myDictionary.keys())
# answer-{"Key-1", "Key-2", "Key-3", "Key-4", "Key-5"}

# 5)items()
print (myDictionary.items())
# answer-{('Key-1': 'Element-1'), ('Key-2': 'Element-2'), ('Key-3': 'Element-3'),
# ('Key-4': 'Element-4'), ('Key-5': 'Element-5')}



