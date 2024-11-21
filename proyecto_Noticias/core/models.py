# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Autores(models.Model):
    id_autor = models.FloatField(primary_key=True)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'autores'


class Calificaciones(models.Model):
    id_calificacion = models.FloatField(primary_key=True)
    id_noticia = models.ForeignKey('Noticias', models.DO_NOTHING, db_column='id_noticia')
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    calificacion = models.BooleanField(blank=True, null=True)
    fecha_calificacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calificaciones'


class Comentarios(models.Model):
    id_comentario = models.FloatField(primary_key=True)
    id_noticia = models.ForeignKey('Noticias', models.DO_NOTHING, db_column='id_noticia')
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    comentario = models.TextField()
    fecha_comentario = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comentarios'


class CorreosAutomaticos(models.Model):
    id_envio = models.FloatField(primary_key=True)
    id_noticia = models.ForeignKey('Noticias', models.DO_NOTHING, db_column='id_noticia')
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    fecha_envio = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'correos_automaticos'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Envios(models.Model):
    id_envio = models.FloatField(primary_key=True)
    id_noticia = models.ForeignKey('Noticias', models.DO_NOTHING, db_column='id_noticia')
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    fecha_envio = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'envios'


class Noticias(models.Model):
    id_noticia = models.FloatField(primary_key=True)
    id_tema = models.ForeignKey('Temas', models.DO_NOTHING, db_column='id_tema')
    id_subtema = models.ForeignKey('Subtemas', models.DO_NOTHING, db_column='id_subtema')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(blank=True, null=True)
    autor = models.ForeignKey(Autores, models.DO_NOTHING)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    numero_visitas = models.FloatField(blank=True, null=True)
    numero_envios = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'noticias'


class Portada(models.Model):
    id_portada = models.FloatField(primary_key=True)
    id_noticia = models.ForeignKey(Noticias, models.DO_NOTHING, db_column='id_noticia')
    fecha_agregado = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portada'


class Subtemas(models.Model):
    id_subtema = models.FloatField(primary_key=True)
    id_tema = models.ForeignKey('Temas', models.DO_NOTHING, db_column='id_tema')
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'subtemas'


class Suscripciones(models.Model):
    id_suscripcion = models.FloatField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    id_tema = models.ForeignKey('Temas', models.DO_NOTHING, db_column='id_tema', blank=True, null=True)
    id_subtema = models.ForeignKey(Subtemas, models.DO_NOTHING, db_column='id_subtema', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suscripciones'


class Temas(models.Model):
    id_tema = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'temas'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)


    class Meta:
        managed = False
        db_table = 'usuarios'


class Visitas(models.Model):
    id_visita = models.FloatField(primary_key=True)
    id_noticia = models.ForeignKey(Noticias, models.DO_NOTHING, db_column='id_noticia')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    fecha_visita = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visitas'
