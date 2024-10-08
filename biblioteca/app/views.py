from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Socio, Libro, Prestamo


def login_view(request, next_page="/"):
    from django.contrib.auth import authenticate
    from django.contrib.auth import login
    from django.http import HttpResponseRedirect, HttpResponse

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['bienvenida'] = f"Bienvenido, {user.username}"
            return HttpResponseRedirect(next_page)
        else:

            return HttpResponse("Credenciales inválidas!")


    return render(request, "app/login_register.html")








@login_required(login_url="login")
def home(request):
    args = {}
    from .forms import BuscadorForm
    if request.method == "POST":
        form = BuscadorForm(request.POST)
    else:
        form = BuscadorForm(request.GET)

    form.is_valid()
    args['form'] = form
    args['objetos'] = form.buscar()
    return render(request, "app/index.html", args)


@login_required(login_url="login")
def buscador(request):
    args = {}
    from .forms import BuscadorForm
    if request.method == "POST":
        form = BuscadorForm(request.POST)
        if form.is_valid():
            args.update({'objetos': form.buscar_libros(), 'form': form})
    else:
        form = BuscadorForm(request.GET)
    args.update({'form': form})

    return render(request, "app/index.html", args)


def libros_prestados(request):
    from .models import Prestamo
    from .forms import BuscadorForm

    args = {
        'objetos': Prestamo.objects.filter(fecha_dev__isnull=True),
        'form': BuscadorForm(request.GET)}


    return render(request, "app/index.html", args)
