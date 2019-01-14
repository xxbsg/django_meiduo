from django.core.mail import send_mail

from celery_tasks.main import app
from shangcheng import settings


@app.task
def fsyx(email,verify_url,):
    # 发送邮箱
    msg = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    # msg = '<a href="http://www.itcast.cn/subject/pythonzly/index.shtml" target="_blank">点击激活</a>'
    send_mail('美多商场激活邮件', '', settings.EMAIL_FROM, ['%s'%email], html_message=msg)