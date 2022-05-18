import os
import glob
import sys

files = glob.glob('*.ruel')

for file in files:
    rulename = file.rstrip('.ruel')
    exitcode = os.system(f'python3 -m nutshell transpile {file} .')
    if exitcode > 0:
        sys.exit(exitcode)
    try:
        os.remove(f"Rule:{rulename}")
    except FileNotFoundError:
        pass
    os.rename(f'{rulename}.rule', f"Rule:{rulename}")

