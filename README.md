# lostPassBitwarden
This repository contains a simple python script that will let you get back your bitwarden credentials from the desktop application.
>Let's say you forgot your master password, but luckly your laptop has windows hello and thus you can unlock your bitwarden vault. With this script you can open the desktop version of the Bitwarden vault and recover automatically most of your data!
Note that the script is far from perfect and only works well with login type credentials.

# Usage
To use this script just download it or copy it and install the dependencies with the following command
'''
pip3 install pyperclip keyboard mouse
'''
After the dependencies are installed you may run the script with the following in mind:
* This script was developed on an 1920 x 1080 screen in windows with 100% scaling, it may not play well on other systems
* This script has a lot of issues, you have to supervise it to check what gets copeid and what not, it is just a useful helper not a full automation

## CAUTION ⚠️
Once the script is running you have 5 seconds to switch to the bitwarden app, it is advised to start the app and set it to fullscreen before starting the script.
