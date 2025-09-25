from django.contrib import admin
from .models import Restaurant, OpeningWindow, Review, Tag

class OpeningWindowInline(admin.TabularInline):
    model = OpeningWindow
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [OpeningWindowInline]

    def get_inline_instances(self, request, obj=None): # add画面
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

admin.site.register(Restaurant, RestaurantAdmin)
# admin.site.register(OpeningWindow)
# admin.site.register(Review)
# admin.site.register(Tag)