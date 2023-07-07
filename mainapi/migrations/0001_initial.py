# Generated by Django 4.2.3 on 2023-07-04 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30, verbose_name='Имя пользователя')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=30, verbose_name='Товар')),
                ('total', models.FloatField(verbose_name='Сумма сделки')),
                ('quantity', models.IntegerField(verbose_name='Количество товара')),
                ('date', models.DateTimeField(verbose_name='Дата и время совершения сделки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapi.user', verbose_name='Пользователь')),
            ],
        ),
    ]
