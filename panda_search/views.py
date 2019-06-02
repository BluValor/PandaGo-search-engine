from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import panda_search.src.django_process_query as dpq
from .forms import QueryForm
from .models import ArticleBox


def index(request):
    return HttpResponse("Welcome to PandaGo_TM")


def query_results(request):
    query_text = request.GET['query_text']
    results_list = dpq.process_query(query_text)
    return render(request, 'results.html', {'results_list': results_list})


def query_input(request):
    form = QueryForm(request.GET)
    return render(request, 'query.html', {'form': form})


def article_data(request, article_id):
    article = ArticleBox.objects.get(id=article_id)
    return render(request, 'article_data.html', {'article': article})
