from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Meep, Comment


# Unregister Groups
admin.site.unregister(Group)

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username field on admin page
    # fields = ["username"]
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)

# Register Meeps
admin.site.register(Meep)

# Register Comment
admin.site.register(Comment)
