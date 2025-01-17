# 通知メール自動配信用モジュール

import datetime
from email.message import EmailMessage
from src.mail.mail import EmailController
from domain.consts import SystemConstants
from lib.config import load_config
config = load_config(SystemConstants.config)
config_secret = load_config(SystemConstants.config_secret)

def down_mail_sender(ip=0):
    # share file via gmail
    subject = config["mail"]["subject_pc_down"]
    with open(config["mail"]["template_pc_down"], 'r', encoding=SystemConstants.encode) as f:
        template = f.read()
    notice_mail = EmailController(config_secret["mail"]["from"], config_secret["mail"]["host"], config_secret["mail"]["port"], config_secret["mail"]["password"])
    body = template
    now = datetime.datetime.now()
    body += f"IP: {ip}\nShareTime: {now}\n"
    notice_mail.create(config_secret["mail"]["to"], subject, body)
    notice_mail.send()

def up_mail_sender(ip=0):
    # share file via gmail
    subject = config["mail"]["subject_pc_up"]
    with open(config["mail"]["template_pc_up"], 'r', encoding=SystemConstants.encode) as f:
        template = f.read()
    notice_mail = EmailController(config_secret["mail"]["from"], config_secret["mail"]["host"], config_secret["mail"]["port"], config_secret["mail"]["password"])
    body = template
    now = datetime.datetime.now()
    body += f"IP: {ip}\nShareTime: {now}\n"
    notice_mail.create(config_secret["mail"]["to"], subject, body)
    notice_mail.send()