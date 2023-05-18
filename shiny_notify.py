import smtplib
import os


def check_mail_acc():
    if os.path.isfile("email.dat") and os.path.isfile("mail_password.dat"):
        with open("log.txt", "a") as f_temp:
            print("Mail Acc Exists", file=f_temp)
        return True
    with open("log.txt", "a") as f_temp:
        print("Mail does not exist", file=f_temp)
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

        with open("log.txt", "a") as f_temp:
            print('Email sent!', file=f_temp)
    except:
        with open("log.txt", "a") as f_temp:
            print('Something went wrong...', file=f_temp)
