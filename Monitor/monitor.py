import requests
from requests.exceptions import Timeout
import logging
import sys
import time
from datetime import datetime
import os
from smtplib import SMTP
import urllib3
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
    recipient = "dcorreal@gmail.com"
    message = f"""From: monitor.modulofinanciero@gmail.com
                Subject: WARNING - Monitor Modulo Financiero\n
                The monitor found that {failed_requests} requests failed out of {total_requests}\n
                Time of occurrence: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n
                IP of the machine that failed: {ip}"""
    server.sendmail(email, recipient, message)

def setupLogger(name, log):
    try:
        os.makedirs("./MonitorData/logging")
    except FileExistsError:
        pass
    logFilename = f"./MonitorData/logging/monitor"+name+".log"
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
            response = requests.get(ip, timeout=5, verify=False)
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
            log.error("More than 20 percenet of the requests failed")
            sendEmail(total_requests, failed_requests, ip)
            log.info("Email sent")
    except Timeout:
        log.error("The request timed out")
        failed_requests += 2


if __name__ == "__main__":
    ip1 = "https://44.195.183.116/"
    ip2 = "https://44.195.183.116/websites"
    ip3 = "https://44.195.183.116/websites/?url=www.google.com/"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    setupEmail()
    setupLogger("1", log1)
    setupLogger("2", log2)
    setupLogger("3", log3)
    main(ip1, log1)
    main(ip2, log2)
    main(ip3, log3)
