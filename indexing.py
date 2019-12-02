import os
import django
from django.db import transaction
from elasticsearch import Elasticsearch

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySearchEngine.settings")
django.setup()

# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from searchApp.models import Content


def make_index(es, index_name):
    """인덱스를 신규 생성한다(존재하면 삭제 후 생성) """
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    print(es.indices.create(index=index_name))


@transaction.atomic
def update_my_model_data():
    es = Elasticsearch("http://localhost:9200/")
    es.info()

    index_name = 'articles'
    make_index(es, index_name)


    doc_files = []

    for i in os.listdir("/Users/parkjeongseop/Desktop/Dev/NLP/hw6/ITnews623_sim383/"):
        try:
            print("processing", i)

            this_doc = open('/Users/parkjeongseop/Desktop/Dev/NLP/hw6/ITnews623_sim383/'+i, 'r', encoding='cp949').read()
            
            # Django Model
            this = Content()
            this.title = i
            this.content = this_doc
            this.save()

            # Elasticsearch Indexing
            doc = {'title': i,    'content': this_doc}
            es.index(index=index_name, doc_type='string', body=doc)
            
        except:
            print("ERROR", i)
    es.indices.refresh(index=index_name)


if __name__ == "__main__":
    update_my_model_data()
    
