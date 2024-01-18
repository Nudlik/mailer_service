from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта')
    email_verify = models.BooleanField(default=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        **NULLABLE,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        permissions = [
            ('can_view_all_fields', 'Может просматривать всю админку')
        ]
