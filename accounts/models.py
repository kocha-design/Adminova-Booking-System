from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('worker', 'Company Worker'),
        ('admin', 'Company Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True)
    
    # Field Mpya la User ID
    user_id = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)

    def is_company_staff(self):
        return self.role in ['worker', 'admin']

    def save(self, *args, **kwargs):
        # Kama ni mtumiaji mpya na hana user_id bado
        if not self.user_id:
            # Amua prefix kulingana na role
            if self.role == 'admin':
                prefix = 'ADM'
            elif self.role == 'worker':
                prefix = 'WRK'
            else:
                prefix = 'CL'
            
            # Tafuta mtumiaji wa mwisho mwenye prefix hiyo
            last_user = CustomUser.objects.filter(user_id__startswith=f"{prefix}-").order_by('-id').first()
            
            if last_user and last_user.user_id:
                # Toa namba kutoka mfano "CL-005" -> 5
                try:
                    last_number = int(last_user.user_id.split('-')[1])
                    new_number = last_number + 1
                except (IndexError, ValueError):
                    new_number = 1
            else:
                new_number = 1
            
            # Tengeneza ID mpya mfano "CL-001"
            self.user_id = f"{prefix}-{new_number:03d}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_id})"