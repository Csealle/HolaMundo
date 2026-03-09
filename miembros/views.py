import time
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import FormularioRegistro

def muro(request):
    return render(request, 'muro.html')

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
            # IMPORTANTE: Guardamos el objeto en la variable 'registro'
            registro = form.save()

            # --- AUTOMATIZACIÓN DE CORREO ---
            asunto = f"Nueva solicitud de membresía: {registro.nombre} {registro.apellidos}"
            mensaje = f"""
            Hola Mesa Directiva,
            
            Se ha recibido una nueva solicitud para el club Hello World:
            
            Nombre: {registro.nombre} {registro.apellidos}
            Carrera: {registro.get_carrera_display()}
            Número de Cuenta: {registro.numero_cuenta}
            Correo: {registro.email_institucional}
            
            Motivos:
            {registro.carta_motivos}
            
            Atentamente,
            Backend de Hello World FES Aragón
            """
            
            # Enviamos a la lista que definas en settings.py o escríbelos aquí
            destinatarios = ['helloworld.clubfesa@gmail.com']
            
            try:
                send_mail(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER, 
                    destinatarios,
                    fail_silently=False,
                )
            except Exception as e:
                # Si falla el envío de correo (por falta de internet o config), 
                # al menos el registro ya se guardó en la DB.
                print(f"Error enviando correo: {e}")

            request.session['ultimo_envio'] = tiempo_actual
            messages.success(request, "¡Solicitud enviada con éxito!")
            return render(request, 'index.html', {'form': FormularioRegistro(), 'exito': True})
        
        else:
            messages.error(request, "Hay errores en tu formulario. Por favor, revísalo.")
            return render(request, 'index.html', {'form': form})
    
        # --- AUTOMATIZACIÓN DE CORREO (ALUMNO) ---
        asunto_alumno = "¡Hemos recibido tu solicitud para Hello World! 🚀"
        mensaje_alumno = f"""
        Hola, {registro.nombre},

        ¡Gracias por tu interés en unirte al Club Hello World de la FES Aragón! 

        Hemos recibido correctamente tu solicitud con los siguientes datos:
        - Carrera: {registro.get_carrera_display()}
        - Número de cuenta: {registro.numero_cuenta}

        Tu carta de motivos está siendo revisada por la Mesa Directiva. Te contactaremos pronto a través de este correo institucional para informarte sobre los siguientes pasos del proceso de selección.

        ¡Mucho éxito!
        Atentamente,
        Equipo de Hello World
        """

        # Enviamos el correo al alumno
        send_mail(
            asunto_alumno,
            mensaje_alumno,
            settings.EMAIL_HOST_USER,
            [registro.email_institucional], # Se envía al correo que el alumno puso
            fail_silently=False,
        )

    else:
        form = FormularioRegistro()
    
    return render(request, 'index.html', {'form': form})