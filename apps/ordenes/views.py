from django.shortcuts import render, get_object_or_404, redirect
from .models import OrdenCompra, DetalleOrdenCompra
from apps.requerimientos.models import Requerimiento
from apps.proveedores.models import Proveedor
from apps.productos.models import Producto
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# --- Lista de Ordenes ---
@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'ordenes/lista.html', {'ordenes': ordenes})

# --- Crear Orden ---
@login_required
@permission_required('ordenes.add_ordencompra', raise_exception=True)
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
        messages.success(request, "Orden de compra creada exitosamente.")
        return redirect('lista_ordenes')

    requerimientos = Requerimiento.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'ordenes/formulario.html', {
        'requerimientos': requerimientos,
        'proveedores': proveedores
    })

# --- Agregar Detalle a la Orden ---
@login_required
@permission_required('ordenes.add_detalleordencompra', raise_exception=True)
def agregar_detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if orden.estado != 'borrador':
        messages.warning(request, "No puedes agregar detalles a una orden que no está en borrador.")
        return redirect('detalle_orden', orden_id=orden.id)

    productos = Producto.objects.all()
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')

        producto = get_object_or_404(Producto, pk=producto_id)
        DetalleOrdenCompra.objects.create(
            orden=orden,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=float(cantidad) * float(precio_unitario)
        )
        messages.success(request, f"El producto '{producto.nombre}' ha sido agregado correctamente.")
        return redirect('detalle_orden', orden_id=orden.id)

    return render(request, 'ordenes/agregar_detalle.html', {'orden': orden, 'productos': productos})

# --- Eliminar Orden ---
@login_required
@permission_required('ordenes.delete_ordencompra', raise_exception=True)
def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if orden.estado != 'borrador':
        messages.warning(request, "No se puede eliminar una orden que no está en borrador.")
        return redirect('detalle_orden', orden_id=orden.id)

    if request.method == 'POST':
        orden.delete()
        messages.success(request, f'La orden {orden.codigo} ha sido eliminada correctamente.')
        return redirect('lista_ordenes')

    return render(request, 'ordenes/confirmar_eliminacion_orden.html', {'orden': orden})

# --- Eliminar Detalle de la Orden ---
@login_required
@permission_required('ordenes.delete_detalleordencompra', raise_exception=True)
def eliminar_detalle_orden(request, detalle_id):
    detalle = get_object_or_404(DetalleOrdenCompra, pk=detalle_id)
    orden = detalle.orden

    if orden.estado != 'borrador':
        messages.warning(request, "No se puede eliminar un detalle de una orden que no está en borrador.")
        return redirect('detalle_orden', orden_id=orden.id)

    if request.method == 'POST':
        detalle.delete()
        messages.success(request, f"Se eliminó el producto '{detalle.producto.nombre}' de la orden {orden.codigo}.")
        return redirect('detalle_orden', orden_id=orden.id)

    return render(request, 'ordenes/confirmar_eliminacion_detalle.html', {'detalle': detalle})

# --- Detalle de la Orden ---
@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    detalles = orden.detalles.all()
    total = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
    return render(request, 'ordenes/detalle.html', {
        'orden': orden,
        'detalles': detalles,
        'total': total
    })
    
@login_required
@permission_required('ordenes.change_ordencompra', raise_exception=True)
def cambiar_estado_orden(request, orden_id, nuevo_estado):
    # Obtener la orden de compra por su ID
    orden = get_object_or_404(OrdenCompra, pk=orden_id)

    # Cambiar el estado de la orden
    orden.estado = nuevo_estado
    orden.save()

    # Redirigir a la página de detalles de la orden
    messages.success(request, f"La orden {orden.codigo} ha cambiado a {nuevo_estado}.")
    return redirect('detalle_orden', orden_id=orden.id)

