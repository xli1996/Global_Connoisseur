from django.db import models

class stu(models.Model):
    user = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    spicy = models.IntegerField()
    sweet = models.IntegerField()
    salty = models.IntegerField()
    num_like = models.IntegerField(default=0)
    def __str__(self):
        return self.user
# Create your models here.

class food(models.Model):
    name = models.CharField(max_length=40,primary_key=True)
    country = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    ingredient = models.CharField(max_length=20)
    headImg = models.FileField(upload_to = './static/picture/', default="")
    spicy = models.IntegerField()
    sweet = models.IntegerField()
    salty = models.IntegerField()
    num_like = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class comment(models.Model):
    user = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    context = models.CharField(max_length=255)
    class Meta:
        unique_together =('user','name')

class likelist(models.Model):
    user = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    class Meta:
        unique_together =('user','name')



    # pic_path = models.CharField(max_length=100)
    def __str__(self):
        return self.name

