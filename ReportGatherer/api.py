from flask import Flask
from flask_restful import Resource, Api
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask("MonitorGatherer")
api = Api(app)


class Reporte(Resource):
    def get(self):
        return sendEmail()


api.add_resource(Reporte, '/getreport/')


def setupEmail():
    global email 
    email = "reportes.modulofinanciero@gmail.com"

    global password
    password = "y43@RnL$ESX%X@"

    global server
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

def sendEmail():
    recipient = "juan.romero1201@gmail.com"
    body = f"""This email contains the historical financial report."""

    message = MIMEMultipart()
    message["From"] = email
    message["To"] = recipient
    message["Subject"] = "INFO - Educacion Estrella Financial Report"
    message.attach(MIMEText(body, "plain"))
    try:
        with open(f"./reports/reporte.xlsx", "rb") as f:
            payload = MIMEBase("application", "octete-stream")
            payload.set_payload(f.read())
            encoders.encode_base64(payload)
            payload.add_header("Content-Disposition", "attachment", filename="reporte.xlsx")
            message.attach(payload)

        text = message.as_string()
        server.sendmail(email, recipient, text)
        return "Email sent"
    except FileNotFoundError:
        return"File not found"


if __name__ == "__main__":
    setupEmail()
    app.run(debug=True)