from django.contrib import admin

from mob_app.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
# Register your models here.
