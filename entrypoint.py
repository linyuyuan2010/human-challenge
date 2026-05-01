import pathlib
import os
import sys

installed = pathlib.Path('/data/INSTALLED.lock')
if not installed.exists():
    from django.core.management import execute_from_command_line
    execute_from_command_line(["migrate"])

    installed.mkdir(parents=True)

if len(sys.argv) > 1:
    os.execvp(sys.argv[1], args=sys.argv[1:])
else:
    exit(1)