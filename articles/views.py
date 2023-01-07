from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from articles.models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    """
    A class-based view in Django that displays a list of "Article" objects.

    This view requires the user to be logged in (via the "LoginRequiredMixin"
    mixin) and uses the template "article_list.html" to render the list of
    articles.

    Attributes:
        model: The model that the view is using.
        template_name: The template name used to render the view.
    """
    model = Article
    template_name = 'articles/article_list.html'
