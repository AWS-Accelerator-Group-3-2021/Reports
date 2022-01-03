import sys, os, platform, time, flask, json, flask_cors, datetime, uuid, requests, random
from dotenv import load_dotenv
load_dotenv()

print("Starting The Reports System setup procedure...")
print()
print("Checking the system environment...")
print()
print("Gathered system information:")
print()
def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

print("""Python version: %s

linux_distribution: %s

system: %s

machine: %s

platform: %s

uname: %s

version: %s

mac_ver: %s
""" % (
sys.version.split('\n'),
linux_distribution(),
platform.system(),
platform.machine(),
platform.platform(),
platform.uname(),
platform.version(),
platform.mac_ver(),
))

print()
print("Checking for python version compatibility...")
time.sleep(1.5)
print()
if sys.version_info[0] < 3:
    print(sys.version_info[0])
    print("Python version is too old. Please install Python 3.8 or higher.")
    sys.exit(1)

print()
print("Checking for required files...")
time.sleep(1.5)
print()
for file in ['.gitignore', 'demo_reports.txt', 'main.py', 'models.py', 'home.js', 'index.html', 'list.html', 'list.js', 'README.md', 'requirements.txt', 'showReport.html', 'showReport.js', 'wiki.md']:
  if not os.path.exists(file):
    print("File `{}` not found.".format(file))
    print("Please make sure that all required files are in the same directory as setup.py.")
    print("It is recommended to clean and just get a fresh copy of the reports system.")
    print("Use the command `git clean -f && git fetch && git reset --hard origin/master` or go to https://gist.github.com/Prakhar896/1604b6d874284b31541e5d0050dcaf35 to get a script to do it for you.")
    print()
    print("SYSTEM SETUP FAILED !!!")
    print("Exiting...")
    sys.exit(1)
  else:
    print("{} ✅".format(file))

print()
print("Checking for and installing required libraries...")
time.sleep(1.5)
print()

os.system("pip install -r requirements.txt")
print()
time.sleep(3)
for moduleName in ['flask', 'flask_cors', 'json', 'os', 'sys', 'platform', 'time', 'datetime', 'uuid', 'requests', 'dotenv', 'random']:
    if moduleName not in sys.modules:
        print("{} ❌".format(moduleName))
        print("Please install the required libraries and try again.")
        print("SYSTEM SETUP FAILED !!!")
        print("Exiting...")
        sys.exit(1)

print()
print("Checking for environment variables...")
time.sleep(1.5)
print()
envError = False
for envVar in ['ADMIN_PASS', 'PASS_EXTENSION', 'DISCORD_WEBHOOK_URL', 'SERVER_ACCESS_CODE', 'VERSION', 'CLIENT_NAME']:
    try:
        if os.environ[envVar] == None or os.environ[envVar] == '':
            print("Environment variable `{}` is not available.".format(envVar))
            print("Please make sure that all required environment variables are set.")
            print()
            print("Setup will give you an option to generate a new environment file after this check.")
            envError = True
        else:
            print("{} ✅".format(envVar))
            print()
    except:
        print("Environment variable `{}` is not available.".format(envVar))
        print("Please make sure that all required environment variables are set.")
        print()
        print("Setup will give you an option to generate a new environment file after this check.")
        envError = True

print()
if envError:
    if platform.system() == 'Windows':
        print()
        print("Sorry, automatic env file generation is not supported on Windows.")
        print("Please manually create a new env file and try again.")
        print()
        print("SYSTEM SETUP FAILED !!!")
        print("Exiting...")
        sys.exit(1)
    
    print('Setup identified that you are missing one or more environment variables.')
    makeFile = input("Would you like setup to generate a new environment file for you? (y/n) ")
    print()
    if makeFile == 'y':
        print("Generating new environment file...this may take a few seconds...")
        time.sleep(1.5)
        print()
        os.system("touch .env")
        os.system("echo \"ADMIN_PASS=\" >> .env")
        os.system("echo \"PASS_EXTENSION=\" >> .env")
        os.system("echo \"DISCORD_WEBHOOK_URL=\" >> .env")
        os.system("echo \"SERVER_ACCESS_CODE=\" >> .env")
        os.system("echo \"VERSION=\" >> .env")
        os.system("echo \"CLIENT_NAME=The Reports System\" >> .env")
        print()
        print("New environment file `.env` generated.")
        print()
        print("Please open the file and set all the required environment variables.")
        print()
        print("Setup will now continue with the setup process...")
        time.sleep(1.5)
        print()
    elif makeFile == 'n':
        print("Aborting automatic env file generation...")
        print()
        print("Setup will now continue with the setup process...")
    else:
        print("Invalid input. Aborting...")
        print()
        print("SETUP FAILED !!!")
        print("Exiting...")
        sys.exit(1)


print()
print("Checking for data files...")
time.sleep(1.5)
print()

for file in ['reports.txt', 'config.txt', 'authTokens.txt']:
    if not os.path.exists(file):
        print("File `{}` not found.".format(file))
        print("However, do not worry, main.py will auto-generate this file for you upon runtime.")
        print()
    else:
        print("{} ✅".format(file))

print()
print("Checking for documentation directories...")
time.sleep(1.5)
print()

if not os.path.exists('assets') or not os.path.exists('assets/version-endpoint.png'):
    print("The `assets` documentation directory or the `version-endpoint.png` that is supposedly within the `assets` folder is missing.")
    print("It is recommended to clean and just get a fresh copy of the reports system.")
    print("Use the command `git clean -f && git fetch && git reset --hard origin/master` or go to https://gist.github.com/Prakhar896/1604b6d874284b31541e5d0050dcaf35 to get a script to do it for you.")
    print()
    print("SYSTEM SETUP FAILED !!!")
    print("Exiting...")
    sys.exit(1)
elif not os.path.exists('README.md') or not os.path.exists('wiki.md'):
    print("The `README.md` or `wiki.md` file that is supposedly within the root directory is missing.")
    print("It is recommended to clean and just get a fresh copy of the reports system.")
    print("Use the command `git clean -f && git fetch && git reset --hard origin/master` or go to https://gist.github.com/Prakhar896/1604b6d874284b31541e5d0050dcaf35 to get a script to do it for you.")
    print()
    print("SYSTEM SETUP FAILED !!!")
    print("Exiting...")
    sys.exit(1)

print()
print("Setup has successfully finished!")
print("All files are found, required libraries are installed, and all required environment variables are set. ✅")
print("The setup process is now complete.")