#!/bin/env python

''' This is step one of the test
  
    This application takes a range and some rules and output the result
'''

# imports
import sys
import os
import json

def parse_cmdline(command_line_args):
  ''' parse the command line '''
  if (len(command_line_args)) < 4:
    print ("error parsing the command line with args %s" % command_line_args)
    printhelp()
    sys.exit(1)

  command_line_args.pop(0) # remove program name

  # ensure ranges are integers
  try:
    range_start = int(command_line_args.pop(0)) 
    range_end = int(command_line_args.pop(0))
  except ValueError as e:
    print ("error, range_start and range_end must be integers")
    printhelp()
    sys.exit(1)

  # set the file name of the rule file
  rule_file = command_line_args.pop(0)

  if int(range_start)>int(range_end):
    print ("error, range_start must be less than range_end")
    printhelp()
    sys.exit(1)

  return (range_start, range_end, rule_file)

def printhelp():
  ''' print the help message in case of command line error '''
  print ("program <start range> <end range> <rule file>")
  print ("Ex : program 1 20 rules.txt")

def parse_rule_file(rule_file):
  ''' open the rule file and create an array of rules '''
  all_rules=[]
  try:
    with open(rule_file) as localfile:
      for lines in localfile:
        json_data = json.loads(lines.rstrip())
        all_rules.append(json_data)
  except IOError as e:
    print("grep: %s: Can't open file" % rule_file)

  return (all_rules)

def multiple_rule(number, keys):
  ''' return true or false is number is a multiple of a the key'''
  for key in keys:
    if (number % key) != 0:
      return False
  return True

def process_rules(number,rules):
  rule_result=number
  rule_matched = False

  for rule in rules:
    if rule['type'] == "multiple":
      if multiple_rule(number,rule["keys"]):
       rule_result = rule["result"]
       rule_matched = True

  return (rule_result, rule_matched)

  
# start the main program
if __name__ == '__main__':

  # init some variables
  result_counter={}
  result_counter["integer"] = 0
  # parse command line
  (range_start, range_end, rule_file) = parse_cmdline(sys.argv)

  # load and parse the rule file
  rules=parse_rule_file(rule_file)

  # loop through the range
  for number in range(range_start,range_end + 1):
    result,status = process_rules(number,rules)
    print result,

    # store result count
    if status:
      if result in result_counter.keys():
        result_counter[result] += 1
      else:
        result_counter[result] = 1
    else :
      result_counter["integer"] += 1

  print ("\n")

  for value in result_counter:
    print ("%s: %s" % (value,result_counter[value]))
