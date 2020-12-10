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

2. In some cases with running collect command on windows you might get error: 
Chrome is downloaded but fails to launch on Node.js 14
If you get an error that looks like this when trying to launch Chromium:

(node:15505) UnhandledPromiseRejectionWarning: Error: Failed to launch the browser process!
spawn /Users/.../node_modules/puppeteer/.local-chromium/mac-756035/chrome-mac/Chromium.app/Contents/MacOS/Chromium ENOENT
This means that the browser was downloaded but failed to be extracted correctly.
The most common cause is a bug in Node.js v14.0.0 which broke extract-zip, the module Puppeteer uses
to extract browser downloads into the right place. The bug was fixed in Node.js v14.1.0, so please make sure you're running that version or higher.
Alternatively, if you cannot upgrade, you could downgrade to Node.js v12, but we recommend upgrading when possible.

