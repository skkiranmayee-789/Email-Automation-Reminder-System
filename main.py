import pandas as pd
import schedule
import time
import logging
import os

from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

# ---------------------------------
# LOAD ENV VARIABLES
# ---------------------------------
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ---------------------------------
# CREATE LOGS FOLDER
# ---------------------------------
os.makedirs("logs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ---------------------------------
# LOGGING CONFIGURATION
# ---------------------------------
logging.basicConfig(
    filename="logs/email_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ---------------------------------
# LOAD CONTACTS
# ---------------------------------
contacts = pd.read_csv("data/contacts.csv")

# ---------------------------------
# LOAD REMINDERS
# ---------------------------------
reminders = pd.read_csv("data/reminders.csv")

# ---------------------------------
# LOAD EMAIL TEMPLATE
# ---------------------------------
with open("templates/email_template.txt", "r") as file:
    template = file.read()

# ---------------------------------
# SEND EMAIL FUNCTION
# ---------------------------------
def send_email(name, email, subject, message):

    try:

        # DRY RUN MODE
        print("\n--------------------------------")
        print(f"Sending Email To: {name}")
        print(f"Email: {email}")
        print(f"Subject: {subject}")
        print("Message:")
        print(message)
        print("--------------------------------")

        logging.info(f"Email sent to {email}")

        return "Sent"

    except Exception as e:

        logging.error(f"Failed for {email}: {e}")

        return "Failed"

# ---------------------------------
# PROCESS REMINDERS
# ---------------------------------
report_data = []

for index, row in contacts.iterrows():

    name = row["Name"]
    email = row["Email"]

    for _, reminder in reminders.iterrows():

        subject = reminder["Subject"]

        personalized_message = template.replace(
            "{name}",
            name
        ).replace(
            "{message}",
            reminder["Message"]
        )

        status = send_email(
            name,
            email,
            subject,
            personalized_message
        )

        report_data.append({
            "Name": name,
            "Email": email,
            "Subject": subject,
            "Status": status,
            "Timestamp": datetime.now()
        })

# ---------------------------------
# GENERATE REPORT
# ---------------------------------
report_df = pd.DataFrame(report_data)

report_path = "outputs/email_report.csv"

report_df.to_csv(report_path, index=False)

print("\n✅ Email automation completed!")
print(f"📄 Report saved at: {report_path}")