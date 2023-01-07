from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from articles.forms import CommentForm
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


class ArticleDetailGet(DetailView):
    """
    A class-based view in Django that displays the details of a
    single "Article" object.

    This view renders the details of the article and includes a form for
    adding comments to it.

    Attributes:
        model: The model that the view is using.
        template_name: The template name used to render the view.

    """
    model = Article
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        """
        This method adds a 'CommentForm' form object (for adding comments
        in articles) to the context data passed to the template when rendering
        the view.

        :param kwargs: Additional keywords arguments.
        :return: This method returns a dictionary with the context data used
            in the template rendering.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class ArticleDetailPost(SingleObjectMixin, FormView):
    """
    A class-based view in Django that handles form submission for adding
    comments to a single "Article" object.

    This view uses the 'SingleObjectMixin' to retrieve the commented
    'Article' object and the 'CommentForm' form to handle comment submissions.

    Attributes:
        model: The model that the view is using.
        form_class: The form class to use for handling the comment submission.
        template_name: The template name used to render the view.
    """
    model = Article
    form_class = CommentForm
    template_name = 'articles/article_detail.html'

    def post(self, request, *args, **kwargs):
        """
        This method handles POST requests for the view, retrieving the
        'Article' object being commented on and calling its parent's
        implementation.

        :param request: The incoming request.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The HTTP response.
        """
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        A method called when the form submission is valid.

        It attaches the article and the comment author (authenticated user)
        to the comment and saves it to the database. It then calls the parent's
        implementation of the method.

        :param form: The form being submitted.
        :return: The HTTP response.
        """
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        This method returns the URL for the detail page of the commented
        article after successful comment form submission.

        :return: It returns the URL for the detail page of the
            commented article.
        """
        article = self.get_object()
        success_url = reverse(
            viewname='article_detail',
            kwargs={
                'pk': article.pk
            }
        )
        return success_url


class ArticleDetailView(LoginRequiredMixin, View):
    """
    A class-based view in Django that handles both GET and POST requests for the detail page of an 'Article' object.

    This view requires the user to be logged in (via the 'LoginRequiredMixin'
    mixin) and uses the 'ArticleDetailGet' and 'ArticleDetailPost' views
    to handle the GET and POST requests, respectively.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the view.

        This method calls the 'ArticleDetailGet' view to handle the request.

        :param request: The incoming GET request.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The HTTP response.n:
        """
        view = ArticleDetailGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for the view.

        This method calls the 'ArticleDetailPost' view to handle the request.

        :param request: The incoming POST request.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The HTTP response.
        """
        view = ArticleDetailPost.as_view()
        return view(request, *args, **kwargs)
