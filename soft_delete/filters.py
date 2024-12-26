from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class SoftDeleteAdminFilter(admin.SimpleListFilter):
    """
        Filters objects by whether or not they have been deleted
    """
    title = _('Deleted')
    parameter_name = 'deleted_at'

    def lookups(self, request, model_admin):
        lookups = (
            ('exclude_deleted', _('Exclude deleted')),
            ('deleted_only', _('Deleted Only')),
        )
        return lookups

    def queryset(self, request, queryset):
        if self.value() == 'exclude_deleted':
            return queryset.filter(deleted_at__isnull=True)
        elif self.value() == 'deleted_only':
            return queryset.filter(deleted_at__isnull=False)
        return queryset