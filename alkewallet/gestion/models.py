from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Cliente(models.Model):
    #username, email, password, reglas, firstname, lasname etc
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.username
    

class Cuenta(models.Model):
    TIPO_CUENTA = [
        ('AHORRO', 'Ahorro'),
        ('CORRIENTE','Corriente'),
        ('DDIGITAL','Digital') #bipersonal, vista,Linea de Credito
                   ]
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE,
        related_name = 'cuentas'
    )
    numero_cuenta = models.CharField(max_length=20, unique=True) # pk podria ser
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.numero_cuenta} - {self.cliente}'


class Transaccion(models.Model):
    #manytomany
    TIPO_TRANSACCION = [
        ('DEPOSITO','Depósito'),
        ('RETIRO', 'Retiro'),
        ('TRANSFERENCIA','Transferencia'),
    ]

    cuenta_origen = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name='transacciones_origen'
        )
    cuenta_destino = models.ForeignKey(
        Cuenta,
        on_delete=models.SET_NULL,
        related_name='transacciones_destino',
        blank=True,
        null=True
    )
    tipo = models.CharField(max_length=20, choices=TIPO_TRANSACCION)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    #validacion antes de guardar los datos
    def clean(self):
        if self.monto <=0:
            raise ValidationError('El monto debe ser mayor que cero.')
        
        if self.tipo == 'TRANSFERENCIA': #si no hay cuenta self.cuenta_destino es false
            if not self.cuenta_destino:
                raise ValidationError('La transferencia requiere una cuenta de destino')
            if self.cuenta_origen == self.cuenta_destino:
                raise ValidationError("La cuenta de destino no puede ser la misma que la de origen")
        
        if self.tipo in  ['RETIRO', 'TRANSFERENCIA'] and self.cuenta_origen.saldo < self.monto:
            raise ValidationError('Saldo insuficiente.')
        if self.tipo in ['RETIRO','DEPOSITO'] and self.cuenta_destino:
            raise ValidationError('no se requiere una cuenta de destino para la operacion')

        


    #metodo save, nos permite generar logica antes de almacenar un dato d en este caso de transaccion
    def save(self, *args, **kwargs):
        es_nueva = self.pk is None #el dato aun  no se guarda en la BD
        if es_nueva:
            self.full_clean()

            if self.tipo == 'DEPOSITO':
                self.cuenta_origen.saldo += self.monto
                self.cuenta_origen.save()
                
            elif self.tipo == 'RETIRO':
                self.cuenta_origen.saldo -= self.monto
                self.cuenta_origen.save()

            elif self.tipo == 'TRANSFERENCIA':
                self.cuenta_origen.saldo -= self.monto
                self.cuenta_destino.saldo += self.monto
                self.cuenta_destino.save()
                self.cuenta_origen.save()
        super().save(*args,**kwargs)


    def __str__(self):
        return f'{self.tipo} - {self.monto}'
