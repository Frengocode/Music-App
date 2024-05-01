from django.contrib import admin
from .models import CustomUser, PlayList, CommentModel, GetPrimePluse

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'play_list')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('play_list',)

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('music_title', 'created_at', 'category')
    search_fields = ('music_title',)
    list_filter = ('created_at', 'category')

@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'music', 'created_at', 'text')
    search_fields = ('user__username', 'music__music_title', 'text')
    list_filter = ('created_at',)



admin.site.register(GetPrimePluse)