import yagmail
import os

def demo_yagmail():
    # 设置收件人，无需发件人
    receivers = ['qz1336732398@163.com']
    # 主题
    subject = 'yagmail测试'
    # 内容
    body = 'Body描述'
    html = '<a href="https://github.com/mrzcode/TestProjectManagement">项目代码点我!</a>'

    # 上传文件，附件的绝对路径 或者 通过open打开直接io流文件

    # path_file = os.path.dirname(os.path.abspath(__file__)) + '../../../img1.png'
    path_file = '/Users/qinzhen/Desktop/img1.png'
    attachment = [path_file]

    # 初始化服务对象直接根据参数给定
    server= yagmail.SMTP(host='smtp.qq.com', port=465,user='1336732398@qq.com', password='tyvpmcekqcjcjdgh')

    server.send(to=receivers, subject=subject, contents=[body,html], attachments=attachment)

    server.close()
    print("邮件发件成功")

# if __name__ == '__main__':
#     demo_yagmail()