# Generated by Django 4.2.11 on 2024-04-28 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0003_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer',
            new_name='user',
        ),
    ]