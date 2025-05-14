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





def agregar_detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if orden.estado != 'borrador':
        return redirect('detalle_orden', orden_id=orden.id)

    productos = Producto.objects.all()
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        precio_unitario = float(request.POST.get('precio_unitario'))

        producto = get_object_or_404(Producto, pk=producto_id)
        subtotal = cantidad * precio_unitario  # ✅ Calcula el subtotal

        # ✅ Guarda el detalle con el subtotal
        DetalleOrdenCompra.objects.create(
            orden=orden,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal  # ✅ Asigna el subtotal calculado
        )

        return redirect('detalle_orden', orden_id=orden.id)

    context = {
        'orden': orden,
        'productos': productos
    }
    return render(request, 'ordenes/agregar_detalle.html', context)


    
def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)

    if request.method == 'POST':
        orden.delete()
        return redirect('lista_ordenes')

    return render(request, 'ordenes/confirmar_eliminacion_orden.html', {'orden': orden})

def cambiar_estado_orden(request, orden_id, nuevo_estado):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    orden.estado = nuevo_estado
    orden.save()
    return redirect('detalle_orden', orden_id=orden.id)

def eliminar_detalle_orden(request, detalle_id):
    detalle = get_object_or_404(DetalleOrdenCompra, pk=detalle_id)
    orden = detalle.orden
    if orden.estado != 'borrador':
        return redirect('detalle_orden', orden_id=orden.id)

    if request.method == 'POST':
        detalle.delete()
        return redirect('detalle_orden', orden_id=orden.id)

    return render(request, 'ordenes/confirmar_eliminacion_detalle.html', {'detalle': detalle})

def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    detalles = orden.detalles.all()
    total = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
    return render(request, 'ordenes/detalle.html', {
        'orden': orden,
        'detalles': detalles,
        'total': total
    })

# Create your views here.
