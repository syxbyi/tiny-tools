import pip

# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
from subprocess import call

for obj in pip.get_installed_distributions():
    call("pip install --upgrade " + obj.project_name, shell = True)
