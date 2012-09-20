from django.contrib.auth.models import User, Group, Permission, ContentType

APP_NAME = 'Inventario'

MODELOS = (
    ('configuracion'),
    ('servidor'),
    ('cargas'),
    ('operador'),
    ('alerta'),
    )

ACCIONES = (
    ('add'),
    ('change'),
    ('delete'),
    )

class run(object):
    def crear_db(self):
        pass

    def crear_admingroup(self):
        try:
            adminGroup = Group()
            adminGroup.name = 'Administradores'
            print "creando grupo %s" % adminGroup.name
            adminGroup.save()
            for permiso in Permission.objects.all():
                adminGroup.permissions.add(permiso)
        except Exception:
            print "no fue posible crear el grupo de administradores"

    def crear_admin(self):
        try:
            adminUser = User.objects.create_user('admin', 'admin@localhost.com', '4dm1n15tr4t0r')
            adminUser.first_name = 'Administrador'
            adminUser.last_name = 'Web'
            adminUser.is_staff = True
            adminUser.is_superuser = True
            print "creando usuario %s" % adminUser.username
            adminUser.save()
            for adminGroup in Group.objects.all():
                adminUser.groups.add(adminGroup)
        except Exception:
            print "no fue posible crear el usuario administrador"

    def crear_appgroup(self):
        try:
            appGroup = Group()
            appGroup.name = 'Web'
            print "creando grupo %s" % appGroup.name
            appGroup.save()
            print "otorgando permisos a %s" % appGroup.name
            for modelo in MODELOS:
                contenido = ContentType.objects.get(app_label=APP_NAME, model=modelo)
                for accion in ACCIONES:
                    code = accion + "_" + modelo
                    permiso = Permission.objects.get(content_type=contenido, codename=code)
                    appGroup.permissions.add(permiso)
        except Exception:
            print "no fue posible crear el grupo de Web"

    def crear_appgroup_add(self):
        try:
            appGroup = Group()
            appGroup.name = 'Web_only_add'
            print "creando grupo %s" % appGroup.name
            appGroup.save()
            print "otorgando permisos a %s" % appGroup.name
            for modelo in MODELOS:
                contenido = ContentType.objects.get(app_label=APP_NAME, model=modelo)
                accion = 'add'
                code = accion + "_" + modelo
                permiso = Permission.objects.get(content_type=contenido, codename=code)
                appGroup.permissions.add(permiso)
        except Exception as e:
            print "no fue posible crear el grupo de Web"

    def crear_appgroup_change(self):
        try:
            appGroup = Group()
            appGroup.name = 'Web_only_change'
            print "creando grupo %s" % appGroup.name
            appGroup.save()
            print "otorgando permisos a %s" % appGroup.name
            for modelo in MODELOS:
                contenido = ContentType.objects.get(app_label=APP_NAME, model=modelo)
                accion = 'change'
                code = accion + "_" + modelo
                permiso = Permission.objects.get(content_type=contenido, codename=code)
                appGroup.permissions.add(permiso)
        except Exception as e:
            print "no fue posible crear el grupo de Web"

    def crear_appgroup_delete(self):
        try:
            appGroup = Group()
            appGroup.name = 'Web_only_delete'
            print "creando grupo %s" % appGroup.name
            appGroup.save()
            print "otorgando permisos a %s" % appGroup.name
            for modelo in MODELOS:
                contenido = ContentType.objects.get(app_label=APP_NAME, model=modelo)
                accion = 'delete'
                code = accion + "_" + modelo
                permiso = Permission.objects.get(content_type=contenido, codename=code)
                appGroup.permissions.add(permiso)
        except Exception as e:
            print "no fue posible crear el grupo de Web"