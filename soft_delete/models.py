from django.db import models
from django.utils import timezone
from . import managers


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, default=None, editable=False, db_index=True)

    objects = managers.SoftDeleteManager()
    all_objects = models.Manager()
    deleted_objects = managers.DeletedManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])