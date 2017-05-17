# wetransfer-slurp

Downloads WeTransfer mails from a GMail account, extracts WeTransfer links, and downloads them.
This script is set up to be configured via environment variables:
 - USERNAME
 - PASSWORD

It writes to `/tmp`.

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

