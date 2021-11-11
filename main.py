import sys
import subprocess
import re
import yagmail


def initialize():
    """
    Figures out OS script is running on (supports Linux/Windows) and then
    calls the logic for whatever OS it finds
    :return: None - Makes additional function call to {INSERT}
    """
    if sys.platform == "linux" or sys.platform == "linux2":
        print("linux")
    elif sys.platform == "win32" or sys.platform == "win64":
        print("windows")
        get_email_repo_and_cloc()


def get_email_repo_and_cloc():
    """
    This function takes the destination email to send the cloc report to as well as the
    target github repo
    :return:
    """

    # get the github repo - must start with https:// and end with .git
    repo_link = input("Please enter the git clone address:")
    validate = re.findall("^https:\/\/.*\.git$", repo_link)
    # this is just getting the directory name (what comes before .git - probably a way to do this with regex)
    directory = ""
    for i in range(len(repo_link) - 1, 0, -1):
        if repo_link[i] == "/":
            break
        directory += repo_link[i]
    directory = directory[:3:-1]
    # our regex findall returns a list of matching items - if there are none
    # or there are more than one (user passed multiple repos) then return invalid message
    if len(validate) == 0 or len(validate) > 1:
        print(""""You entered an invalid address - it is either not a valid git repo form or you
              entered more than one repo.""")
    # opening Poweshell and cloning passed github link
    clone_repo = subprocess.Popen(["powershell.exe", f"git clone {repo_link}"], stdout=sys.stdout)
    clone_repo.communicate()
    # running cloc against repo and decoding bit stream to string to pass to email
    run_cloc = subprocess.run(["powershell.exe", f"C:\\cloc-1.64.exe {directory}"], capture_output=True)
    cloc_results = run_cloc.stdout.decode("utf-8")
    email_report(cloc_results, directory)


def email_report(email_body, repo_name):
    """
    Builds and sends the report email using yagmail
    :param email_body: String representation of cloc report
    :param repo_name: Name of repo - used in email subject
    :return:
    """

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


