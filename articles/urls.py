from django.urls import path

from articles.views import ArticleListView, ArticleDetailView, ArticleCreateView

urlpatterns = [
    path(
        route='',
        view=ArticleListView.as_view(),
        name='article_list'
    ),
    path(
        route='details/<int:pk>',
        view=ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path(
        route='new/',
        view=ArticleCreateView.as_view(),
        name='article_new'
    )
]
