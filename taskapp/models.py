from django.db import models
from django.utils import timezone

class Task(models.Model):
    name = models.CharField(max_length = 40)
    email = models.EmailField(max_length=100)
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 400)
    link_id = models.AutoField(primary_key = True)
    datecreated = models.DateTimeField()
    datelastmodified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.link_id:
            self.datecreated = timezone.now()
        else:
            self.datecreated = self.getCreatedDate()
        self.datelastmodified = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def getCreatedDate(self):
        return self.datecreated

class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 200)

    def __str__(self):
        return self.comment
