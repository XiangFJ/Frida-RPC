import smtplib  # smtp服务器
from email.mime.text import MIMEText  # 邮件文本


def send_msg(info, module):

    # 邮件构建
    # 授权密码 RXXIUPQSQNLDBGYK
    subject = module + " - 模块报错！！！"  # 邮件标题
    sender = "pmi1331199xxxx@163.com"  # 发送方
    content = "错误信息 ===> " + info
    receiver = "pmi1331199xxxx@163.com" # 接收方 , 字符串列表，邮件发送地址
    password = "RXXIUPQSQNLDBGYK"

    message = MIMEText(content, "plain", "utf-8")
    # content 发送内容     "plain"文本格式   utf-8 编码格式

    message['Subject'] = subject  # 邮件标题
    message['To'] = receiver  # 收件人
    message['From'] = sender  # 发件人

    smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  # 实例化smtp服务器
    smtp.login(sender, password)  # 发件人登录
    smtp.sendmail(sender, receiver, message.as_string())  # as_string 对 message 的消息进行了封装
    smtp.close()
