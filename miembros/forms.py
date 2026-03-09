from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import RegistroClub
from django.core.validators import MinLengthValidator, MaxLengthValidator

class FormularioRegistro(forms.ModelForm):
    # Regex para Nombres y Apellidos: Solo letras y espacios
    letras_validator = RegexValidator(
        regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
        message="Este campo solo puede contener letras."
    )

    # Regex para Número de Cuenta: Exactamente 9 dígitos
    cuenta_validator = RegexValidator(
        regex=r'^\d{9}$',
        message="El número de cuenta debe tener exactamente 9 dígitos numéricos."
    )

    # Sobrescribimos los campos para agregar las validaciones
    nombre = forms.CharField(validators=[letras_validator])
    apellidos = forms.CharField(validators=[letras_validator])
    numero_cuenta = forms.CharField(validators=[cuenta_validator])
    email_institucional = forms.EmailField()

    # Agregamos un validador de longitud
    carta_motivos = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Cuéntanos por qué quieres ser parte de Hello World...'}),
        validators=[
            MinLengthValidator(100, message="¡Tu respuesta es muy corta! Cuéntanos más (mínimo 100 caracteres)."),
            MaxLengthValidator(350, message="¡Te pasaste! Intenta ser más sintético (máximo 300 caracteres).")
        ]
    )

    class Meta:
        model = RegistroClub
        fields = ['nombre', 'apellidos', 'numero_cuenta', 'email_institucional', 'carrera', 'otra_carrera', 'carta_motivos']

    # Validación para Numero de Cuenta duplicado
    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data.get('numero_cuenta')
        if RegistroClub.objects.filter(numero_cuenta=numero_cuenta).exists():
            raise forms.ValidationError("Este número de cuenta ya tiene una solicitud en proceso.")
        return numero_cuenta

    # Validación personalizada para el correo institucional (UNAM/Aragón)
    def clean_email_institucional(self):
        email = self.cleaned_data.get('email_institucional').lower()
        dominios_validos = ['@aragon.unam.mx', '@comunidad.unam.mx']
        
        if not any(email.endswith(dominio) for dominio in dominios_validos):
            raise forms.ValidationError("Usa un correo válido: @aragon.unam.mx o @comunidad.unam.mx")
        
        # Luego validamos si ya existe en la base de datos
        if RegistroClub.objects.filter(email_institucional=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        
        return email