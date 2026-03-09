from django import forms
from .models import RegistroClub

class FormularioRegistro(forms.ModelForm):
    class Meta:
        model = RegistroClub
        fields = ['nombre', 'apellidos', 'numero_cuenta', 'email_institucional', 'carrera', 'otra_carrera', 'carta_motivos']
        widgets = {
            'carta_motivos': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Cuéntanos por qué quieres entrar...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        carrera = cleaned_data.get("carrera")
        otra_carrera = cleaned_data.get("otra_carrera")

        # Restricción: Si eligen "Otra", no pueden escribir una que ya esté en la lista
        if carrera == 'OTRA' and otra_carrera:
            opciones_existentes = [choice[1].lower() for choice in RegistroClub.CARRERAS_CHOICES]
            if otra_carrera.lower() in [opt.lower() for opt in ["Computación", "Mecánica", "Industrial", "Eléctrica Electrónica"]]:
                raise ValidationError("Esa carrera ya está en las opciones principales. Por favor selecciónala del menú.")
        
        return cleaned_data