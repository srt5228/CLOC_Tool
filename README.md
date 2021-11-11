# CLOC_Tool
This repo contains a script to run the CLOC tool against a remote git repo 
CLOC - https://github.com/AlDanial/cloc

This script is meant to be run on a windows machine with the CLOC executable installed dirictly in the C:\ directory. This was the easiest method for getting CLOC working
on Windows without worrying about end users installing and configuring Perl correctly. I have included the exe in the repo for convenience - again, please install it directly
in the C drive (not a subfolder). 

In addition to having CLOC installed, the machine will require python to be installed as well: https://www.python.org/downloads/

External Python Packages Used: 

          - Yagmail - GMAIL SMTP library for sending the results to recepient email
          - keyring - Allows python direct access to OS keyring (in case of Windows - Windows Credential Manager)
          
Program Functionality: 

This script begins by requesting the remote git repo you would like to run an analysis on. This link MUST be of the format (https://xxxxxxxxxxxxxx.git), you can only pass one 
repo in at a time. It will then ask you for a recepient email - I have not implemented any input validation here other than stripping whitespace so make sure to enter the 
recipient email exactly - if the email is not sent then you likely entered an invalid address. 

Additionally, yagmail is hardwired to scottieCLOC@gmail.com - the first time you run the script keyring will ask you for the password for this email account. If you would like
to use your own gmail account - change line 63 of the code to the email you would prefer. NOTE: If you provide your own GMAIL account, you need to make sure you have 
"Less Secure App Access turned on in GMAIL settings. 
          
