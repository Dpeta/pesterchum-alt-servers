#!/usr/bin/env python3
# Wrapper script to run Pesterchum from an import independently of the current working directory. (useful for wheel)
# Running MainProgram() from an import would be better, but I think it requires making **all** imports relative depending on __main__,
# and probably other stuff too-

import os
import sys
from subprocess import call

#print(sys.argv)
def main(argv):
    arguments = ''
    for x in argv[1:]:
        arguments += x + ' '
    #print(arguments)
    
    directory_path = os.getcwd()
    print("Working directory: " + directory_path)
    os.chdir(os.path.dirname(__file__))
    print("Working directory set to: " + directory_path)
    print("Running Pesterchum as subprocess, this is not ideal.")
    retcode = call("python3 pesterchum.py " + " " + str(arguments), shell=True)
    print(retcode)

if __name__ == "__main__":
    main(sys.argv)
