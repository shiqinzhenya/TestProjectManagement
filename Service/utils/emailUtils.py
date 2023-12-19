import yagmail
import traceback
from configs import config

'''
receivers 收件人，字符数组['邮件地址']
subject 邮件主题, 字符串
contents 邮件内容，自定义 字符数组
attachments 附件默认为空
'''
def sendEmail(receivers, subject, contents, attachments=[]):
    try:
        server = yagmail.SMTP(host=config.MAIL_HOST, port=config.MAIL_PORT, user=config.MAIL_USER, password=config)

        server.send(to=receivers, subject=subject, contents=contents,attachments=attachments)

        server.close()

    except Exception:
        print('traceback.format_exc(): {}'.format(traceback.format_exc()))
        return False
    return True