from django.contrib import admin
from .models import Contestant, Challenge
from django.contrib.admin import ModelAdmin


def set_result_win(modeladmin, request, queryset):
    try:
        for each in queryset:
            each.set_results(Challenge.WIN)
    except:
        ModelAdmin.message_user(message="An Error occurred at set_result_win!")


set_result_win.short_description = "Set to WIN and update scores"


def set_result_lose(modeladmin, request, queryset):
    try:
        for each in queryset:
            each.set_results(Challenge.LOSE)
    except:
        ModelAdmin.message_user(message="An Error occurred at set_result_lose!")


set_result_lose.short_description = "Set to LOSE and update scores"


class ChallengeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['result']}),
        ('Date Information', {'fields': ['start_date', 'expire_date']}),
        ('Contestant Information', {'fields': ['attacker', 'defender']}),
        (None, {'fields': ['remark']})
    ]
    list_display = ('id', 'expire_date', 'attacker', 'defender', 'is_handled')
    list_filter = ['result']
    actions = [set_result_win, set_result_lose]


class ContestantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'score', 'phone']}),
        ('User Linkage', {'fields': ['user']})
    ]
    list_display = ('name', 'score')

admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Challenge, ChallengeAdmin)

# class ContestantInline(admin.StackedInline):
#     model = Contestant
#     can_delete = False
#     verbose_name_plural = 'contestant'
#
# # Define a new User admin
# class UserAdmin(UserAdmin):
#     inlines = (ContestantInline, )
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


