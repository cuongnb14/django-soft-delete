from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.query.QuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, self._db).filter(deleted_at__isnull=True)


class DeletedQuerySet(models.query.QuerySet):
    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        qs.update(deleted_at=None)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return DeletedQuerySet(self.model, self._db).filter(deleted_at__isnull=False)
