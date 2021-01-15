import  smtplib
import csv
from email.message import EmailMessage
from getpass import getpass

# Block 6 -> Get credintials
def get_credintials():
    while True:
        sender = input('Sender Mail: ')
        if not sender.endswith('@gmail.com'):
            print("Please Enter A Valid Gmail.")
            continue
        password = getpass("Password: ")
        if len(password) < 6 :
            print("Password must be more than 5 letters.")
            continue
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender,str(password))
        except:
            print("Wrong credintials")
            continue
        break
    print()
    return (sender,password)

def get_mails():
    path = input("Mails,PDFs File (.CSV) Path: ")
    mails = []
    files = []

    with open(path,'r') as f:
        lines = csv.reader(f,delimiter = ';')
        try:
            for line in lines:
                if line != [] and '@' in line[1]:
                    mails.append(line[1])
                    files.append(line[2])
        except:
            print("Something Wrong.")
            get_mails()
    return mails,files

# Block 8 -> Subject and Body
def mail_text():
    # Let User set Subject
    subject = input('Subject: ')
    # Let user put body
    text = ""
    body = ""
    print("Body:")
    i = 0
    while text.lower() != "end":
        if i != 0:
            body +=  text +'\n'
        text = input()
        i+=1
    return (subject,body)

# Bloak 10 -> Preview
def preview(mails,subject, body ,sender,password, files):
    print("\n\nSubject: {}\n{}\nAttachments: {}".format(subject,body,files))
    print()
    confirm = input("Do You Confirm?(y/n) ")
    if confirm.lower() in ['y','yes','yeah']:
        send(mails,body,subject,files,sender,password)

# Send e-mails
def send(mails,body,subject,files,sender,password):

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender,password)
        i = 0
        success = []
        fail = []
        l = len(mails)
        print("Sent to:")
        for i in range(l):
            try:
                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = mails[i]
                msg.set_content(body)
                if files[i] != None:
                    try:
                        with open(files[i], 'rb') as f:
                            data = f.read()
                            name = f.name
                        msg.add_attachment(data,maintype='applicatoin',subtype = 'octet-stream',filename = name)
                    except:
                        pass
                smtp.send_message(msg)
                success.append(mails[i])
                print(mails[i])
            except:
                fail.append(mails[i])

    if len(fail) != 0:
        print("\nFailed to send to:\n")
        for i in fail:
            print(i)


def main():

    # Get credintials
    sender,password = get_credintials()
    # Get emails from CSV file
    mails,files = get_mails()
    # Get subject and body
    subject,body = mail_text()
    # get PDF
    preview(mails,subject, body, sender, password, files)

    s = input("Press Enter to Exit!")


main()
