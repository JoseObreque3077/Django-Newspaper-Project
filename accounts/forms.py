from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    A Custom user signup class-based form that extends the Django
    UserCreationForm class, adding a user age field.
    """
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'age'
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user edit class-based form that extends the Django UserChangeForm
    class, adding a user age field.
    """
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'age'
        )
