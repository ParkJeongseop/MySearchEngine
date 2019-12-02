from django.shortcuts import render, redirect
from elasticsearch import Elasticsearch
import time
from .models import Content

# Create your views here.
def search(request):
    return render(request, 'search.html')


class Result():
    score = None
    title = None
    content = None


def result(request):
    start_time = time.time()
    keyword = request.GET['query']
    print(keyword)
    # 일레스틱서치 IP주소와 포트(기본:9200)로 연결한다
    es = Elasticsearch("http://localhost:9200/")  # 환경에 맞게 바꿀 것
    es.info()

    index_name = 'articles'

    results = es.search(index=index_name, body={'query': {'match': {'content': keyword}}})
    
    _results = []
    for result in results['hits']['hits']:
        this_result = Result()
        this_result.score = result['_score']
        this_result.title = result['_source']['title']
        
        content_temp = result['_source']['content']
        pos = content_temp.find(keyword)-5
        pos = 0 if pos < 0 else pos
        content_temp = content_temp[pos:]
        content_temp = "".join(content_temp[:250].splitlines())
        this_result.content = content_temp.replace(keyword, "<b>"+keyword+"</b>")
        # this_result.full_content = result['_source']['content']
        _results.append(this_result)
        # print(this_result.score)
        # print('score:', result['_score'], 'source:', result['_source']['title'], '\n', 
        #     "".join(result['_source']['content'][:80].splitlines()))
    if not results['hits']['hits']:
        print("검색결과가 없습니다.")
    return render(request, 'result.html', {'keyword': keyword, 'num':len(results['hits']['hits']), 'searching_time': round(time.time()-start_time, 2), 'results': _results})


def viewer(request):
    title = request.GET["title"]
    query = request.GET.get("query")

    content = Content.objects.filter(title=title).all()[0].content
    content = content.replace("\n", "<p>")
    if query:
        content = content.replace(query, """<span style="background-color:yellow">""" + query + """</span>""")

    return render(request, 'content.html', {'title': title, 'content': content, 'query':query})
