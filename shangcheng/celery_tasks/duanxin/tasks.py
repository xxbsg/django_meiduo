from celery_tasks.main import app
from disanfang.yuntongxun.sms import CCP
@app.task
def fsdxyzm(mobile,dxyzm):
    # 发送验证码
    CCP().send_template_sms('%s'%mobile, ['%s' % dxyzm, 5], 1)