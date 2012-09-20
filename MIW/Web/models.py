from django.db import models
from datetime import datetime

class configuracion(models.Model):
    agente              = models.CharField(max_length=30, null=False, blank=False)
    clave               = models.CharField(max_length=30, null=False, blank=False, unique=True)
    valor               = models.CharField(max_length=30, null=False, blank=False)
    modificado          = models.CharField(max_length=30, null=False, blank=False)
    defvalor            = models.CharField(max_length=30, null=False, blank=False)
    prevalor            = models.CharField(max_length=30, null=False, blank=False)

    def __unicode__(self):
        return self.agente

    class Meta:
        verbose_name = "Configuracion"
        verbose_name_plural = "Configuraciones"

class servidor(models.Model):
    fqdn                = models.CharField(max_length=30, null=False, blank=False, unique=True)
    puerto              = models.IntegerField(null=False, default=54321)
    activo              = models.BooleanField(null=False, blank=False, default=True)
    habilitado          = models.BooleanField(null=False, blank=False, default=True)
    modificado          = models.DateTimeField(default=datetime.now, null=False, blank=False)
    intento             = models.IntegerField(null=False, default=0)

    def __unicode__(self):
        return self.fqdn

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"

class cargas(models.Model):
    servidorid          = models.ForeignKey(servidor)
    time_unix           = models.CharField(max_length=30, null=False, blank=False)
    cpu_total           = models.FloatField(null=False)
    cpu_cores           = models.CharField(max_length=30, null=False, blank=False)
    mem_total           = models.IntegerField(null=False)
    mem_used            = models.IntegerField(null=False)
    mem_free            = models.IntegerField(null=False)
    mem_percent         = models.CharField(max_length=30, null=False, blank=False)
    io_read_count       = models.IntegerField(null=False)
    io_write_count      = models.IntegerField(null=False)
    io_read_bytes       = models.IntegerField(null=False)
    io_write_bytes      = models.IntegerField(null=False)
    io_read_time        = models.IntegerField(null=False)
    io_write_time       = models.IntegerField(null=False)
    net_bytes_sent      = models.IntegerField(null=False)
    net_bytes_recv      = models.IntegerField(null=False)
    net_packets_sent    = models.IntegerField(null=False)
    net_packets_recv    = models.IntegerField(null=False)
    hdd_device          = models.CharField(max_length=30, null=False, blank=False)
    hdd_total           = models.IntegerField(null=False)
    hdd_used            = models.IntegerField(null=False)
    hdd_free            = models.IntegerField(null=False)
    hdd_percent         = models.CharField(max_length=30, null=False, blank=False)

    def __unicode__(self):
        return u'%s' % (unicode(self.time_unix))

    class Meta:
        verbose_name = "Carga"
        verbose_name_plural = "Cargas"

class operador(models.Model):
    nombre              = models.CharField(max_length=30, null=False, blank=False, unique=True)
    clave               = models.CharField(max_length=10, null=False, blank=False)
    correo              = models.CharField(max_length=20, null=False, blank=False)
    jid                 = models.CharField(max_length=20, null=False, blank=False)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"

class alerta(models.Model):
    operadorid          = models.ForeignKey(operador)
    tipo                = models.CharField(max_length=30, null=False, blank=False)
    nivel               = models.CharField(max_length=30, null=False, blank=False)
    mensaje             = models.TextField()
    enviado             = models.DateField()

    def __unicode__(self):
        return self.operadorid

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"