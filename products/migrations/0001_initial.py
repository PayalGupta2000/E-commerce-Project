# Generated by Django 4.0.3 on 2022-03-24 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('brand_logo', models.ImageField(upload_to='media/brand')),
                ('reg_date', models.DateTimeField()),
            ],
        ),
    ]