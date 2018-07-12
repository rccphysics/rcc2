from django.contrib import admin

from .models import Site, Doctor, Dosimetrist

from .forms import SiteForm

admin.site.register(Site)
admin.site.register(Doctor)
admin.site.register(Dosimetrist)

class SiteAdmin(admin.ModelAdmin):
    form = SiteForm
    fieldsets = (
        (None, {
            'fields': ('name', 'color')
        }),
    )
