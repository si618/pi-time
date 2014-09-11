from subprocess import call

print 'Upgrading PYPI...'
packages = [package[0:package.index('=')] for package in open('requirements.txt')]
for package in packages:
    call('pip install --upgrade --quiet ' + package, shell=True)

print '\nUpdating NPM...'
call('npm update', shell=True)

print '\nShowing PYPI versions...'
for package in packages:
    call('pip show ' + package, shell=True)

print '\nListing NPM packages...'
call('npm list', shell=True)

