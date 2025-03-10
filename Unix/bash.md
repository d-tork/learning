# Bash / Command line

## Searching files by contents
```bash
grep -rnw '/path/to/somewhere/' -e 'pattern'
```
where `-r` is recursive, `-n` is line number, and `-w` matches the whole word

Or more often, a quick search of the current directory:
```bash
grep -ir 'my text' .
```

## Searching _for_ a file by name pattern
```
find . -type f -name "*.tex"
```
> Traverse current directory (and subdirectories) for regular files that end in "tex".

## Finding filenames that match a pattern
```bash
find /data -type f -name '*.csv' -size -2k  
# (that are smaller than 2KB)
```

And to [remove files which match that pattern](https://unix.stackexchange.com/a/84853), 
append the `-delete` option if your `find` supports it.

## Encrypting with GPG (`gnupg`)
Based on [multiple](https://linuxconfig.org/how-to-encrypt-and-decrypt-individual-files-with-gpg/)
[articles](https://linuxconfig.org/how-to-create-compressed-encrypted-archives-with-tar-and-gpg/)
from linuxconfig.org.

### Get yourself a key
```bash
gpg --full-generate-key
```

### Encrypt with your default GPG key
For the recipient name, use the name for the key that will decrypt it.
```bash
gpg -e -r "Recipient Name" test.txt
```
It appends `.gpg` to the filename for the output.

### Decrypt
```bash
gpg -d test.txt.gpg > test_decrypted.txt
```
Because it outputs the decrypted contents to STDOUT, redirect or pipe it somewhere.

### Creating encrypted archives
```bash
tar -cvzf - folder_to_encrypt/ | gpg -e -r "Recipient Name" > encrypted_folder.tar.gz.gpg
```
This `tar`s and compresses to STDOUT in order to pipe it to gpg. To use a simple password instead 
of a key, replace `-r "Recipient Name"` with `-c ` (to input it into the shell) or `-c --passphrase
P@ssword!`. **Note**: an ssh session might give you  _signing failed: Inappropriate ioctl for 
device_. To fix this:
```bash
export GPG_TTY=$(tty)
```

To decrypt and extract:
```bash
gpg -d encrypted_folder.tar.gz.gpg | tar -xvzf -
```

#### Create multiple individual encrypted archives of directories
```bash
for i in * ; do tar -cvzf - "$i" | gpg > "$
```

### Encrypting for someone else
First, get your recipient's public key from them and import it. Also send them _your_ public key.
```bash
gpg --import yourfriends.key
gpg --output mygpgkey_pub.gpg --armor --export 'Your Name'
```
Then encrypt for them:
```bash
gpg -e -u "Your Name" -r "Their Name" test.txt
```

## Preview a CSV file
Works well for _very_ large files
```bash
head data.csv | column -s ',' -tn
```
Or to page through it:
```bash
column -s ',' -tn < data.csv | less -#2 -N -S
```

## How to run a script in the background
Add `&` after the command
```bash
./test.sh &

./test.sh > /dev/null 2>&1 &
./test.sh > outfile.log 2>&1 &
```
_Note: `2>&1` means standard error is redirected to standard output. And since
standard output has been redirected to outfile.log in the example, stderr also
goes there._

Use the linux **nohup** command, which is not affected by closing the terminal
```bash
nohup ./test.sh > dev/null 2>&1 &
```

Use the linux **setsid** command
```bash
setsid ./test.sh > dev/null 2>&1 &
```

## How to find your job running
```bash
jobs

ps -ef | grep "test.sh" | grep -v grep
```

## Sorting `du` by size
```bash
du -hs * | sort -hr
```
Where `du -hs` is human-readable and summarized, `*` is all the items in the current directory, 
and `sort -hr` is human-numeric-sort (i.e. between 2K and 1G) and in descending order.

## Command / Parameter expansion
from https://guide.bash.academy/expansions/

Parameter expansions (and all other value expansions) should **always** be double-quoted.
```bash
"the contents of the file are $(cat myfile.txt)"

contents="$(cat myfile.txt)"
```

Curly braces wrapped around parameter names are optional, but allow you to apply some formatting:
```bash
$ time=23.73
$ echo "current record is ${time%.*} seconds and ${time#*.} hundreths."
current record is 23 seconds and 73 hundredths.

$ echo "PATH currently contains: ${PATH//:/, }"
PATH currently contains: /Users/lhunath/.bin, /usr/local/bin, /usr/bin, /bin, /usr/libexec
```

## Truncate very wide output
Sometimes the output is too wide for the terminal and it wraps, causing ugly line breaks and 
spacing (e.g., `docker ps` when a container has a lot of port mappings).
```bash
docker ps | less -S
```

For docker specifically, `ps` [can be formatted](./Docker.md).

## Directly pass a file to a command
Instead of piping the output of a file with `cat` to another command (which runs an additional
process)
```bash
$ cat greeting.txt | wc -w
```
pass it directly:
```bash
$ < greeting.txt wc -w
```

## Pipe intermediate output at any time
`tee` inserted will still pass stdout to the next step in the pipeline.
```bash
seq 0 2 100 | tee even.txt | trim 5
```

## Pass your secret keys from file via command substitution
```bash
curl -s "http://newsapi.org/v2/everything?q=linux&apiKey=$(< /data/.secret/newsapi.org_apikey)"
```

## Edit previous command(s) with `fc`
Ensure your editor is set with `FCEDIT=vim`. List the commands first to get their number, or else
specify a negative number to walk backwards.
```
$ fc -l
10175  vim ~/.bash_profile
10176  config st
10177  config diff
10178* config st
10179* config add .vimrc

$ fc 10175
```

## Looping through lines in a file
```bash
# Setup
curl -s "https://randomuser.me/api/1.2/?results=5&seed=dsatcl2e" |
jq -r '.results[].email' > emails

while read line
do
echo "Sending invitation to ${line}."
done < emails
```

## Misc.
`alias` can be run to see all available aliases

`seq 5` prints an incrementing list of numbers up to five, `dseq 5` does the same but with dates.

## Bash history
[Great Digital Ocean article](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps) on using bash history and setting up how it's appended to.

[Good StackOverflow answer](https://superuser.com/questions/7414/how-can-i-search-the-bash-history-and-rerun-a-command)

### Get bash history into vim for use elsewhere
```bash
history | vim -
```
But this doesn't allow you to edit and write back to history to modify commands.

### Recalling historic command for editing first
To request a command be printed rather than executed after history substitution, add the `:p` 
modifier. This writes it to history so you can simply hit "up" and then modify.
```bash
!42:p
```

### Use builtin `fc` to modify a historic command in an editor
```
fc -10  # edit the 10th previous command

fc 1980  # edit command 1980
```
Upon exiting, the command will be executed. 

### Store a typed but unexecuted command in history
<kbd>Alt</kbd>+<kbd>#</kbd> comments out the current line and puts it in the history buffer.

Alternatively, <kbd>Esc</kbd><kbd>#</kbd>

### Navigate history with vim commands
With vi set as the editor (`set -o vi`), hit <kbd>Esc</kbd>, followed by the number of the command 
you want + <kbd>G</kbd>. This will place that command in the current prompt for editing.

### Searching through history as you type
<kbd>Ctrl</kbd>+<kbd>R</kbd>, then start typing. It will display the most recent command that matches
your pattern, and you can cycle through matches with <kbd>Ctrl</kbd>+<kbd>R</kbd> continuously.

### Immediately execute the first matching result
Type a <kbd>!</kbd>, followed by your search pattern. **Careful:** Hitting enter will execute.
```bash
!vi  # executes the last vim command
```

## One-line `for` loops with glob pattern
```bash
for f in ./billdownload-*; do ./runner.sh ${f}; done
```

## Checking if last command executed successfully

```bash
if command ; then
	echo success
else
	echo failed
fi
```

or as a beginner antipattern:

```bash
echo "this will work"
RESULT=$?
if [ $RESULT -eq 0 ]; then
  echo success
else
  echo failed
fi
```

## Redirecting output and errors

Send errors from your command to a specific file (redirect STDERR)
```
cmd 2> errors.txt
```

Combine errors with normal output
```
cmd 2>&1
```

