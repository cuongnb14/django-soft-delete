# Django Soft Delete

A Django utility package that provides soft delete functionality for Django models. Instead of permanently removing records from the database, this package marks them as "deleted" using a timestamp field, allowing for data recovery and maintaining referential integrity.

## Features

- **Soft Delete**: Mark records as deleted without removing them from the database
- **Multiple Managers**: Access active, deleted, or all records easily
- **Admin Integration**: Built-in Django admin support with filtering
- **Batch Operations**: Delete multiple records at once
- **Restore Functionality**: Undelete previously soft-deleted records
- **Database Indexed**: Optimized queries with indexed `deleted_at` field

## Installation

```bash
pip install git+https://github.com/cuongnb14/django-soft-delete.git@v1.0.0#egg=django-soft-delete
```

Add to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'soft_delete',
]
```

## Quick Start

### 1. Create a Model

Inherit from `SoftDeleteModel` instead of Django's `models.Model`:

```python
from soft_delete.models import SoftDeleteModel

class Article(SoftDeleteModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### 2. Use Different Managers

```python
# Get only active (non-deleted) records
active_articles = Article.objects.all()

# Get all records including deleted ones
all_articles = Article.all_objects.all()

# Get only deleted records
deleted_articles = Article.deleted_objects.all()
```

### 3. Soft Delete Records

```python
article = Article.objects.get(id=1)

# Soft delete (sets deleted_at timestamp)
article.delete()

# Permanently delete from database
article.hard_delete()

# Restore a soft-deleted record
article.restore()
```

### 4. Batch Operations

```python
# Soft delete multiple records
Article.objects.filter(category='draft').delete()

# Restore multiple records
Article.deleted_objects.filter(category='important').restore()
```

## Admin Integration

### Basic Admin

```python
from django.contrib import admin
from soft_delete.admin import SoftDeleteModelAdmin
from .models import Article

@admin.register(Article)
class ArticleAdmin(SoftDeleteModelAdmin):
    list_display = ['title', 'created_at', 'deleted_at']
    list_filter = ['created_at']
```

The admin integration provides:
- **Automatic filtering** to show deleted status
- **Custom soft delete action** replacing the default delete
- **View all records** including soft-deleted ones
- **Built-in filter** to toggle between active, deleted, or all records

## API Reference

### SoftDeleteModel

Base abstract model that provides soft delete functionality.

#### Fields
- `deleted_at`: DateTimeField that stores the deletion timestamp (null for active records)

#### Managers
- `objects`: Returns only active (non-deleted) records
- `all_objects`: Returns all records including deleted ones  
- `deleted_objects`: Returns only soft-deleted records

#### Methods
- `delete()`: Soft delete the record (sets `deleted_at` to current timestamp)
- `hard_delete()`: Permanently delete the record from database
- `restore()`: Restore a soft-deleted record (sets `deleted_at` to None)

### SoftDeleteModelAdmin

Admin class that provides soft delete functionality in Django admin.

#### Features
- Shows all records (active and deleted) in the admin list view
- Replaces default delete action with soft delete action
- Adds automatic filtering by deletion status
- Provides batch soft delete operations

### SoftDeleteAdminFilter

Admin filter for viewing records by deletion status.

#### Filter Options
- **Exclude deleted**: Show only active records
- **Deleted Only**: Show only soft-deleted records
- **All**: Show both active and deleted records (default)

## Requirements

- Python 3.8+
- Django 5.0+

## License

MIT License
