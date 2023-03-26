from django.contrib import admin
from .models import UserHistoryTable, QuickInviteLogs
# Register your models here.


admin.register([UserHistoryTable])
admin.register(QuickInviteLogs)