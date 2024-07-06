from django.contrib import admin
from .models import Block, Flour, House
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(Block)
admin.site.register(Flour)
admin.site.register(House)
