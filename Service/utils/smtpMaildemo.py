import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
# 解决收件人和发送人显示异常
from email.utils import parseaddr, formataddr

def format_addr(str):
    addr = parseaddr(str)
    return formataddr(addr)
def yagmail():

    # 使用SMTP连接
    smtplib.SMTP(host="", port=25, local_hostname="")
    # 通常使用 SSL连接
    smtplib.SMTP_SSL(host='', port=25)

    # 发送者
    sender = '1336732398@qq.com'
    # qq邮箱的授权码
    passward = 'tyvpmcekqcjcjdgh'
    # 接受者
    reciver = 'qz1336732398@163.com'

    # 主题
    subject = '测试SMTP邮箱'
    # 内容
    content = 'qq to 163'

    # 动议邮件三要素
    # msg = MIMEText(content, 'plain', 'utf-8') 字符串无样式发送
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = format_addr(u'qz <%s>' %sender)
    msg['To'] = format_addr(u'li <%s>' %reciver)
    print(msg['To'])
    msg['subject'] = subject


    try:
        client =  smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
        print("连接成功")
        client.login(sender, passward)
        print("登录成功")
        client.sendmail(list(sender), list(reciver), msg.as_string())
        print("发送成功")

    except smtplib.SMTPException as e:
        print("发送邮件异常")
    finally:
        client.quit()
