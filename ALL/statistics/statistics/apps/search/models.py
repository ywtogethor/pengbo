from django.db import models

# Create your models here.

class SearchStat(models.Model):
    keyword = models.CharField(max_length=1024)
    number = models.IntegerField()
    date = models.IntegerField()
    
    def __unicode__(self):
        return self.keyword+"|"+str(self.number)
    class Meta:
        ordering = ['-number']
