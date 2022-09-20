# Generated by Django 4.1.1 on 2022-09-20 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='L', max_length=50)),
                ('done', models.BooleanField()),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]