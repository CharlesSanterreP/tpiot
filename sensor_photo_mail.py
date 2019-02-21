import grovepi
# Import smtplib for the actual sending function
import smtplib, string, subprocess, time

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from subprocess import call

print("System Working")

SMTP_USERNAME = 'charlou95@gmail.com'  # Mail id of the sender
SMTP_PASSWORD = 'mdptpiot_1234'  # Pasword of the sender
SMTP_RECIPIENT = 'charlou95@gmail.com' # Mail id of the reciever
SMTP_SERVER = 'smtp.gmail.com'  # Address of the SMTP server
SSL_PORT = 465

while True:     # in case of IO error, restart
    try:
        while True:
            if grovepi.ultrasonicRead(7) < 100:  # If a person walks through the door
                print("Welcome")
                time.sleep(.5)

                # Take a picture from the Raspberry Pi camera
                call (["raspistill -o i1.jpg -w 640 -h 480 -t 0"], shell=True)
                print("Image Shot")
                p = subprocess.Popen(["runlevel"], stdout=subprocess.PIPE)
                out, err=p.communicate()    # Connect to the mail server
                if out[2] == '0':
                    print('Halt detected')
                    exit(0)
                if out [2] == '6':
                    print('Shutdown detected')
                    exit(0)
                print("Connected to mail")

                # Create the container (outer) email message
                TO = SMTP_RECIPIENT
                FROM = SMTP_USERNAME
                msg = MIMEMultipart()
                msg.preamble = 'Rpi Sends image'

                # Attach the image
                fp = open('i1.jpg', 'rb')
                img = MIMEImage(fp.read())
                fp.close()
                msg.attach(img)

                # Send the email via Gmail
                print("Sending the mail")
                server = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(FROM, [TO], msg.as_string())
                server.quit()
                print("Mail sent")

    except IOError:
        print("Error")
