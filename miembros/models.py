from django.db import models

# Create your models here.

class RegistroClub(models.Model):
    CARRERAS_CHOICES = [
        ('COMP', 'Ingeniería en Computación'),
        ('MECA', 'Ingeniería Mecánica'),
        ('INDU', 'Ingeniería Industrial'),
        ('ELEC', 'Ingeniería Eléctrica Electrónica'),
        ('OTRA', 'Otra (Especificar)'),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=9, unique=True)
    email_institucional = models.EmailField(unique=True)
    carrera = models.CharField(max_length=10, choices=CARRERAS_CHOICES)
    otra_carrera = models.CharField(max_length=100, blank=True, null=True)
    carta_motivos = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
