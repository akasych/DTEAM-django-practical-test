from django.db import models
from django.utils import timezone


class CVDoc(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id', 'lastname'])
        ]
    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, default='', blank=True)
    profession = models.CharField(max_length=100, default='', blank=True)

    @property
    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    @property
    def pdf_file_name(self) -> str:
        return f"{self.firstname}{self.lastname}CV.pdf"

    def __str__(self):
        return f"{self.get_full_name()} CV"


class Project(models.Model):
    class Meta:
        ordering = ['startDate']
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    startDate = models.DateField()
    endDate = models.DateField()
    cvDoc = models.ForeignKey(CVDoc, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return f"{self.cvDoc.get_full_name()}'s project {self.title}"


class Skill(models.Model):
    title = models.CharField(max_length=30)
    experience = models.IntegerField()
    cvDoc = models.ForeignKey(CVDoc, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f"{self.cvDoc.get_full_name()} {self.title}: {self.experience} years"


class RequestLog(models.Model):
    method = models.CharField(max_length=10)
    url = models.TextField()
    remote_ip = models.CharField(max_length=15)
    response_status = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        timestamp_loc = timezone.localtime(self.timestamp)
        timestamp_str = timestamp_loc.strftime("%Y-%m-%d  %H:%M:%S")
        return f" Status: {self.response_status} | {self.method} {self.url} at [{timestamp_str}] from {self.remote_ip}."
