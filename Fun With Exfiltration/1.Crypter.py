# This library will be used for Symmetric encryption.
from Cryptodome.Cipher import AES, PKCS1_OAEP
# This one for Asymmetric encryption.
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib

# This function will be responsible for RSA key generation (Asymmetric Encryption).
def generate():
    new_key = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key = new_key.publickey().exportKey()

    with open('key.private', 'wb') as f:
        f.write(private_key)

    with open('key.public', 'wb') as f:
        f.write(public_key)

# This function accepts key type (public or private) as argument.
def get_rsa_cipher(keytype):
    # Read the corresponding file:
    with open(f'key.{keytype}') as f:
        key = f.read()
    rsakey = RSA.importKey(key)
    # Returns cipher object and the size of RSA in bytes.
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())

# This function takes is responsible for data encryption.
def encrypt(plaintext):
    # Compresses plaintext bytes.
    compressed_text = zlib.compress(plaintext)

    # Generate random session key to be used in the AES cipher.
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    # Encrypt compressed plaintext.
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)

    # Pass the session key along with the ciphertext to be decrypted on the other side.
    cipher_rsa, _ = get_rsa_cipher('public')
    # Encrypt the (session key) with RSA key generated from the public key.
    encrypted_session_key = cipher_rsa.encrypt(session_key)

    # Assign all the information we need for decryption into one payload:
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    # Base64 encode it:
    encrypted = base64.encodebytes(msg_payload)
    return(encrypted)

# This function is for description (Basically reversing the encryption function).
def decrypt(encrypted):
    # First, Base64 decode the string into bytes.
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    cipher_rsa, keysize_in_bytes = get_rsa_cipher('private')

    # Read the encrypted session-key along with other parameters we need to decrypt from the encrypted string.
    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    ciphertext = encrypted_bytes.read()

    # Decrypt the session-key using the RSA private key.
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    # Use that key to decrypt the message itself with the AES cipher.
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)

    # Finally decompress the into plaintext byte string.
    plaintext = zlib.decompress(decrypted)
    return plaintext

# This function is used to generate the keys if you don't have any.
#if __name__ == '__main__':
#    generate()

# Where this one is to actually use the already generated keys.
if __name__ == '__main__':
    plaintext = b'hey there you.'
    print(decrypt(encrypt(plaintext)))
