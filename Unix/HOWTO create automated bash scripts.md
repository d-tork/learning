# HOW TO Create automated bash scripts
_i.e., to automate cloud backups_

## Prep
1. Wherever you're storing your script, make sure it's added to the PATH variable:
  ```bash
  export PATH=$PATH:~/bin
  ```

## Write the script
1. Create a new text file beginning with the following line:
  ```bash
  #!/bin/bash
  ```
2. Add your terminal commands to the file
  ```bash
  echo Hello World!
  ```
3. Save the file as plain text
  * file extension should be `.sh` (common practice)
  * put it in `~/bin` for safekeeping
4. Make executable
  ```bash
  chmod u+x myscript.sh
  ```
  * now it can be run with the filename directly (else, must call it with `bash myscript.sh`)
5. [Optional] Add a notification action
  ```bash
  #!/bin/bash
  /usr/bin/osascript -e 'display notification "message" with title "title"'
  ```

## Option A: Cron job
_In macOS, this has been largely replaced by launchd. However, you can still run cron jobs and learn more about them [here.](https://www.marksanborn.net/linux/learning-cron-by-example/)_
1. Run the following
  ```bash
  crontab -e
  ```
2. Add your command to that file, beginning with the cron syntax for scheduling:
  > **min | hr | dom | mon | dow | command**
  >
  > * **min** - Minutes
  > * **hr** - Hours (24 hour time)
  > * **dom** - Day of Month
  > * **mon** - Month
  > * **dow** - Day of Week (0 and 7 are Sunday)
  >
  > use * as a wildcard for any of these arguments

## Option B: Automator/launchd
_Essentially what you're doing here is creating a .plist file with a calendar/scheduler event in it. See [this page](https://www.maketecheasier.com/use-launchd-run-scripts-on-schedule-macos) for a detailed guide._  
User Agents stored in `~/Library/LaunchAgents`, root daemons in `/Library/LaunchDaemons`

1. Typical job definition:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.user.myscript</string> <!--don't include .plist-->
        <key>Program</key>
        <string>/Users/user/Scripts/myscript.sh</string> <!--include .sh-->
        <key>RunAtLoad</key>
        <true/>
    </dict>
```
  * "local" is a good prefix/domain for the label (job name)
  * there are two other options for running besides `RunAtLoad`:
    ```xml
    <key>StartInterval</key>
    <integer>7200</integer> <!--measured in seconds-->
    ```
    ```xml
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
        <!-- where these keys correspond to the cron arguments above -->
    </dict>
    ```
2. Save that file as `com.user.myscript.plist` in the proper folder.
3. Load your script into `launchctl`
  ```bash
  launchctl load ~/Library/LaunchAgents/com.user.myscript.plist
  ```
  * to remove it, use the `unload` command
  * to run it immediately, use
    ```bash
    launchctl start com.user.myscript
    ```


## Quick references
* iCloud Drive path for terminal  
  ```
  ~/Library/Mobile\ Documents/com~apple~CloudDocs/
  ```
* [rsync man page](https://www.unix.com/man-page/osx/1/rsync/)
* [launchd reference page](http://www.launchd.info/)
* How to create a terminal alias
  1. Edit or create .bash_profile file
  2. Add to bottom of file:  
    ```
    alias sync-home='rsync -varuz ~/ ~/OneDrive/'
    ```
  3. Refresh the bash shell environment  
    ```
    source ~/.bash_profile
    ```
