import os
import datetime
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from AI_Copilot import ai_newsletter


def run_weibo_event():
    # 运行 Weibo_Event.py 文件
    os.system("python Weibo_Event.py")


def send_email():
    # 获取当前日期
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    print('正在生成新闻简报…')
    newsletter = ai_newsletter()
    print(newsletter)

    # 生成发送邮件的内容
    msg = MIMEMultipart()
    msg['From'] = "179807648@qq.com"
    msg['To'] = "13488753641@163.com, 179807648@qq.com"
    msg['Subject'] = f"人工智能行业大事件日报 - {date_str}"

    body = f"早安，今天是 {date_str} " \
           "附件是过去24小时人工智能行业重要的新产品新技术和行业动态汇总，包含如下媒体：\n" \
           "\n" \
           "@宝玉xp\n" \
           "@互联网的那点事\n" \
           "@机器之心\n" \
           "@量子位\n" \
           "@新智元\n" \
            "\n" \
           f"{newsletter}\n" \
           "\n" \
           "请下载附件中的 CSV 文件并访问 Claude 镜像站（https://www.claudeai.ai）进行研判释读。\n" \


    msg.attach(MIMEText(body, 'plain'))

    # 检查 weibo_event 文件夹下是否存在当天日期的 CSV 文件
    folder_path = "weibo_event"
    file_name = f"{date_str}.csv"
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        print(f"No file found for {date_str}")
        return

    # 将 CSV 文件添加为附件
    attachment = open(file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)  # 将附件内容以base64编码
    part.add_header('Content-Disposition',
                    f"attachment; filename= {file_name.encode('gbk').decode()}")  # 指定文件名的字符编码为gbk
    msg.attach(part)

    # 发送邮件
    email_server = smtplib.SMTP('smtp.qq.com', 587)  # 使用你的邮件服务器和端口号
    email_server.starttls()
    email_server.login("179807648@qq.com", "zlftnvbaoocccaje")  # 使用你的邮箱地址和密码进行登录
    # email_server.login("bot74862@gmail.com", "up99rwHMj7M&ULKD")  # 使用你的邮箱地址和密码进行登录

    email_server.send_message(msg)
    email_server.quit()


if __name__ == "__main__":
    # run_weibo_event()
    send_email()
