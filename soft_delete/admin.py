from django.contrib import admin
from .filters import SoftDeleteAdminFilter


class SoftDeleteModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.all_objects.all()

    @admin.action(description='Soft delete selected')
    def action_soft_delete(self, request, queryset):
        result = queryset.delete()
        self.message_user(request, f'Soft deleted {result[0]} record')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        actions['action_soft_delete'] = self.get_action('action_soft_delete')
        return actions

    def get_list_filter(self, request):
        return [SoftDeleteAdminFilter] + list(super().get_list_filter(request))
