from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdenCompra, DetalleOrdenCompra
from .forms import OrdenCompraForm, DetalleOrdenCompraForm
from apps.requerimientos.models import Requerimiento
from apps.proveedores.models import Proveedor
from .models import OrdenCompra
from apps.usuarios.models import Usuario
from apps.productos.models import Producto

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
    productos = Producto.objects.all()  # Obtener todos los productos

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        producto = get_object_or_404(Producto, pk=producto_id)

        DetalleOrdenCompra.objects.create(
            orden=orden,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        return redirect('lista_ordenes')

    return render(request, 'ordenes/agregar_detalle.html', {
        'orden': orden,
        'productos': productos  # Pasar productos al contexto
    })
    
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    detalles = orden.detalles.all()
    total = sum([detalle.subtotal for detalle in detalles])
    return render(request, 'ordenes/detalle.html', {'orden': orden, 'detalles': detalles, 'total': total})


# Create your views here.
