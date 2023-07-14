# Generated by Django 4.2.2 on 2023-07-10 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('good_hands_app', '0005_alter_institution_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institution',
            options={'ordering': ['name'], 'verbose_name_plural': 'Institutions'},
        ),
        migrations.CreateModel(
            name='InstitutionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='good_hands_app.category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='good_hands_app.institution')),
            ],
        ),
    ]