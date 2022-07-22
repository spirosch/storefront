from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user όπου παίρνει το ξένο σώμα από το User που κάναμε define από το auth.models import User
    # CASCADE γιατί θέλουμε μόλις σβηστεί ο χρήστης να σβηστούν και τα likes του
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # content_type παίρνει το περιεχόμενο από το ContentType from contenttypes.models
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey()

