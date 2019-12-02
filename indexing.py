import os
import django
from django.db import transaction

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySearchEngine.settings")
django.setup()

# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from searchApp.models import Content

@transaction.atomic
def update_my_model_data():
    for i in os.listdir("/Users/parkjeongseop/Desktop/Dev/NLP/hw6/ITnews623_sim383/"):
        try:
            this_doc = open('/Users/parkjeongseop/Desktop/Dev/NLP/hw6/ITnews623_sim383/'+i, 'r', encoding='cp949').read()
            this = Content()
            this.title = i
            this.content = this_doc
            this.save()
            print(i)
            
        except:
            print("ERROR", i)

if __name__ == "__main__":
    update_my_model_data()

