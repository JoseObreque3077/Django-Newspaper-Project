from django.urls import path

from articles.views import ArticleListView, ArticleDetailView

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
    )
]
