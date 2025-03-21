from django.db import models
from django.utils.translation import gettext_lazy as _


class Userroles(models.IntegerChoices):
    ADMIN = 1, _("admin")
    Customer = 2, _("Intermediate")
