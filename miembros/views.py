import time
import ssl
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail, get_connection
from django.conf import settings
from .forms import FormularioRegistro

def index(request):
    if request.method == 'POST':
        # 1. Rate Limiting (Evitar Spam)
        ultimo_envio = request.session.get('ultimo_envio')
        tiempo_actual = time.time()

        if ultimo_envio and (tiempo_actual - ultimo_envio < 60):
            messages.error(request, "Espera un minuto antes de enviar otra solicitud.")
            return render(request, 'index.html', {'form': FormularioRegistro(request.POST)})

        form = FormularioRegistro(request.POST)

        if form.is_valid():
            # Guardamos el registro en la base de datos
            registro = form.save()

            # --- PARCHE MAESTRO PARA SSL (Windows/Python 3.13) ---
            # Creamos un contexto que no verifique certificados locales
            contexto_seguro = ssl._create_unverified_context()

            try:
                # Abrimos la conexión manualmente inyectando el contexto seguro
                connection = get_connection(
                    backend=settings.EMAIL_BACKEND,
                    fail_silently=False,
                    context=contexto_seguro 
                )

                # --- 1. CORREO PARA LA MESA DIRECTIVA ---
                asunto_mesa = f"Nueva solicitud de membresía: {registro.nombre} {registro.apellidos}"
                mensaje_mesa = f"""
                Hola Mesa Directiva,
                
                Se ha recibido una nueva solicitud para Hello World:
                
                Nombre: {registro.nombre} {registro.apellidos}
                Carrera: {registro.get_carrera_display()}
                Número de Cuenta: {registro.numero_cuenta}
                Correo: {registro.email_institucional}
                
                Motivos:
                {registro.carta_motivos}
                """
                destinatarios_mesa = ['helloworld.clubfesa@gmail.com']
                
                send_mail(
                    asunto_mesa,
                    mensaje_mesa,
                    settings.EMAIL_HOST_USER, 
                    destinatarios_mesa,
                    fail_silently=False,
                    connection=connection # Usamos la conexión parchada
                )

                # --- 2. CORREO PARA EL ALUMNO (Confirmación) ---
                asunto_alumno = "¡Hemos recibido tu solicitud para Hello World! 🚀"
                mensaje_alumno = f"""
                Hola {registro.nombre},

                ¡Gracias por tu interés en unirte al Club Hello World de la FES Aragón! 

                Hemos recibido tu solicitud (Cuenta: {registro.numero_cuenta}).
                Tu carta de motivos está siendo revisada por la Mesa Directiva. Te contactaremos pronto.

                ¡Mucho éxito!
                Atentamente, Equipo de Hello World
                """
                
                send_mail(
                    asunto_alumno,
                    mensaje_alumno,
                    settings.EMAIL_HOST_USER,
                    [registro.email_institucional],
                    fail_silently=False,
                    connection=connection # Usamos la conexión parchada
                )

                # Si todo sale bien, marcamos el tiempo y enviamos éxito
                request.session['ultimo_envio'] = tiempo_actual
                messages.success(request, "¡Solicitud enviada con éxito!")
                return render(request, 'index.html', {'form': FormularioRegistro(), 'exito': True})

            except Exception as e:
                # Si falla el correo, el registro ya está a salvo en la DB
                print(f"Error enviando correo: {e}")
                messages.success(request, "¡Registro guardado! (Hubo un detalle con los correos de confirmación)")
                return render(request, 'index.html', {'form': FormularioRegistro(), 'exito': True})
        
        else:
            # Si el formulario no es válido (ej. motivos < 100 caracteres)
            messages.error(request, "Hay errores en tu formulario. Por favor, revísalo.")
            return render(request, 'index.html', {'form': form})
    
    else:
        # Petición GET normal
        form = FormularioRegistro()
    
    return render(request, 'index.html', {'form': form})