from crypter import decrypt

with open('exfiled_pdf.txt', 'rb') as f:
    contents = f.read()
with open ('exfiled.pdf', 'wb') as f:
    f.write(decrypt(contents))
