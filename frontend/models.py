from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_end_time = models.DateTimeField()
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        return timezone.now() < self.bid_end_time
    
    def __str__(self):
        return f"Auction for {self.product.name}"
    

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que agregó el ítem
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Referencia al modelo Product
    quantity = models.PositiveIntegerField(default=1)  # Cantidad del producto
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)  # Precio en el momento de la compra
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Precio: {self.price_at_purchase})"
    

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Calificación entre 1 y 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.product.name}'

