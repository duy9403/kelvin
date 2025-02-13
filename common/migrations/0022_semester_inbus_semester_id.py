# Generated by Django 4.2.16 on 2025-02-13 13:33

from django.db import migrations, models


def semester_str(semester):
    return f"{semester.year}{'W' if semester.winter else 'S'}"


def set_default_values(apps, schema_editor):
    kelvin_to_inbus_semester_ids = {'2019W': 118, '2019S': 119, '2020W': 120, '2020S': 121, '2021W': 122, '2021S': 123,
                                    '2022W': 124, '2022S': 128, '2023W': 125, '2023S': 129, '2024W': 126}
    Semester = apps.get_model('common', 'Semester')
    for semester in Semester.objects.all():
        semester.inbus_semester_id = kelvin_to_inbus_semester_ids[semester_str(semester)]
        semester.save()


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0021_task_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='inbus_semester_id',
            field=models.IntegerField(null=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_default_values),
        migrations.AlterField(
            model_name='semester',
            name='inbus_semester_id',
            field=models.IntegerField(),  # Make it non-nullable after setting values
        ),
    ]
