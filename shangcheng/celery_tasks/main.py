from celery import Celery


#进行Celery允许配置
# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shangcheng.settings'
# 实例化出一个芹菜
app=Celery(main='celery_tasks') #参数 main脚本名称 为包名 实际要求一个具有唯一性的名称
# 加载配置文件
app.config_from_object('celery_tasks.config')
#自动加载任务
app.autodiscover_tasks(['celery_tasks.duanxin'])

