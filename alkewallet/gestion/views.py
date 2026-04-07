from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Cuenta,Cliente, Transaccion
from .forms import RegistroUsuarioForm, TransaccionForm, CuentaForm

from django.db.models import Count,Sum
from django.db import connection

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(
                user=user,
                telefono=form.cleaned_data.get('telefono'),
                direccion=form.cleaned_data.get('direccion')
            )
            login(request, user)
            return redirect('cuenta_list')

    else:
        form = RegistroUsuarioForm()

    return render(request,'registration/registro.html',{'form':form})

@login_required
def cuenta_list(request):
    """enlistar las cuentas de un usuario"""
    cuentas = Cuenta.objects.filter(cliente__user=request.user)
    return render(request, 'cuenta_list.html', {'cuentas':cuentas})

@login_required
def cuenta_create(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)#en nuestro formulario no esta el campo user.cliente, por lo que debemos pasarlo como referencia para crear la cuenta
            #commit False, obten los datos en memoria pero sin guardar en la bd aun
            cuenta.cliente = request.user.cliente
            cuenta.save()
            return redirect('cuenta_list')
    else:
        form = CuentaForm()
    return render(request, 'cuenta_form.html',{'form':form})

@login_required
def cuenta_update(request, pk):
    #cuenta = Cuenta.objects.get(pk=pk) #standar, pero se debe validar a parte
    cuenta = get_object_or_404(Cuenta, pk=pk, cliente__user = request.user) #encuentrame el objeto o lanza un error 404
    
    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('cuenta_list')
    else:
        form = CuentaForm(instance=cuenta)
    return render(request, 'cuenta_form.html', {'form':form})


@login_required
def cuenta_delete(request,pk):
    cuenta = get_object_or_404(Cuenta, pk=pk,cliente__user=request.user)

    if request.method == 'POST':
        cuenta.delete()
        return redirect('cuenta_list')

    return render(request, 'cuenta_confirm_delete.html',{'cuenta':cuenta})

@login_required
def transaccion_list(request):
    transacciones =  Transaccion.objects.filter(
        cuenta_origen__cliente__user=request.user
    ).select_related('cuenta_origen', 'cuenta_destino')

    return render(request,'transaccion_list.html', {'transacciones':transacciones})

@login_required
def transaccion_create(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        form.fields['cuenta_origen'].queryset = Cuenta.objects.filter(cliente__user=request.user)
        form.fields['cuenta_destino'].queryset = Cuenta.objects.all()
        if form.is_valid():
            transaccion = form.save()
            return redirect('transaccion_list')

    else:
        form = TransaccionForm()
        form.fields['cuenta_origen'].queryset = Cuenta.objects.filter(cliente__user=request.user)#solo puede usar las cuentas del usuario logeado actualmente
        form.fields['cuenta_destino'].queryset = Cuenta.objects.all()

    return render(request, 'transaccion_form.html',{'form':form})



@login_required
def reportes(request):
    total_saldo = Cuenta.objects.filter(cliente__user=request.user).aggregate(
        total=Sum('saldo')
    )
    resumen_tipos = Transaccion.objects.filter(
        cuenta_origen__cliente__user=request.user
    ).values('tipo').annotate(cantidad=Count('id'))

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT tipo, COUNT(*)
            FROM gestion_transaccion
            GROUP BY tipo
            """)
        
        resumen_sql = cursor.fetchall()
    # print(resumen_sql)
    return render(request, 'reportes.html',{
        'total_saldo':total_saldo,
        'resumen_tipos': resumen_tipos,
        'resumen_sql':resumen_sql
    })


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)

        return redirect(login)
    return redirect('inicio')