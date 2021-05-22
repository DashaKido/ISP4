from djangotoolbox.fields import ListField
from django.db import models


class Post(models.Model):
    tags = ListField(models.DateTimeField())