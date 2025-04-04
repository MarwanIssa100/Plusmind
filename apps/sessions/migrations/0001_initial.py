# Generated by Django 5.1.7 on 2025-03-23 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('reviews', '0001_initial'),
        ('therapist', '0002_rename_speciality_therapist_specialty_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_type', models.CharField(choices=[('consultation', 'Consultation'), ('treatment', 'Treatment'), ('group', 'Group')], max_length=20)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.reviews')),
                ('therapist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapist.therapist')),
            ],
        ),
    ]
