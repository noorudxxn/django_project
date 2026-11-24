from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Weight(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    weight = models.DecimalField(max_digits=5, decimal_places=2)

    date = models.DateField(default=timezone.localdate,editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name='unique_user_weight_date'
            )
        ]

    def __str__(self):
        return self.user.username