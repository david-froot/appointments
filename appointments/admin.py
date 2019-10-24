from django.contrib import admin
from models import Insurer, SiteVisit, PatientAppointmentSlot


class InsurerAdmin(admin.ModelAdmin):
    pass

class SiteVisitAdmin(admin.ModelAdmin):
    pass

class PatientAppointmentSlotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Insurer, InsurerAdmin)
admin.site.register(SiteVisit, SiteVisitAdmin)
admin.site.register(PatientAppointmentSlot, PatientAppointmentSlotAdmin)
