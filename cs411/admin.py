from django.contrib import admin
from .models import stu
from .models import food
from .models import comment
from .models import likelist
admin.site.register(likelist)
admin.site.register(stu)
admin.site.register(food)
admin.site.register(comment)
# Register your models here.
