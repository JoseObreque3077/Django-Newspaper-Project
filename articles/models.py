from django.conf import settings
from django.db import models
from django.urls import reverse


class Article(models.Model):
    """
    This class represents an article object.

    Attributes:
        title: The title of the article.
        body: The body or content of the article.
        date: The article creation date and time.
        author: The user who is the author of the article.
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Título'
    )
    body = models.CharField(
        verbose_name='Texto'
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        It returns the string representation of an 'Article' object.
        :return: The title of the article.
        """
        return self.title

    def get_absolute_url(self):
        """
        It returns the absolute URL of the detail page for an Article object.
        :return: The absolute URL of the detail page for the article.
        """
        article_detail_url = reverse(
            viewname='article_detail',
            kwargs={
                'pk': self.pk
            }
        )
        return article_detail_url
