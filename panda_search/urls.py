from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('query_input/', views.query_input, name='query_input'),
    path('results/', views.query_results, name='results'),
    path('article/<int:article_id>/', views.article_data, name='article data'),
]