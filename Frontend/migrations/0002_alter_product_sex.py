# Generated by Django 4.2.11 on 2024-04-23 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sex',
            field=models.CharField(max_length=5),
        ),
    ]
