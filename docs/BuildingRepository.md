# Local Notes for Building a GitHub Repo

1. Log in to GitHub profile on github.com

2. Pair your machine with GitHub using SSH key pairs 
(https://www.warp.dev/terminus/git-clone-ssh)

    2a. Generate an SSH key on local machine
        - $ ssh-keygen -t ed25519 -C "<comment>"
        - will ask you about file path to save to and if you want a 
passphrase
        - can check by running
            - $ ls ~/.ssh
        - NOTE:
            - "ed25519" is a popular cryptographic format
            - <comment> is usually the username, e.g. "brewstronomy"

    2b. Connect SSH key pair to Github
        - Log in to Git
