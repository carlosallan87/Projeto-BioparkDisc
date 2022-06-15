# Generated by Django 4.0.2 on 2022-03-16 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.CharField(max_length=30)),
                ('perfil', models.IntegerField(choices=[(1, 'dominância'), (2, 'influência'), (3, 'cautela'), (4, 'estabilidade')])),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('ra', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Teste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.CharField(max_length=50)),
                ('ano', models.IntegerField()),
                ('semestre', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ini', models.DateTimeField()),
                ('data_fim', models.DateTimeField()),
                ('influencia', models.FloatField()),
                ('dominancia', models.FloatField()),
                ('cautela', models.FloatField()),
                ('estabilidade', models.FloatField()),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projeto5_website.aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField(max_length=140)),
                ('teste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projeto5_website.teste')),
            ],
        ),
        migrations.AddField(
            model_name='aluno',
            name='turma',
            field=models.ManyToManyField(to='projeto5_website.Turma'),
        ),
    ]