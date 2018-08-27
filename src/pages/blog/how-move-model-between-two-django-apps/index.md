---
title: How to move a model between two Django apps
subtitle: And save references with content types and other entries
lead: Moving a model between two Django apps isn't a trivial task, at the moment of writing (actual for Django 1.10 and the earlier versions). It becomes more difficult, if you need to keep references with content types or other entries.
date: "2016-09-25"
shareImage: "./../../../media/images/django-logo-negative.png"
---

### Warning

Do not perform any operations on a production database, test everyting on a dump first.

### The wrong way

If you have a Django app (I'll call it **app1**, in my example) with a lot of models and if you want to move some of these models into a separate app (will be **app2**) you can't just cut a model definition from the **app1**, paste it into a new application and then run the **makemigrations** command. Django will simply remove your table and will create a new one. As a result of these operations, you'll lose your data.

#### Why does it happen?

Whenever you run the **makemigrations** command, Django applies all migrations internally to build a project state, then compares the state to the state presented in your code. All the differences will be written in new migration files.

Django manages migrations on a per-app basis and it "thinks" that one model has been removed from **app1** and a new one has been added to **app2**.

So your cut-and-paste operation will lead to the same result as the following operations:

1. Remove your model definition from **app1**;
2. Run the **makemigrations** command _(here Django will generate a migration that removes your data)_;
3. Add your model definition to **app2**;
4. Run the **makemigrations** command again.

### The right way

It will be easier to explain the solution with an example. In my **app1** application I have the following **models.py**:

```python
from django.contrib.contenttypes.models import ContentType
from django.db import models


def get_default_page_content_type():
    return ContentType.objects.get_for_model(DefaultContentType)


class DefaultContentType(models.Model):
    pass


class ModelWithContentType(models.Model):
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        related_name='+',
        on_delete=models.SET(get_default_page_content_type)
    )


class RelatedModel(models.Model):
    relation = models.ForeignKey(
        'app1.ModelThatShouldBeMoved',
        related_name='relations',
        on_delete=models.CASCADE
    )


class ModelThatShouldBeMoved(models.Model):
    title = models.CharField(max_length=255)
```

As you may notice from the names of models, I want to move the **ModelThatShouldBeMoved** model into **app2**. This model is related to the **RelatedModel** model which will stay in **app1.** Also we have an indirect reference (through the **ModelWithContentType.content_type** field) from **ModelWithContentType**. And we need to keep all these direct and indirect relations!

You can create a test data set using the following snippet (run **python manage.py shell** and insert the code):


```python
from django.contrib.contenttypes.models import ContentType

from app1.models import ModelWithContentType, ModelThatShouldBeMoved, RelatedModel

# We need to keep the same content type id for ModelThatShouldBeMoved
content_type = ContentType.objects.get_for_model(ModelThatShouldBeMoved)
ModelWithContentType.objects.create(content_type=content_type)

# We need to keep relations with other objects
test_entry = ModelThatShouldBeMoved.objects.create(title='Test entry')
relation = RelatedModel.objects.create(relation=test_entry)
```

As a result, you will have the following entries in the database:

```bash
django_migration_test=# select * from app1_modelthatshouldbemoved;
 id |   title
----+------------
  1 | Test entry
(1 row)

django_migration_test=# select * from app1_relatedmodel;
 id | relation_id
----+-------------
  1 |           1
(1 row)

django_migration_test=# select * from app1_modelwithcontenttype;
 id | content_type_id
----+-----------------
  1 |               8
(1 row)

django_migration_test=# select * from django_content_type where app_label in ('app1', 'app2');
 id | app_label |         model
----+-----------+------------------------
  7 | app1      | defaultcontenttype
  8 | app1      | modelthatshouldbemoved
  9 | app1      | relatedmodel
 10 | app1      | modelwithcontenttype
(4 rows)
```

#### TL;DR;

If you are familiar with Django migrations, here is the list of steps to get the job done:

1. Create a migration in **app1** which will rename a table in the database for **ModelThatShouldBeMoved**. This migration should change only the database, not the project state;
2. Create a migration in **app2** which will add a model to the state and will update content types in the database. I'll also rename the **ModelThatShouldBeMoved** model to **ModelThatWasMoved** in my example;
3. Create migrations in **all the apps** that have relations with the model that you want to move. Migrations should change relations in the state;
4. Create a migration that removes the **ModelThatShouldBeMoved** model from the state;
5. Update your code.

Some migrations will use the [SeparateDatabaseAndState](https://docs.djangoproject.com/en/1.10/ref/migration-operations/#separatedatabaseandstate) operation**.**

#### Step 1

First, I need to rename a table in the database for the **ModelThatShouldBeMoved** model.

This step isn't necessary, if you specified the [Meta.db_table](https://docs.djangoproject.com/en/1.10/ref/models/options/#db-table) attribute in your model before. By default, Django generates a table name using an app label and a model’s class name, with an underscore between them ([see the docs](https://docs.djangoproject.com/en/1.10/ref/models/options/#table-names) for details). If you don't care about the table name, you can simply add the **Meta.db_table** attribute to your model and generate a new migration automatically.

In my case I have a table with a name **app1_modelthatshouldbemoved**. I want to rename the **ModelThatShouldBeMoved** model to **ModelThatWasMoved** and put it into the **app2**, so I need the name to be **app2_modelthatwasmoved** to match Django's naming convention.

Here is the migration for my case (**0002_rename_table.py** in the **app1** app):

```python
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # This migration should depend on the previous migration in our app
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(name='ModelThatShouldBeMoved', table='app2_modelthatwasmoved'),
    ]
```


#### Step 2

Now I need to add a migration that creates a model in the state for **app2** and updates content types in the database.

I've called my migration **0001_move_a_model_and_rename.py**, because it's the first migration in my **app2**. In your case it may be a migration with a different number. Also you will probably need to specify the previous migration in your app as a dependency.

```python
from __future__ import unicode_literals

from django.db import migrations, models


def update_contentypes(apps, schema_editor):
    """
    Updates content types.
    We want to have the same content type id, when the model is moved and renamed.
    """
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias

    # Move the ModelThatShouldBeMoved model to app2 and rename to ModelThatWasMoved
    qs = ContentType.objects.using(db_alias).filter(app_label='app1', model='modelthatshouldbemoved')
    qs.update(app_label='app2', model='modelthatwasmoved')


def update_contentypes_reverse(apps, schema_editor):
    """
    Reverts changes in content types.
    """
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias

    # Move the ModelThatWasMoved model to app1 and rename to ModelThatShouldBeMoved
    qs = ContentType.objects.using(db_alias).filter(app_label='app2', model='modelthatwasmoved')
    qs.update(app_label='app1', model='modelthatshouldbemoved')


class Migration(migrations.Migration):

    dependencies = [
        # We need to run 0002_rename_table form app1 first,
        # because it changes the table of ModelThatShouldBeMoved.
        # Only after that we will update content types and rename the model.
        ('app1', '0002_rename_table'),
        # This migration also depends on the contenttype app,
        # so we need to specify dependency on 0002_remove_content_type_name.
        # If you use Django < 1.8, you will probably need to specify 0001_initial.
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='ModelThatShouldBeMoved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameModel(
            old_name='ModelThatShouldBeMoved',
            new_name='ModelThatWasMoved',
        ),
    ]

    database_operations = [
        migrations.RunPython(update_contentypes, update_contentypes_reverse),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
            database_operations=database_operations
        ),
    ]
```

Note that the **CreateModel** operation should reflect your model definition. Otherwise you may lose your data.

As an alternative to the **CreateModel** operation, you can copy and paste all the operations related to your model since the first migration (usually **0001_initial**) in your application.

Note also that if you do not need to rename your model, you need to remove the **RenameModel** operation and remove the **model** argument from the **update** calls in the **update_contentypes** and **update_contentypes_reverse** functions.

#### Step 3

I need to create migrations for **all the apps that have models which have relations with the model that I want to move**.

In my example, I have only one app that contains only one field which refers the old **ModelThatShouldBeMoved** model. My migration (**0003_update_relations.py** in **app1**):

```python
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # The previous migration in app1
        ('app1', '0002_rename_table'),
        # This migration should depend on the migration that creates a model in the state of app2,
        # because we are going to refer a new model here.
        ('app2', '0001_move_a_model_and_rename'),
    ]

    state_operations = [
        migrations.AlterField(
            model_name='relatedmodel',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations',
                                    to='app2.ModelThatWasMoved'),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
```

Note that the **AlterField** operation should contain the same field definition as your model. The only difference is reference to your model. So this definition:

```python
models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations',
                                    to='app1.ModelThatShouldBeMoved')
```

should be replaced with this one, in my case:

```python
models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations',
                                    to='app2.ModelThatWasMoved')
```

#### Step 4

The last migration simply removes the model from the state of **app1** (**0004_delete_old_model_from_the_state.py**):

```python
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_update_relations'),
    ]

    state_operations = [
        migrations.DeleteModel('ModelThatShouldBeMoved'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
```

#### Step 5

####

On the final step I just need to update my code:

1. Move the model definition into a new app (**app2**, in my case);
2. Update imports;
3. Update relations (see the **RelatedModel.relation** definition, for example).

My **models.py** from **app1**:

```python
from django.contrib.contenttypes.models import ContentType
from django.db import models


def get_default_page_content_type():
    return ContentType.objects.get_for_model(DefaultContentType)


class DefaultContentType(models.Model):
    pass


class ModelWithContentType(models.Model):
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        related_name='+',
        on_delete=models.SET(get_default_page_content_type)
    )


class RelatedModel(models.Model):
    relation = models.ForeignKey(
        'app2.ModelThatWasMoved',
        related_name='relations',
        on_delete=models.CASCADE
    )
```

And **models.py** from **app2**:

```python
from django.db import models


class ModelThatWasMoved(models.Model):
    title = models.CharField(max_length=255)
```

#### Testing

To test changes you can run the **python ****manage.py makemigrations --dry-run** command. This command will try to generate migrations without actually writing them to a disk.

**Expected result:**

```bash
No changes detected
```

You can also try to run the same SQL queries as shown before (but with a new table name):

```bash
django_migration_test=# select * from app2_modelthatwasmoved;
 id |   title
----+------------
  1 | Test entry
(1 row)

django_migration_test=# select * from app1_relatedmodel;
 id | relation_id
----+-------------
  1 |           1
(1 row)

django_migration_test=# select * from app1_modelwithcontenttype;
 id | content_type_id
----+-----------------
  1 |               8
(1 row)

django_migration_test=# select * from django_content_type where app_label in ('app1', 'app2');
 id | app_label |        model
----+-----------+----------------------
  7 | app1      | defaultcontenttype
  9 | app1      | relatedmodel
 10 | app1      | modelwithcontenttype
  8 | app2      | modelthatwasmoved
(4 rows)
```

**Expected result:**

Data should be the same as before except the **django_content_type** table. This table should contain a new **app_label** and a new **model** name, but the same id (see the entry with **id=8**) for the model that has been moved.
