from django.contrib import admin

from .models import Genre, Movie, MovieGenre, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')
    search_fields = ('title',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return "(No image)"
    image_preview.allow_tags = True

admin.site.register(Genre)
admin.site.register(MovieGenre)
admin.site.register(Review)