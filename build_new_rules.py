import os
import glob

files = glob.glob('*.ruel')

for file in files:
    rulename = file.rstrip('.ruel')
    os.system(f'python3 -m nutshell transpile -vvvvsc {file} .')
    os.system(f'mv {rulename}.rule "Rule:{rulename}"')