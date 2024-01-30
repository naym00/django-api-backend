from datetime import datetime
import re
from django.core.mail import EmailMessage
from email_validator import validate_email, EmailNotValidError

class Generichelps:

    def send_mail_including_attatchment(self, subject, message, recipient_list, attachments=[], email_from = None):
        flag = False
        try:
            email = EmailMessage(subject, message, email_from, recipient_list)
            for attachment in attachments:
                email.attach_file(attachment)
            flag = bool(email.send())
        except: flag = False
        return flag
    
    def emailvalidate(self, email, condition=True):
        flag = False
        if condition:
            try:
                v = validate_email(email) 
                # replace with normalized form
                email = v["email"]  
                flag = True
            except EmailNotValidError as e: pass
        else: flag = True
        return flag
    
    def attachmentvalidate(self, attachmentname, condition=True):
        flag = False
        if condition:
            if '.pdf' in attachmentname[len(attachmentname)-4:]: flag = True
        else: flag = True
        return flag

    def numbervalidate(self, num, condition=True):
        flag = False
        if condition:
            if num.isnumeric():
                if len(num) == 11:
                    if num[:2] == '01':
                        if num[2] in ['3', '4', '5', '6', '7', '8', '9']:
                            flag = True
        else: flag = True
        return flag
    
    def datevalidate(self, date, condition=True):
        flag = False
        if condition:
            try:
                datetime.strptime(f'{date} 00:00:00', '%Y-%m-%d %H:%M:%S')
                flag = True
            except:
                pass
        else: flag = True
        return flag
    
    def datevalitime(self, time, condition=True):
        flag = False
        if condition:
            try:
                datetime.strptime(f'2024-01-01 {time}', '%Y-%m-%d %H:%M:%S')
                flag = True
            except:
                pass
        else: flag = True
        return flag