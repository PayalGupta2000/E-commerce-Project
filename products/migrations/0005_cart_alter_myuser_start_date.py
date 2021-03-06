# Generated by Django 4.0.3 on 2022-04-06 05:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_myuser_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('quanitity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('user_email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='myuser',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 6, 11, 23, 21, 88526)),
        ),
    ]
