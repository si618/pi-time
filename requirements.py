from subprocess import call

print "Updating python packages..."
packages = [package[0:package.index("=")] for package in open("requirements.txt")]
for package in packages:
    if len(package.strip()) > 0:
        call("pip install --upgrade " + package, shell=True)

print "\nUpdating npm packages..."
call("npm update", shell=True)

print "\nUpdating bower components..."
call("bower update", shell=True)
# call("grunt bowercopy", shell=True)

print "\nInstalled python packages:"
for package in packages:
    call("pip show " + package, shell=True)

print "\nInstalled npm packages:\n"
call("npm list --depth=0", shell=True)

print "\nInstalled bower components:\n"
call("bower list", shell=True)