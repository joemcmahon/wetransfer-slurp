# wetransfer-slurp

Downloads WeTransfer mails from a GMail account, extracts WeTransfer links, and downloads them.
This script is set up to be configured via environment variables:
 - USERNAME
 - PASSWORD

It writes to `/tmp`.

# "GMail isn't letting me log in!"

This is because GMail doesn't want you to give your password to third parties to access
it on your behalf. There are two options to fix this:
 - Turn on "allow less secure apps". This is not saying that the app is full of security
   holes, but that it's an app that has your credentials, and giving your credentials to
   a third party app might allow them to be compromised.
 - The better solution: turn on two-factor authentication for the account, and then set
   an application-specific password for wetransfer-slurp to use. This password is meant
   only to be used by wetransfer-slurp, and can be revoked by you at any time, making
   safer (if you think wetransfer-slurp has compromised its password, you can simply
   imvalidate that password without locking yourself out completely).

## Running with Docker

It is strongly suggested you build a Docker image using the supplied Dockerfile, and run
the script like this:

```bash
docker build -t wetransfer-slurp:latest .

docker run --rm \
    -e USERNAME='imap_user@mail.provider.com' \
    -e PASSWORD='imapmailpassword` \
    -v /your/desired/location:/tmp \
    wetransfer-slurp:latest
```

