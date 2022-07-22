from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from settings.py --> INSTALLED_APPS --> django.contrib.contenttypes
# this model is specifically made for allowing generic relationships.


# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=255)



class TaggedItem(models.Model):
    # with TaggedItem class --> we can find out What tag applied to what object
    tag= models.ForeignKey(Tag, on_delete=models.CASCADE)
    # CASCADE because if we delete a tag, we want to remove it from all the associated objects.
    
    # Παρακάτω θέλουμε 1) Type (product, video, article) και 2)ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #  για αρχή θέλουμε να κάνουμε associate το Product με το Product από το models.py αλλά επειδή
    # στο μέλλον μπορεί να μην είναι product, να είναι μια άλλη κλάση από το models.py, για αυτό το λόγο
    # κάνουμε import πάνω πάνω το from django.contrib.contenttypes.models import ContentType
    # και έτσι δημιουργούμε generic Relationships.
    object_id = models.PositiveIntegerField()
    # PositiveIntegerField() because we're assuming that every table is going to have a primary key,
    # and all primary keys are positive integers.
    content_object = GenericForeignKey()
    # when quering data, we might want to get the actual object that this tag is applied like the actual product
    # To do that we add the content_object field 
    # Using this field, content_object, we CAN READ the actual object that a particular tag is applied to.

