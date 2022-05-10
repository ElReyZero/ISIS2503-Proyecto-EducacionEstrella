import requests
from requests.exceptions import Timeout
import logging
import sys
import time
from datetime import datetime
import os
from smtplib import SMTP
import urllib3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

log1 = logging.getLogger("monitor_log1")
log2 = logging.getLogger("monitor_log2")
log3 = logging.getLogger("monitor_log3")

def setupEmail():
    global email 
    email = "monitor.modulofinanciero@gmail.com"

    global password
    password = "SqB*!kE7R24CjrVtMqDC"

    global server
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)


def sendEmail(total_requests, failed_requests, ip):
    recipient = "juan.romero1201@gmail.com"
    body = f"""The monitor found that {failed_requests} requests failed out of {total_requests}\nTime of occurrence: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nIP of the machine that failed: {ip}"""

    message = MIMEMultipart()
    message["From"] = email
    message["To"] = recipient
    message["Subject"] = "WARNING - Monitor Modulo Financiero"
    message.attach(MIMEText(body, "plain"))
    ip = ip[8:22]
    with open(f"./MonitorData/logging/monitor_"+ip+".log", "rb") as f:
        payload = MIMEBase("application", "octete-stream")
        payload.set_payload(f.read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Disposition", "attachment", filename="monitor_"+ip+".log")
        message.attach(payload)

    text = message.as_string()
    server.sendmail(email, recipient, text)


def setupLogger(name, log):
    try:
        os.makedirs("./MonitorData/logging")
    except FileExistsError:
        pass
    logFilename = f"./MonitorData/logging/monitor_"+name+".log"
    formatter = logging.Formatter("%(asctime)s | %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    level = logging.DEBUG

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)


    file_handler = logging.FileHandler(logFilename)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    log.setLevel(level)
    log.addHandler(console_handler)
    log.addHandler(file_handler)


def main(ip, log):

    total_requests = 0
    failed_requests = 0
    try:
        for _ in range(100):
            log.info(f"Monitoring IP: {ip} | Sending request")
            t1 = time.time()
            response = requests.get(ip, timeout=1, verify=False)
            log.info(f"Monitoring IP: {ip} | Request sent")
            total_requests += 1
            if not response:
                log.error(f"Monitoring IP: {ip} | Request Failed. Response code: %s", response.status_code)
                failed_requests += 1
            t2 = time.time()
            log.info(f"Monitoring IP: {ip} | Request # {total_requests} completed in {t2-t1} seconds")
            time.sleep(0.5)

        log.info(f"Monitoring IP: {ip} | Finished sending requests")
        log.info(f"Monitoring IP: {ip} | Number of requests sent: {total_requests}")
        log.info(f"Monitoring IP: {ip} | Number of requests failed: {failed_requests}")
        if failed_requests > total_requests/5: #20%
            log.error("More than 20 percent of the requests failed")
            sendEmail(total_requests, failed_requests, ip)
            log.info("Email sent")
    except Timeout:
        log.error("The request timed out")
        failed_requests += 2


if __name__ == "__main__":
    ip1 = "http://52.91.92.224:8000/banca-empleo/"
    ip2 = "http://54.226.89.229:8000/banca-empleo/"
    ip3 = "http://54.87.23.251:8000/banca-empleo/"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    setupEmail()   
    setupLogger(ip1[8:22], log1)
    setupLogger(ip2[8:22], log2)
    setupLogger(ip3[8:22], log3)
    main(ip1, log1)
    main(ip2, log2)
    main(ip3, log3)
