# Command line

## Searching files by contents
```bash
grep -rnw '/path/to/somewhere/' -e 'pattern'
```
where `-r` is recursive, `-n` is line number, and `-w` matches the whole word

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
