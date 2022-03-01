from django.contrib import admin
from .models import Recipe , Image , Ingredient , Instruction , Vedio
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Image)
admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(Vedio)