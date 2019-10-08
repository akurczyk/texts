from django.contrib import admin

from .models import Text, Vote, Comment

admin.site.register(Text)
admin.site.register(Vote)
admin.site.register(Comment)
