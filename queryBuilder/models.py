from django.db import models


class Resume(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name =models.CharField(max_length=100)
    text = models.TextField()

    class Meta:
        db_table = 'resume'