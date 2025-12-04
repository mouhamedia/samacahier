from django.db import models
from django.contrib.auth import get_user_model
from clients.models import Client

User = get_user_model()


class Credit(models.Model):
    """Modèle pour les crédits accordés aux clients."""
    
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('partial', 'Partiellement payé'),
        ('paid', 'Payé'),
        ('overdue', 'En retard'),
        ('archived', 'Archivé'),
    )
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='credits')
    boutiquier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product = models.CharField(max_length=100, blank=True, help_text="Produit ou article vendu")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    
    # ← PEUT ÊTRE DÉSACTIVÉ
    is_active = models.BooleanField(default=True, help_text="Si inactif, n'est pas compté dans les totaux")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Crédit'
        verbose_name_plural = 'Crédits'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Crédit de {self.amount} pour {self.client.name}"
    
    @property
    def remaining_amount(self):
        """Retourne le montant restant à payer."""
        return self.amount - self.paid_amount


class Payment(models.Model):
    """Modèle pour les paiements des crédits."""
    
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='cash')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Paiement de {self.amount} pour crédit {self.credit.id}"
    
    def save(self, *args, **kwargs):
        """Met à jour le montant payé du crédit."""
        super().save(*args, **kwargs)
        
        credit = self.credit
        total_paid = credit.payments.aggregate(models.Sum('amount'))['amount__sum'] or 0
        credit.paid_amount = total_paid
        
        # Mettre à jour le statut
        if credit.paid_amount >= credit.amount:
            credit.status = 'paid'
        elif credit.paid_amount > 0:
            credit.status = 'partial'
        
        credit.save()
