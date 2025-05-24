from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
import json

from .models import OrdenCompra, DetalleOrdenCompra
from apps.requerimientos.models import Requerimiento, DetalleRequerimiento
from apps.proveedores.models import Proveedor
from apps.productos.models import Producto, Categoria

@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()
    
    # Sumar los totales
    total_general = sum([orden.total for orden in ordenes if orden.total])

    return render(request, 'ordenes/mis_ordenes_generadas.html', {
        'ordenes': ordenes,
        'total_general': total_general,
        'es_admin': True  
    })


# ================== COMPRADOR ==================

@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def lista_requerimientos_aprobados(request):
    requerimientos = Requerimiento.objects.filter(
        estado='aprobado',
        activo=True
    ).select_related('solicitante', 'departamento').prefetch_related('detalles__producto__categoria').order_by('-fecha')
    
    return render(request, 'ordenes/lista_requerimientos_aprobados.html', {
        'requerimientos': requerimientos
       
    })

@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def ver_detalle_requerimiento_comprador(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, estado='aprobado', activo=True)
    detalles = requerimiento.detalles.select_related('producto__categoria').all()
    
    return render(request, 'ordenes/detalle_requerimiento_comprador.html', {
        'requerimiento': requerimiento,
        'detalles': detalles
    })

@login_required
@permission_required('ordenes.add_ordencompra', raise_exception=True)
def asignar_proveedores(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, estado='aprobado', activo=True)
    detalles = requerimiento.detalles.select_related('producto__categoria').all()
    
    productos_por_categoria = {}
    for detalle in detalles:
        categoria = detalle.producto.categoria
        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []
        productos_por_categoria[categoria].append({
            'detalle': detalle,
            'producto': detalle.producto,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.producto.precio_referencial
        })
    
    proveedores = Proveedor.objects.filter(activo=True).order_by('razon_social')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                asignaciones = {}
                for detalle in detalles:
                    producto_id = str(detalle.producto.id)
                    proveedor_id = request.POST.get(f'proveedor_producto_{producto_id}')
                    if proveedor_id:
                        proveedor = get_object_or_404(Proveedor, pk=proveedor_id, activo=True)
                        asignaciones[detalle.id] = {
                            'detalle': detalle,
                            'proveedor': proveedor,
                            'precio_unitario': detalle.producto.precio_referencial
                        }
                request.session[f'asignaciones_requerimiento_{requerimiento_id}'] = {
                    str(detalle_id): {
                        'detalle_id': asig['detalle'].id,
                        'proveedor_id': asig['proveedor'].id,
                        'precio_unitario': float(asig['precio_unitario'])
                    }
                    for detalle_id, asig in asignaciones.items()
                }
                messages.success(request, "Proveedores asignados correctamente.")
                return redirect('generar_orden_compra', requerimiento_id=requerimiento.id)
        except Exception as e:
            messages.error(request, f"Error al asignar proveedores: {str(e)}")
    
    return render(request, 'ordenes/asignar_proveedores.html', {
        'requerimiento': requerimiento,
        'productos_por_categoria': productos_por_categoria,
        'proveedores': proveedores
    })

@login_required
@permission_required('ordenes.add_ordencompra', raise_exception=True)
def generar_orden_compra(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, estado='aprobado', activo=True)
    asignaciones_data = request.session.get(f'asignaciones_requerimiento_{requerimiento_id}')
    
    if not asignaciones_data:
        messages.error(request, "No se encontraron asignaciones de proveedores.")
        return redirect('asignar_proveedores', requerimiento_id=requerimiento.id)
    
    asignaciones = {}
    for detalle_id, asig_data in asignaciones_data.items():
        detalle = get_object_or_404(DetalleRequerimiento, pk=asig_data['detalle_id'])
        proveedor = get_object_or_404(Proveedor, pk=asig_data['proveedor_id'])
        asignaciones[int(detalle_id)] = {
            'detalle': detalle,
            'proveedor': proveedor,
            'precio_unitario': asig_data['precio_unitario']
        }
    
    ordenes_por_proveedor = {}
    for asig in asignaciones.values():
        proveedor = asig['proveedor']
        if proveedor not in ordenes_por_proveedor:
            ordenes_por_proveedor[proveedor] = []
        ordenes_por_proveedor[proveedor].append(asig)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                ordenes_creadas = []
                for proveedor, items in ordenes_por_proveedor.items():
                    ultimo_numero = OrdenCompra.objects.count() + 1
                    codigo_orden = f"OC-{datetime.now().year}-{ultimo_numero:05d}"
                    orden = OrdenCompra.objects.create(
                        codigo=codigo_orden,
                        requerimiento=requerimiento,
                        proveedor=proveedor,
                        usuario_emisor=request.user,
                        estado='emitida',
                        fecha_emision=timezone.now().date()
                    )
                    total_orden = 0
                    for item in items:
                        detalle = item['detalle']
                        precio_unitario = item['precio_unitario']
                        subtotal = precio_unitario * detalle.cantidad
                        DetalleOrdenCompra.objects.create(
                            orden=orden,
                            producto=detalle.producto,
                            cantidad=detalle.cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal
                        )
                        total_orden += subtotal
                    orden.subtotal = total_orden
                    orden.total = total_orden
                    orden.save()
                    ordenes_creadas.append(orden)
                requerimiento.estado = 'en_proceso'
                requerimiento.save()
                if f'asignaciones_requerimiento_{requerimiento_id}' in request.session:
                    del request.session[f'asignaciones_requerimiento_{requerimiento_id}']
                messages.success(request, "Órdenes generadas correctamente.")
                return redirect('resumen_ordenes_generadas', requerimiento_id=requerimiento.id)
        except Exception as e:
            messages.error(request, f"Error al generar órdenes: {str(e)}")
    
    return render(request, 'ordenes/generar_orden_compra.html', {
        'requerimiento': requerimiento,
        'ordenes_por_proveedor': ordenes_por_proveedor
    })

@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def resumen_ordenes_generadas(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    ordenes = OrdenCompra.objects.filter(requerimiento=requerimiento).select_related('proveedor').prefetch_related('detalles__producto')
    return render(request, 'ordenes/resumen_ordenes_generadas.html', {
        'requerimiento': requerimiento,
        'ordenes': ordenes
    })

@login_required
@permission_required('ordenes.view_ordencompra', raise_exception=True)
def mis_ordenes_generadas(request):
    ordenes = OrdenCompra.objects.filter(
        usuario_emisor=request.user
    ).select_related('requerimiento', 'proveedor').order_by('-fecha_emision')
    
    # Calcular el total general
    total_general = sum([orden.total for orden in ordenes if orden.total])

    return render(request, 'ordenes/mis_ordenes_generadas.html', {
        'ordenes': ordenes,
        'total_general': total_general,
        'es_admin': False
    })


@login_required
def aplicar_proveedor_categoria(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            categoria_id = data.get('categoria_id')
            proveedor_id = data.get('proveedor_id')
            if not categoria_id or not proveedor_id:
                return JsonResponse({'success': False, 'error': 'Datos incompletos'})
            categoria = get_object_or_404(Categoria, pk=categoria_id)
            proveedor = get_object_or_404(Proveedor, pk=proveedor_id, activo=True)
            return JsonResponse({
                'success': True,
                'categoria_id': categoria_id,
                'proveedor_id': proveedor_id,
                'proveedor_nombre': proveedor.razon_social
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})