import zmail
import time
import requests
from bs4 import BeautifulSoup

# 邮箱配置信息
mail_user = "xxxxxxxx"
mail_pwd = "xxxxxxxxxx"
mail_host = "pop3.mxhichina.com"

# 建立邮件的连接
server = zmail.server(mail_user, mail_pwd, pop_host = mail_host)
mail = server.get_latest()
id = mail["id"] - 1

def send_notice(message):
   headers = {"Content-Type": "text/plain"}
   print(message)
   data = {
      "msgtype": "text",
      "text": {
         "content": message,
  }
   }
   r = requests.post(
      url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=',
      headers=headers, json=data)
   print(r.text)

while True:
    try:
        mail = server.get_latest()
        maxid = mail["id"]
        while id < maxid:
            id += 1
            mail = server.get_mail(id)
            # 主题 + 正文 
 #           content = "".join(mail["content"]) 
 #           content = mail["content_html"]
            content =  BeautifulSoup(mail["content_html"][0]).get_text()
            message = f"""发件人：\n{mail['from']}\n主题：\n{mail['subject']}\n正文：\n{content}"""
            print(message)
            send_notice(message)
            server.delete(id)
        # 如果邮箱有邮件被删除
        if id > maxid:
            id = maxid
    # 如果超时，则重新登陆
    except Exception as e:
        server = zmail.server(mail_user, mail_pwd, pop_host =  mail_host)
    # 每30秒检查一次
    time.sleep(5)
