from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):
    """
    Unit test case for the 'HomeView' class that handles the website
    homepage render and other general-purpose pages.
    """
    HOMEPAGE_URL = reverse('home')

    @classmethod
    def setUpTestData(cls):
        """
        This method creates objects in a test database that are available to
        all unit tests. It is called only once for this test case, and the
        created objects are shared among all unit tests in this test case.
        """
        # Custom user model used by this project
        user_model = get_user_model()

        # Test user
        cls.user = user_model.objects.create(
            username='test_user',
            email='test@example.net',
            age=18
        )
        # Use of non-encrypted password
        cls.user.set_password('test_pass')
        cls.user.save()

    def test_homepage_render_user_not_authenticated(self):
        """
        Checks that a non-authenticated user can access the website homepage.
        """
        # HTTP Response
        response = self.client.get(self.HOMEPAGE_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='home.html'
        )

    def test_homepage_render_user_authenticated(self):
        """
        Checks that an authenticated user can access the website homepage.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(self.HOMEPAGE_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='home.html'
        )