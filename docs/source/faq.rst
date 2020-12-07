Troubleshooting and FAQ
==================================================


1. If you get error like **Error: spawn wmic.exe ENOENT** while running collect command (using apify) in alternat on **Microsoft Windows** 
This indicates that the wmic utility's directory is not found on your PATH.
Open the advanced System Properties window (you can open the System page
with Windows+Pause/Break) and on the Advanced tab, click Environment Variables.
In the section for system variables, find PATH (or any capitalization thereof).
Add this entry to it::


    %SystemRoot%\System32\Wbem


Note that entries are delimited by semicolons.

