from django.shortcuts import render
from .forms import FormularioRegistro # Importas tu clase de forms.py

def pagina_inicio(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save() # Aquí se guarda en SQLite
            # Aquí podrías redireccionar a una página de éxito
    else:
        form = FormularioRegistro() # Creas el formulario vacío
    
    # AQUÍ ES DONDE SE CONECTAN:
    # Le dices: "Usa index.html y rellena la palabra 'form' con mi FormularioRegistro"
    return render(request, 'index.html', {'form': form})