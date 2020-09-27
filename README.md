# PythonCode
﻿# LoginController utility

Login Controller is a utility created for auto login agents in case of force logout by finesse due to IP phone unregistration. it is tested with  cisco finesse 11.0 and 11.5 version.

## Installation

Run the installer to install the utility.

## Modification
modify the finesse primary and secondary url in ConfigProperty.ini file -->server section post installation. The file will be in the installed path inside LoginController folder.

## Usage

doubleclick the desktop icon to invoke the browser.Ideally it should run with user rights, If the utility closes after opening the browser,
then it may require admin rights, right click and run as administrator to run it.
```

##process notes for end users.

ProcessNote for LoginController utility(Administrator)
1) A shortcut for all users  will be created on desktop by this installer.
2) Go to LoginController folder in program files(default path) and modify the ConfigProperty.ini file----->server url section.
primary should have primary finesse url
secondary field should have secondary finesse url.
3) credentials are detected at user logon.

ProcessNote for LoginController utility(Agents):
1)Agent should double click on the desktop icon � LoginController.exe
2)It will load Finesse URL in new  Internet Explorer browser and open a window console.
3)Window console (logincontroller.exe) must be closed.
4)Post loading of Finesse URL- agent must enter their credentials and extension as BAU practice.
5)At Normal logout-the utility should close the browser and the user should manually close(LoginController.exe)
6)This utility will autologin the user only in case of IP phone unregistration.
7) The utility will also send reporting events to webserver. Reporting events will be send for (loggedon- eventcode 1,
  Forcedlogout-eventcode 2,ReloginafterForcedLogout-3)
Note: In case of utility not working,Agents may revert to normal login process to finsesse
