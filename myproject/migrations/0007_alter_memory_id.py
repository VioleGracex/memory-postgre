# Generated by Django 5.0.4 on 2024-05-05 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0006_rename_user_memory_custom_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
