from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("hello, you are at the poll index")

def detail(request, question_id):# detail(request=<HttpRequest object>, question_id=34)
    return HttpResponse('you are looking at question %s.' % question_id)

def results(request, question_id):
    response = 'your are looking at question %s.'
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse('you are voting on question %s.' % question_id)

