#!/bin/env python
''' compute the Hailstone (Collatz sequence) max steps
    for numbers between 1 and max_number

    prune@lecentre.net - 20150808
'''
# vars
max_number = 1000000

# internal vars
chain_count = {}

# compute
for n in range(1, max_number):
  current = n # backup the current number 
  steps = 1 # we start at one as the n number is a step itself
  while n != 1:
    if (n%2 == 1):
      # odd
      n = (n*3+1)
      steps += 1
    elif (n%2 == 0):
      # even
      n = n/2
      steps += 1
    else :
      print ("error")
  
  # fill the array of steps with corresponding numbers
  if steps in chain_count.keys():
    chain_count[steps].append(current)
  else:
    chain_count[steps] = [current]

# print result
max_steps=max(chain_count.keys())
print ("max number of step is %s for numbers %s" % (max_steps, chain_count[max_steps]))
