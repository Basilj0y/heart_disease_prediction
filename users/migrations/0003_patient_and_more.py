# Generated by Django 5.1.3 on 2024-11-20 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_hospital_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Patient_ID', models.CharField(max_length=100)),
                ('Height_cm', models.FloatField()),
                ('Weight_kg', models.FloatField()),
                ('Temperature_C', models.FloatField()),
                ('Heart_Rate', models.FloatField()),
                ('Cholesterol_mg_dL', models.FloatField()),
                ('Blood_Sugar_mg_dL', models.FloatField()),
                ('Symptoms_Chest_Pain', models.IntegerField(default=0)),
                ('Symptoms_Dizziness', models.IntegerField(default=0)),
                ('Symptoms_Fatigue', models.IntegerField(default=0)),
                ('Symptoms_Nausea', models.IntegerField(default=0)),
                ('Symptoms_Palpitations', models.IntegerField(default=0)),
                ('Symptoms_Shortness_of_Breath', models.IntegerField(default=0)),
                ('Existing_Conditions_Asthma', models.IntegerField(default=0)),
                ('Existing_Conditions_Diabetes', models.IntegerField(default=0)),
                ('Existing_Conditions_High_Cholesterol', models.IntegerField(default=0)),
                ('Existing_Conditions_Hypertension', models.IntegerField(default=0)),
                ('Existing_Conditions_Thyroid', models.IntegerField(default=0)),
                ('Laboratory_Test_Results_High_Blood_Sugar', models.IntegerField(default=0)),
                ('Laboratory_Test_Results_High_Cholesterol', models.IntegerField(default=0)),
                ('Laboratory_Test_Results_Low_Iron', models.IntegerField(default=0)),
                ('Laboratory_Test_Results_Normal', models.IntegerField(default=0)),
                ('Smoking_Status_Current', models.IntegerField(default=0)),
                ('Smoking_Status_Former', models.IntegerField(default=0)),
                ('Smoking_Status_Never', models.IntegerField(default=0)),
                ('Family_History_Heart_Disease_No', models.IntegerField(default=0)),
                ('Family_History_Heart_Disease_Yes', models.IntegerField(default=0)),
                ('Blood_Pressure_Systolic', models.FloatField()),
                ('Blood_Pressure_Diastolic', models.FloatField()),
            ],
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Hospital_name',
            new_name='hospital_name',
        ),
    ]
