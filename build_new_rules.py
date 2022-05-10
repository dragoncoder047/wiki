import os
import glob
import sys

files = glob.glob('*.ruel')

for file in files:
    rulename = file.rstrip('.ruel')
    exitcode = os.system(f'python3 -m nutshell transpile {file} .')
    exitcode += os.system(f'mv {rulename}.rule "Rule:{rulename}"')
    if exitcode > 0:
        sys.exit(exitcode)

sys.exit(0)
# permanent fix for supposedly/nutshell#20
with open('Rule:Fusion') as f: badtext = f.read()
bef, af = badtext.split('var any.0')
goodtext = bef + '\n\nvar anyNTAAHead.0 = {7,8}\nvar any.0' + af
with open('Rule:Fusion', 'w') as f: f.write(goodtext)

