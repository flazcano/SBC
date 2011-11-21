from django.db import models

class operador(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=False)
    clave = models.CharField(max_length=10, null=False, blank=False)
    correo = models.CharField(max_length=20, null=False, blank=False)
    jid = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.oid, self.nombre, self.clave, self.correo, self.jid)

class alerta(models.Model):
    operadorid = models.ForeignKey(operador)
    tipo = models.CharField(max_length=30, null=False, blank=False)
    nivel = models.CharField(max_length=30, null=False, blank=False)
    mensaje = models.TextField()
    enviado = models.DateField()

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.aid, self.operadorid, self.tipo, self.nivel, self.mensaje, self.enviado)