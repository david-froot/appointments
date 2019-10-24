from django.contrib.auth.admin import UserAdmin
from users.models import User as MyUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin

class MyUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        model = MyUser


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('role','phone_number', 'address', 'city', 
            					'state', 'zipcode')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'first_name', 'last_name', 
                        'email', 'phone_number', 'address', 'city', 'state', 'zipcode')}
        ),
    )

admin.site.register(MyUser, MyUserAdmin)
