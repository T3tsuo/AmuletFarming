import smtplib
import os


def check_mail_acc():
    if os.path.isfile("email.dat") and os.path.isfile("mail_password.dat"):
        print("Mail Acc Exists")
        return True
    print("Mail does not exist")
    return False


def ping_mail(user, password, mes):
    sent_from = user
    to = [user, user]
    subject = "PokemonUI Notification"

    email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (sent_from, ", ".join(to), subject, mes)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(user, password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
