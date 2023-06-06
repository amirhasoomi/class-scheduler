from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    SAT = 1
    SUN = 2
    MON = 3
    TUE = 4
    WED = 5
    THU = 6
    FRI = 7
    WEEK_DAYS = (
        (SAT, 'sat'),
        (SUN, 'sun'),
        (MON, 'mon'),
        (TUE, 'tue'),
        (WED, 'wed'),
        (THU, 'thu'),
        (FRI, 'fri'),
    )
