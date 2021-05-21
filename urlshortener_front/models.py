from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.forms import URLField


class User(AbstractUser):
    pass


class URLdata(models.Model):
    user = models.ForeignKey("User",null=True,blank=True,on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    slug = models.CharField(max_length=15)
    clicks = models.IntegerField(null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    visitors = models.IntegerField(null=True,default=0)


    @classmethod
    def Visited(self, *args, **kwargs):
        self.visitors += 1
        self.save()
    def Clicked(self):
        self.clicks += 1
        self.save()

    def validate_url(self):
        url_form_field = URLField()
        try:
            self.url = url_form_field.clean(self.url)
        except ValidationError:
            return False
        return True

    def __str__(self):
        return f"Short Url for: {self.url} is {self.slug}"

