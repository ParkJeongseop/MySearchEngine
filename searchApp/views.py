from django.shortcuts import render

# Create your views here.
def search(request):
    return render(request, 'search.html')

def result(request):
    keyword = request.GET['query']
    print(keyword)
    return render(request, 'result.html', {'keyword': keyword})