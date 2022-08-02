from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from modeltranslation.admin import TranslationAdmin
from .models import User


class UserAdmin(TranslationAdmin, BaseUserAdmin):
    list_display = ('username' , 'last_online')

    fieldsets = (
                ('User Info',{
                    'fields': ('username', 'first_name', 'last_name','email')
                 }),
                 ('Password',{
                     'fields': ('password', )
                 }),
                 ('User Permission',{
                     'fields': ('groups',)
                 }),
                 ('User Block',{
                     'fields': ('is_active','is_staff', 'is_superuser')
                 }),
                ('inform', {
                    'fields': ('about_us',)
                }),
                 ('Date public and visit',{
                     'fields': ('date_joined', 'last_login')
                 }),
                ('Locations', {
                    'fields': ('country', 'location', 'language')
                }),
                 ('Online Status',{
                     'fields': ('last_online', )
                 }),
                ('User Avatar',{
                    'fields': ('image', )
                })
                 )



admin.site.register(User, UserAdmin)
