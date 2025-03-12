from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    preferencias = models.TextField()  # Lista separada por comas (ej: "pizza,ensalada")
    ingredientes = models.TextField()  # Lista separada por comas (ej: "tomate,queso")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
