from django.db import models

from pos_project.choices import EstadoEntidades


# Create your models here.
class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True)
    codigo_grupo = models.CharField(max_length=5, null=False)
    nombre_grupo = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'grupos_articulos'
        ordering = ['codigo_grupo']

class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True)
    codigo_linea = models.CharField(max_length=10, null=False)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_linea')
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'lineas_articulos'
        ordering = ['codigo_linea']

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True)
    codigo_articulo = models.CharField(max_length=25, null=False)
    codigo_barras = models.CharField(max_length=25, null=False)
    descripcion = models.CharField(max_length=150)
    presentacion = models.CharField(max_length=100)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='articulo_grupo')
    linea = models.ForeignKey(LineaArticulo, on_delete=models.RESTRICT, null=False, related_name='articulo_linea')
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    stock = models.DecimalField(max_digits=12, decimal_places=2)
    imagen = models.CharField(max_length=255)

    class Meta:
        db_table = 'articulos'
        ordering = ['descripcion']

class CanalCliente(models.Model):
    articulo_id = models.CharField(max_length=3, primary_key=True)
    nombre_canal = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'canal_cliente'

class Cliente(models.Model):
    cliente_id = models.UUIDField(primary_key=True)
    tipo_identificacion = models.CharField(max_length=1)
    nro_identificacion = models.CharField(max_length=11)
    nombres = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    correo_electronico = models.CharField(max_length=255)
    nro_movil = models.CharField(max_length=15)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    canal = models.ForeignKey(CanalCliente, on_delete=models.RESTRICT, null=False, related_name='cliente_canal')

    class Meta:
        db_table = 'cliente'
        ordering = ['nombres']

class Pedido(models.Model):
    pedido_id = models.UUIDField(primary_key=True)
    nro_pedido = models.IntegerField()
    fecha_pedido = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False, related_name='pedido_cliente')
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'pedido'
        ordering = ['nro_pedido']

class ItemPedido(models.Model):
    item_id = models.UUIDField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT, null=False, related_name='item_pedido')
    nro_item = models.IntegerField()
    articulo = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='item_articulo')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total_item = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'item_pedido'
        ordering = ['nro_item']

class Precio(models.Model):
    precio_id = models.UUIDField(primary_key=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='precio_articulo')
    precio_1 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_2 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_3 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_4 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'precio'