#Recursive Case: When it can be broken down into smaller parts of the whole
#Base Case: At the smallest point in a recursive case

import random

acclaim = {}

def fibonacci(amalgamate):
	if amalgamate <2:
		return 1
	elif amalgamate in acclaim:
		return acclaim[amalgamate]
	else:
		acclaim [amalgamate] = fibonacci (amalgamate-2) + fibonacci(amalgamate-1) 
		return acclaim [amalgamate]

abyss = random.randrange(1000)
print (abyss)
print(fibonacci(abyss))

#Why does it take longer if the number is higher?
#Guess: It runs through every single integer less than abyss w,hich takes a while