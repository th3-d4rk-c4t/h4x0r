from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models


from conf.models import BaseModel


class Member(BaseModel, AbstractBaseUser):
    USERNAME_FIELD = 'username'
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9\-_]+$",
                message="Special characters (except space & dash) are not accepted",
            ),
        ],
    )
    question = models.CharField(max_length = 500, default=None)
    answer = models.CharField(max_length = 50, default=None)

    class Meta:
        db_table = "members"

    def __str__(self):
        return self.username
