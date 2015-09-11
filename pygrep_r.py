#!/bin/env python

''' this script replicate the shell command :
          grep -r [Regex] [Files...]

    prune@lecentre.net - 20150808
'''

from __future__ import absolute_import, division, print_function
import sys
import os
import re

def printhelp():
  ''' print a help message '''
  print ('''
Usage :
    pygrep-r.py [Regex] [Files...]
''')

def parse_cmdline(command_line_args):
  ''' parse the command line to find a regexp and some paths or directories '''
  if (len(command_line_args)) < 3:
    print ("error parsing the command line with args %s" % command_line_args)
    printhelp()
    sys.exit(1)

  command_line_args.pop(0) # remove program name
  regexp = command_line_args.pop(0) # set regexp
  files = command_line_args # set the file names to grep into

  return (regexp, files)

def grep_regexp(my_path, my_regexp_comp):
  ''' Open a file and check the content against a regexp'''
  try:
    with open(my_path, 'rb') as localfile:
      for line in localfile:
        content = line.rstrip()
        if my_regexp_comp.search(content):
          print ("%s:%s" % (my_path, str(content)))
  except IOError as e:
    print ("grep: {0}: I/O error({1}): {2}".format(my_path, e.errno, e.strerror))
  except ValueError:
    print("grep: %s: File conversion error" % my_path)
  except:
    print("grep: %s: Can't open file" % my_path)

if __name__ == '__main__':
  (regexp, paths) = parse_cmdline(sys.argv)

  # compile regexp
  try:
    regexp_comp = re.compile(regexp)
  except :
    print("Error compiling the regexp '{0}'".format(regexp))
    sys.exit(1)

  # loop through commandline paths
  for path in paths:
    # walk through the path
    for root, dirs, files in os.walk(path, topdown=False):
      for filename in files:
        fullpath = os.path.join(root, filename)
        grep_regexp(fullpath, regexp_comp)
