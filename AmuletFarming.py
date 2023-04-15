import time
import os
import pickle

import grab_items
import heal_return
import time_to_seconds
from shiny_notify import ping_mail, check_mail_acc

# this program grabs items and then fly's to go restore pokemon pp

os.environ['REQUESTS_CA_BUNDLE'] = "certifi/cacert.pem"

if os.path.isfile("email.dat"):
    google_email = pickle.load(open("email.dat", "rb"))

if os.path.isfile("mail_password.dat"):
    mail_password = pickle.load(open("mail_password.dat", "rb"))


def run(x=None, run_code_time=None):
    if x is None and run_code_time is None:
        # then ask for amount of times user can use sweet scent before going to pokecenter
        x = input("Number of times to use sweet scent: ")
        # ask how long the code should run
        print("Time format: hours.minutes\n2.35 = 2 hours and 35 minutes")
        run_code_time = input("How long do you want the code to run for: ")
    x = int(x)
    run_code_time = time_to_seconds.sum_seconds(run_code_time)
    print("Running for " + str(run_code_time) + " seconds")
    time.sleep(2)
    # this is when the code started to run
    start_time = time.time()
    # this is when the code should stop
    end_time = time.time() + run_code_time
    # while we have not reached the end time, keep on going
    while end_time > time.time():
        heal_return.run()
        grab_items.run(x)
        if end_time > time.time():
            print(str(round((time.time() - start_time) / (end_time - start_time) * 100)) + "% Done")
        else:
            print("100% Done")

    # send email to user that script is done if they have put their acc details
    if check_mail_acc():
        ping_mail(google_email, mail_password, "Script is DONE")

