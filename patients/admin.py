from django.contrib import admin
from models import PatientInformation, HealthHistory, Medication, Allergy, Surgery, FamilyHistory

class PatientInfoAdmin(admin.ModelAdmin):
    pass

class HealthHistoryAdmin(admin.ModelAdmin):
    pass

class MedicationAdmin(admin.ModelAdmin):
    pass

class AllergyAdmin(admin.ModelAdmin):
    pass

class SurgeryAdmin(admin.ModelAdmin):
    pass

class FamilyHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(PatientInformation, PatientInfoAdmin)
admin.site.register(HealthHistory, HealthHistoryAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Allergy, AllergyAdmin)
admin.site.register(Surgery, SurgeryAdmin)
admin.site.register(FamilyHistory, FamilyHistoryAdmin)