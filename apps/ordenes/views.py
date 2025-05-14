from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdenCompra, DetalleOrdenCompra
from .forms import OrdenCompraForm, DetalleOrdenCompraForm
from apps.requerimientos.models import Requerimiento
from apps.proveedores.models import Proveedor
from .models import OrdenCompra
from apps.usuarios.models import Usuario
from apps.productos.models import Producto
from django.urls import reverse
from django.contrib import messages

def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'ordenes/lista.html', {'ordenes': ordenes})



def crear_orden(request):
    if request.method == 'POST':
        requerimiento_id = request.POST.get('requerimiento')
        proveedor_id = request.POST.get('proveedor')
        requerimiento = Requerimiento.objects.get(id=requerimiento_id)
        proveedor = Proveedor.objects.get(id=proveedor_id)
        
        # Selecciona el primer usuario disponible
        usuario_emisor = Usuario.objects.first()

        OrdenCompra.objects.create(
            requerimiento=requerimiento,
            proveedor=proveedor,
            usuario_emisor=usuario_emisor,
            estado='borrador'
        )
        return redirect('lista_ordenes')

    requerimientos = Requerimiento.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'ordenes/formulario.html', {
        'requerimientos': requerimientos,
        'proveedores': proveedores
    })



from django.contrib import messages

def agregar_detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        precio_unitario = float(request.POST.get('precio_unitario'))
        subtotal = cantidad * precio_unitario

        detalle = DetalleOrdenCompra(
            orden=orden,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal  # Calculado antes de guardar
        )
        detalle.save()
        return redirect('detalle_orden', orden.id)



    productos = Producto.objects.all()
    return render(request, 'ordenes/agregar_detalle.html', {'orden': orden, 'productos': productos})

    

def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if request.method == 'POST':
        orden.delete()
        messages.success(request, 'La orden ha sido eliminada correctamente.')
        return redirect('lista_ordenes')
    return render(request, 'ordenes/confirmar_eliminacion.html', {'orden': orden})


    
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    detalles = orden.detalles.all()
    total = sum([detalle.subtotal for detalle in detalles])
    return render(request, 'ordenes/detalle.html', {'orden': orden, 'detalles': detalles, 'total': total})

def cambiar_estado_orden(request, orden_id, nuevo_estado):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    orden.estado = nuevo_estado
    orden.save()
    return redirect('detalle_orden', orden_id=orden.id)

def eliminar_detalle_orden(request, orden_id, detalle_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    detalle = get_object_or_404(DetalleOrdenCompra, pk=detalle_id, orden=orden)
    detalle.delete()
    return redirect('detalle_orden', orden_id=orden.id)

# Create your views here.
