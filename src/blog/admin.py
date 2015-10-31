from django.contrib import admin

from blog.models import PostMeta, Post, TagMeta, Tag


class TagMetaAdmin(admin.ModelAdmin):
    list_display = ('slug', )


class TagAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('title', 'slug')


class PostMetaAdmin(admin.ModelAdmin):
    list_display = ('slug', )


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('title', 'slug')


admin.site.register(TagMeta, TagMetaAdmin)
admin.site.register(Tag, TagAdmin)

admin.site.register(PostMeta, PostMetaAdmin)
admin.site.register(Post, PostAdmin)
