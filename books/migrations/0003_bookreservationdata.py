# Generated by Django 4.0.3 on 2022-04-30 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_bookdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookreservationdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentid', models.IntegerField()),
                ('booktitle', models.CharField(max_length=500)),
            ],
        ),
    ]
