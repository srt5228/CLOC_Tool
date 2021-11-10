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


    repo_link = input("Please enter the git clone address:")
    validate = re.findall("^https:\/\/.*\.git$", repo_link)
    directory = ""
    for i in range(len(repo_link) - 1, 0, -1):
        if repo_link[i] == "/":
            break
        directory += repo_link[i]
    directory = directory[:3:-1]
    print(directory)
    if len(validate) == 0 or len(validate) > 1:
        print("You entered an invalid address")

    p = subprocess.Popen(["powershell.exe", f"git clone {repo_link}"], stdout=sys.stdout)
    print(p.stdout)
    p.communicate()
    q = subprocess.Popen(["powershell.exe", f"C:\\cloc-1.64.exe {directory}"], stdout=subprocess.PIPE)
    p2 = subprocess.run(["powershell.exe", f"C:\\cloc-1.64.exe {directory}"], capture_output=True)
    p2s = p2.stdout.decode("utf-8")
    print(p2s)
    result = q.communicate()
    print(result)
    # subprocess.call("powershell.exe C:\cloc-1.64.exe C:\Users\srthompson\Documents\\front_end_react")

    receiver = "scottiecodes@gmail.com"
    body = p2s

    yag = yagmail.SMTP("ScottieCLOC@gmail.com")
    yag.send(
        to=receiver,
        subject="CLOC Results",
        contents=body
    )



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initialize()


