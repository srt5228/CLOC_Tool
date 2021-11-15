import sys
import subprocess
import pkg_resources
import re
import pathlib
# Checks if yagmail is installed - if not installs it
required = {'yagmail', 'keyring'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yagmail"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "keyring"])
import yagmail
import keyring

def initialize():
    """
    Figures out OS script is running on (supports Linux/Windows) and then
    calls the logic for whatever OS it finds
    :return: None - Makes additional function call to {INSERT}
    """
    if sys.platform == "linux" or sys.platform == "linux2":
        print("linux functionality not supported")
    elif sys.platform == "win32" or sys.platform == "win64":
        print("windows")
        get_repo()


def get_repo():
    """
    This function takes the destination email to send the cloc report to as well as the
    target github repo
    :return:
    """

    valid = False
    while not valid:
        # get the github repo - must start with https:// and end with .git
        repo_link = input("Please enter the git clone address:")
        validate = re.findall("^https:\/\/.*\.git$", repo_link)

        # our regex findall returns a list of matching items - if there are none
        # or there are more than one (user passed multiple repos) then return invalid message
        if len(validate) == 0 or len(validate) > 1:
            print(""""You entered an invalid address - it is either not a valid git repo form or you
                  entered more than one repo. """)
        else:
            # user entered an appropriate git link
            valid = True
    cloc_repo(repo_link)


def cloc_repo(repo_link):
    """
    Takes repo link from get_repo and figures out directory name, runs cloc
    :param repo_link: The repo link passed from get_repo
    :return:
    """

    # this is just getting the directory name (what comes before .git - probably a way to do this with regex)
    directory = ""
    for i in range(len(repo_link) - 1, 0, -1):
        if repo_link[i] == "/":
            break
        directory += repo_link[i]
    directory = directory[:3:-1]
    # opening Poweshell and cloning passed github link
    clone_repo = subprocess.Popen(["powershell.exe", f"git clone {repo_link}"], stdout=sys.stdout)
    clone_repo.communicate()
    # running cloc against repo and decoding bit stream to string to pass to email
    run_cloc = subprocess.run(["powershell.exe", f"cloc-1.90.exe {directory}"], capture_output=True)
    cloc_results = run_cloc.stdout.decode("utf-8")
    # deleting the repo directory to avoid error messages if the user clocs the same repo - could have also checked
    subprocess.Popen(["powershell.exe", f"Remove-Item -Force -Recurse -Path .\\{directory}"], stdout=sys.stdout)
    # for the existence but feel like users might not want to keep taking space with these directories
    print(cloc_results)
    email_report(cloc_results, directory)


def email_report(email_body, repo_name):
    """
    Builds and sends the report email using yagmail
    :param email_body: String representation of cloc report
    :param repo_name: Name of repo - used in email subject
    :return:
    """

    keyring.set_password("system", "ScottieCLOC@gmail.com", "i;C{vEwLW0}cr2gBK!=5")
    receiver = input("Please enter email to send report to:")

    yag = yagmail.SMTP("ScottieCLOC@gmail.com")
    yag.send(
        to=receiver,
        subject=f"CLOC Results for git repo {repo_name}",
        contents=email_body
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initialize()


