from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'

    USER_TYPE_SUPER = 1
    USER_TYPE_ADMIN = 2
    USER_TYPE_USER = 3
    USER_TYPES = (
        (USER_TYPE_SUPER, 'super'),
        (USER_TYPE_ADMIN, 'admin'),
        (USER_TYPE_USER, 'user'),
    )
