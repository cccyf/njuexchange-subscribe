# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

import private_data #邮件信息 密码等

context = ssl._create_unverified_context()
filename='last_save'#存上一次最新通知名 首行单行存全名

def crawl(front, url):
    last_name = _init_lastname()
    html = urlopen(url=url, context=context).read();
    soup = BeautifulSoup(html, "html.parser", from_encoding='GBK')
    ul_part = soup.find('ul', class_='ny').findAll('a')
    new_infos = []
    for each in ul_part:
        if each.string != last_name:
            new_infos.append(NewInfoEntry(front + each['href'], each.string))
        else:
            break
    if len(new_infos) > 0:
        send(new_infos)
        _update_lastname(new_infos[0].info_name)    
    soup.clear()
    return


def send(new_list):
    content = 'New exchange projects：\n'
    for each in new_list:
        content += 'info  :  ' + each.info_name + '\n'
        content += 'url  :  ' + each.info_url + '\n'
    msg = MIMEText(content,'plain')
    msg['from'] = _format_address(private_data.sender_name,private_data.sender)
    msg['to'] = _format_address(private_data.receiver_name,private_data.receivers)
    msg['subject'] = Header('New exchange project infos');
    try:
        smtp = smtplib.SMTP_SSL(private_data.mail_host, 465)
        #to access qq.smtp.com 
        #use smtp_ssl and 465 for ssl port
        smtp.set_debuglevel(1)
        smtp.login(private_data.mail_user, private_data.mail_pass)
        #mail_pass should be the authorization code
        #qq邮箱的smtp服务 需要用授权码而不是密码
        smtp.sendmail(private_data.sender, private_data.receivers, msg.as_string())
        smtp.quit()
        print('success')
    except smtplib.SMTPException:
        print('cannot send the email')
    return

def _format_address(name,address):
    return formataddr((Header(name,'utf-8').encode(),\
        address))

def _init_lastname():
    file = open(filename,'r')
    name = file.readline()
    file.close()
    return name

def _update_lastname(new_name):
    file = open(filename,'w')
    file.write(new_name)
    file.flush()
    file.close()
    return

class NewInfoEntry:
    info_url = ''
    info_name = ''

    def __init__(self, url, name):
        self.info_name = name
        self.info_url = url
