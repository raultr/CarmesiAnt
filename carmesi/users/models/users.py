"""User model """

# standar library

# third.party

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Exceptions

# Utilities
from utilerias.models import CarmesiAudit



class User(CarmesiAudit, AbstractUser):
    email = models.EmailField(
        'email adress',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con ese email'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="El formato del numero de telefono debe de ser: +999999999. de 9 a 15 digitos."
)

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name','last_name']

    is_client = models.BooleanField(
        'client status',
        default= True,
        help_text=('Si es un cliente del sistema')
        )

    is_verified = models.BooleanField(
        'verificado',
        default=False,
        help_text='Si el usuario ya verifico que es su correo'
        )

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
