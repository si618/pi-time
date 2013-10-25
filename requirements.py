from subprocess import call

packages = [package[0:package.index('=')] for package in open('requirements.txt')]
for package in packages:
    call('pip install --upgrade ' + package, shell=True)