import random
import string
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_access_code():
    """Génère un code d'accès unique et permanent (ex: ABC-DE-001)"""
    code = str(uuid.uuid4())[:8].upper()
    return f"{code}"


class Client(models.Model):
    """Modèle pour les clients créés par les boutiquiers."""
    
    STATUS_CHOICES = (
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
        ('archived', 'Archivé'),
    )
    
    boutiquier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # CODE UNIQUE & PERMANENT
    access_code = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False,
        help_text="Code d'accès unique et permanent"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Générer le code UNE SEULE FOIS
        if not self.access_code:
            self.access_code = generate_access_code()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.access_code})"
