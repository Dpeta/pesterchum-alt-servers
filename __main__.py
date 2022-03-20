#!/usr/bin/env python3
# Tries to run_as_subprocess.py as an absolute and relative import. (for script or module)
import sys

try:
    from .run_as_subprocess import main
except (ImportError, ModuleNotFoundError):
    from run_as_subprocess import main 
    
main(sys.argv)
