import pathlib
import os
import sys

installed = pathlib.Path('/data/INSTALLED.lock')
if installed.exists():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'human_challenge.settings')
    
    from django.core.management import call_command
    call_command("migrate")

    installed.mkdir(parents=True)

if len(sys.argv) > 1:
    os.execvp(sys.argv[1], args=sys.argv[1:])
else:
    exit(1)