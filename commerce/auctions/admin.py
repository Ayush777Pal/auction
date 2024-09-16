from django.contrib import admin

from .models import User, listing, house, Comment, Bid
# Register your models here.
admin.site.register(User)
admin.site.register(listing)
admin.site.register(house)
admin.site.register(Comment)
admin.site.register(Bid)
