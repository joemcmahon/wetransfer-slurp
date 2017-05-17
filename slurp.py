import email, getpass, imaplib, os, re
import requests, sys, json, getopt

if (sys.version_info > (3, 0)):
    from urllib.parse import urlparse, parse_qs
else:
    from urlparse import urlparse, parse_qs

imaplib._MAXLINE = 100000

DOWNLOAD_URL_PARAMS_PREFIX = "downloads/"
CHUNK_SIZE = 1024

def fetch():
    user = os.environ['USERNAME']
    if user == '':
      print('USERNAME not set')
      exit(1)

    pwd = os.environ['PASSWORD']
    if pwd == '':
      print('PASSWORD not set')
      exit(1)

    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("inbox") # here you a can choose a mail box like INBOX instead

    resp, items = m.search(None, 'subject', '"sent you files via WeTransfer"') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items = items[0].split() # getting the mails id

    urls = []
    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
        url = mail["X-WT-Download-URL"]
        urls.append(url)
    return urls

def download(file_id, recipient_id, security_hash, outdir='/tmp'):
    url = "https://www.wetransfer.com/api/ui/transfers/{0}/{2}/download?recipient_id={1}".format(
           file_id, recipient_id, security_hash)

    r = requests.get(url)
    download_data = r.json()
    if 'error' in download_data.keys():
         print(download_data)
         raise KeyError("URL didn't work.")

    print("Downloading {0}...".format(url))

    if 'direct_link' in download_data:
        direct_link_path = urlparse(download_data['direct_link']).path
        direct_link_path = direct_link_path.split('/')
        file_name = direct_link_path[-1]

        r = requests.get(download_data['direct_link'], stream=True)
    else:
        file_name = download_data['fields']['filename']
        r = requests.post(
            download_data['formdata']['action'],
            data=download_data["fields"],
            stream=True
            )

    file_name = os.path.join(outdir, file_name)
    file_size = int(r.headers["Content-Length"])
    output_file = open(file_name, 'wb')
    counter = 0
    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            output_file.write(chunk)
            output_file.flush()
            sys.stdout.write(
                '\r{0}% {1}/{2}'.format((counter * CHUNK_SIZE) * 100/file_size,
                                        counter * CHUNK_SIZE,
                                        file_size))
            counter += 1

    sys.stdout.write('\r100% {0}/{1}\n'.format(file_size, file_size))
    output_file.close()
    return file_name

def extract_params(url):
    """
        Extracts params from url
    """
    params = url.split(DOWNLOAD_URL_PARAMS_PREFIX)[1].split('/')
    [file_id, recipient_id, security_hash] = ['', '', '']
    if len(params) > 2:
        # The url is similar to
        # https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ
        [file_id, recipient_id, security_hash] = params
    else:
        # The url is similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/ZZZZZZZZ
        # In this case we have no recipient_id
        [file_id, security_hash] = params

    return [file_id, recipient_id, security_hash]


def extract_url_redirection(url):
    """
        Follow the url redirection if necesary
    """
    return requests.get(url).url


def main(argv):
    urls = fetch()

    for url in urls:
        url = extract_url_redirection(url)
        [file_id, recipient_id, security_hash] = extract_params(url)
        print(download(file_id, recipient_id, security_hash))

if __name__ == "__main__":
    main(sys.argv[1:])


