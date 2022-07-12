# Generated by Django 4.0.3 on 2022-04-13 06:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_cart_alter_myuser_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='Men', max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='myuser',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 13, 11, 32, 34, 34404)),
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]
