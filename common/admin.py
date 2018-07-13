from django.contrib import admin

from .models import Site, Doctor, Dosimetrist

from .forms import SiteForm

class SiteAdmin(admin.ModelAdmin):
    form = SiteForm
    fieldsets = (
        (None, {
            'fields': ('name','color')
        }),
    )

admin.site.register(Site, SiteAdmin)
admin.site.register(Doctor)
admin.site.register(Dosimetrist)
