# Local Notes for Building a GitHub Repo

This small guide is for building a GitHub repository -- particularly, by creating a remote repository on github.com and then cloning it to a local machine. It serves as both a resource and a record of how I built this repo -- otherwise, I might totally forget.

This guide mostly follows https://www.warp.dev/terminus/git-clone-ssh.

NOTE: Pt 1 is OPTIONAL if you already have SSH keys that are connected to your GitHub account.

## (OPTIONAL) Pt 1 -- Configure GitHub to use SSH

1. On your local machine, run `$ ssh-keygen -t ed25519 -C "<comment>"` to generate an SSH key pair
   - You can specify the filepath to save the SSH key to (default is `~/.ssh/`)
   - You may set a passphrase (default is no passphrase)
   - Check that this was successful by running `$ ls <path/to/sshkey/`
   - NOTE:
        - "ed25519" is a popular cryptographic format
        - "<comment> is usually the username/email, e.g. "brewstronomy"

2. Copy your SSH public key (e.g. contents of `ed25519.pub`)
   - One way is by running `$ cat ~/.ssh/ed25519.pub` and copying the results
   - NOTE:
         - Ensure the ssh-agent is active by running `$ eval $(ssh-agent)`

3. Log in to your GitHub profile

4. Click on "New SSH Key"
   - Under **Settings > SSH and GPG Keys > New SSH key**

5. Enter the SSH public key
   - Paste the key in the "Key" field
   - You can also specify a Title (and a key type)
  
6. Click "Add SSH Key"
   - Your GitHub profile is now configured to allow repository access using SSH protocols


## Pt 2 -- Create Remote GitHub Repository

1. Log in to your GitHub profile

2. Click on "New" to create a new remote repository
   - NOTE:
         - This assumes a *public* repository -- private repositories require more configuration

3. Navigate to the repository page

4. Copy the repository SSH URL
   - Under **Code > SSH**
   - Will copy something like `git@github.com:<account>/<repo>.git`


## Pt 3 -- Clone Remote Repository to Local Repository

1. Navigate to the filepath where the local repository will be stored

2. Clone the remote repository by running `$ git clone <copied SSH URL from step 2.4>`
   - This should create the repo folder in your current directory
   - You can now make changes to the local directory.

TO DO:
* add doc for pushing/pulling
* add doc for creating repo starting from a local repo
* add doc about merge/rebase/fast-forward
