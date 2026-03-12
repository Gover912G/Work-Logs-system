from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class WorkLog(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, blank=True)
    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    problem = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)

    # ✅ THIS MUST BE INSIDE THE MODEL
    def save(self, *args, **kwargs):
        if not self.ticket_id:

            today = datetime.now()
            date_str = today.strftime("%d-%m-%Y")

            new_number = 1

            while True:
                ticket_candidate = f"TCK-{date_str}-{new_number:04d}"

                if not WorkLog.objects.filter(ticket_id=ticket_candidate).exists():
                    self.ticket_id = ticket_candidate
                    break

                new_number += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_id