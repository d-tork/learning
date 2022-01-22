# Bash / Command line

## Searching files by contents
```bash
grep -rnw '/path/to/somewhere/' -e 'pattern'
```
where `-r` is recursive, `-n` is line number, and `-w` matches the whole word

## Searching _for_ a file by name pattern
```
find . type f -name "*.tex"
```
> Traverse current directory (and subdirectories) for regular files that end in "tex".

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
gpg --export -a "Your Name" > your.key
```
Then encrypt for them:
```bash
gpg -e -u "Your Name" -r "Their Name" test.txt
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
