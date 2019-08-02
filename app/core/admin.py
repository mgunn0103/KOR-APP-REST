from django.contrib import admin

# import the default Django UserAdmin class, but give it an alias of BaseUserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
# this is the recommended convention for converting string in our python to human-readable text
from django.utils.translation import gettext as _

"""We need to change some of the admin class variables to support our custom 
    user model
"""

""" We are creating our own UserAdmin class. Notice that we import the existing UserAdmin 
    class made available by Django as BaseUserAdmin, so that there are no conflicts
"""
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        # this has something to do with the top of the page
        (None, {'fields': ('email', 'password')}),
        # this is for the personal info. Be sure to add the trailing comma, so that it is not mistaken fort string
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'), 
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    """ The UserAdmin by default takes an add field sets which defines the fields that you
        include on the add page which is the same as the create user page. All we are going 
        to do is customize this field set to include our email address, password, and password2
        so you can create a new user in the system with very minimal required data. Later, if 
        you want to add extra fields like the name or any other fields, you can do that later in
        the Edit Page 
    """
    """ The first field is the title of the section None. The second part is the definition
        of the fields that we want to include in the form
    """
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# this registers the UserAdmin class to the User model for the admin site
admin.site.register(models.User, UserAdmin)

