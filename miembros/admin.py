from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RegistroClub

@admin.register(RegistroClub)
class RegistroClubAdmin(admin.ModelAdmin):
    # Esto hará que veas columnas bonitas en la lista
    list_display = ('nombre', 'apellidos', 'email_institucional', 'carrera')
    # Agregamos un buscador por si el club crece mucho
    search_fields = ('nombre', 'numero_cuenta', 'email_institucional')