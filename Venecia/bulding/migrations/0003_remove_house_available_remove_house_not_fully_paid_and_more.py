# Generated by Django 5.0.6 on 2024-07-01 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulding', '0002_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='available',
        ),
        migrations.RemoveField(
            model_name='house',
            name='not_fully_paid',
        ),
        migrations.RemoveField(
            model_name='house',
            name='sold',
        ),
        migrations.AddField(
            model_name='block',
            name='reserved',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flour',
            name='reserved',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='house',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('sold', 'Sold'), ('reserved', 'Reserved'), ('not_fully_paid', 'Not Fully Paid')], default='available', max_length=15),
        ),
    ]