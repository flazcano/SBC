from django.db import models

class configuracion(models.Model):
    agente              = models.CharField(max_length=30, null=False, blank=False)
    clave               = models.CharField(max_length=30, null=False, blank=False)
    valor               = models.CharField(max_length=30, null=False, blank=False)
    modificado          = models.CharField(max_length=30, null=False, blank=False)
    defvalor            = models.CharField(max_length=30, null=False, blank=False)
    prevalor            = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        pass

class servidor(models.Model):
    fqdn                = models.CharField(max_length=30, null=False, blank=False)
    puerto              = models.IntegerField(null=False, default=54321)
    activo              = models.BooleanField(null=False, blank=False, default=True)
    modificado          = models.CharField(max_length=30, null=False, blank=False)
    intento             = models.IntegerField(null=False, default=0)

    def __str__(self):
        pass

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

    def __str__(self):
        pass

class operador(models.Model):
    nombre              = models.CharField(max_length=30, null=False, blank=False)
    clave               = models.CharField(max_length=10, null=False, blank=False)
    correo              = models.CharField(max_length=20, null=False, blank=False)
    jid                 = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.id, self.nombre, self.clave, self.correo, self.jid)

class alerta(models.Model):
    operadorid          = models.ForeignKey(operador)
    tipo                = models.CharField(max_length=30, null=False, blank=False)
    nivel               = models.CharField(max_length=30, null=False, blank=False)
    mensaje             = models.TextField()
    enviado             = models.DateField()

    def __str__(self):
        return "%s, %s, %s, %s" % (self.tipo, self.nivel, self.mensaje, self.enviado)

    def getOpEn(self):
        return "%s %s" % (self.operadorid, self.enviado)

