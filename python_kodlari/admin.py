from django.contrib import admin
from tracks.models import Track,TrackUserModel


# admin.site.register(Track)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['id','name','genres','artist']
    ordering = ['genres']




@admin.register(TrackUserModel)
class TrackUserModelAdmin(admin.ModelAdmin):
    list_display = ['User', 'Track', 'rating']  
    ordering = ['User'] 
    