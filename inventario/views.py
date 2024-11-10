from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# Vista para listar los productos
def lista_productos(request):
    productos = Producto.objects.all()
    productos_bajo_inventario = [p for p in productos if p.inventario_bajo()]
    return render(request, 'inventario/lista_productos.html', {
        'productos': productos,
        'productos_bajo_inventario': productos_bajo_inventario,
    })

# Vista para agregar un nuevo producto
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/agregar_producto.html', {'form': form})

# Vista para ver los detalles de un producto específico
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'inventario/detalle_producto.html', {'producto': producto})

# Vista para generar el reporte en PDF
def generar_reporte(request):
    productos = Producto.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Reporte de Inventario")
    y = 750

    for producto in productos:
        p.drawString(100, y, f"{producto.nombre} - Cantidad: {producto.cantidad} - Precio: ${producto.precio}")
        y -= 20

    p.showPage()
    p.save()
    return response

def aumentar_stock(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        cantidad_aumentar = int(request.POST['cantidad'])
        producto.cantidad += cantidad_aumentar
        producto.save()
        return redirect('detalle_producto', pk=producto.pk)  # Redirigir a la página de detalles del producto

    return render(request, 'inventario/aumentar_stock.html', {'producto': producto})


# Create your views here.
