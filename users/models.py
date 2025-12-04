from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec rôles (client ou boutiquier).
    """
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('boutiquier', 'Boutiquier'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Actif'),
        ('inactive', 'Inactif - Non payé'),
        ('archived', 'Archivé'),
    )
    
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    
    # Statut (peut être inactif sans être supprimé)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Totaux (pour les boutiquiers)
    total_owed = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        help_text="Montant total dû par ce boutiquier"
    )
    paid_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        help_text="Montant payé par ce boutiquier"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def calculate_totals(self):
        """Calculer le montant total dû et payé (pour boutiquiers)"""
        from credits.models import Credit
        
        credits = Credit.objects.filter(
            client__boutiquier=self,
            is_active=True
        )
        
        self.total_owed = sum(c.amount for c in credits) or 0
        self.paid_amount = sum(c.paid_amount for c in credits) or 0
        self.save()
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
