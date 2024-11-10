from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

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
    # Consulta los productos
    productos = Producto.objects.all()
    
    # Configuración de la respuesta HTTP para generar el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'
    
    # Configuración del PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4  # Dimensiones del tamaño de la página

    # Encabezado del reporte
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.HexColor("#003366"))
    p.drawString(100, height - 80, "Reporte de Inventario")
    
    # Línea de encabezado
    p.setLineWidth(1)
    p.line(50, height - 100, width - 50, height - 100)
    
    # Información de la tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 130, "Nombre")
    p.drawString(250, height - 130, "Cantidad")
    p.drawString(350, height - 130, "Precio")
    
    # Línea separadora
    p.setLineWidth(0.5)
    p.line(50, height - 135, width - 50, height - 135)
    
    # Variables para la posición inicial del contenido
    y_position = height - 160
    p.setFont("Helvetica", 10)
    
    # Iterar sobre productos para mostrarlos en filas
    for producto in productos:
        if y_position < 50:  # Verifica si hay espacio suficiente en la página
            p.showPage()  # Agrega una nueva página si es necesario
            y_position = height - 80  # Restablece la posición en la nueva página

            # Repite los encabezados en la nueva página
            p.setFont("Helvetica-Bold", 18)
            p.setFillColor(colors.HexColor("#003366"))
            p.drawString(100, height - 80, "Reporte de Inventario")
            p.setLineWidth(1)
            p.line(50, height - 100, width - 50, height - 100)

            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, height - 130, "Nombre")
            p.drawString(250, height - 130, "Cantidad")
            p.drawString(350, height - 130, "Precio")
            p.setLineWidth(0.5)
            p.line(50, height - 135, width - 50, height - 135)
            y_position = height - 160
            p.setFont("Helvetica", 10)

        # Escribir los datos de cada producto
        p.drawString(100, y_position, producto.nombre)
        p.drawString(250, y_position, str(producto.cantidad))
        p.drawString(350, y_position, f"${producto.precio:.2f}")
        y_position -= 20  # Ajusta el espaciado entre filas
    
    # Guardar y cerrar el PDF
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
