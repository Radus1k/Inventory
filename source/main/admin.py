from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Element)
admin.site.register(Room)
admin.site.register(Floor)
admin.site.register(Building)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(EntityUserRequest)
