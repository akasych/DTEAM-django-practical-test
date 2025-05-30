from django.db import models


class CVDoc(models.Model):
    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, default='', blank=True)
    bio = models.TextField(max_length=500, default='', blank=True)

    def __str__(self):
        return f"CV of {self.firstname} {self.lastname}"


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    startDate = models.DateField()
    endDate = models.DateField()
    cvDoc = models.ForeignKey(CVDoc, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return f"Project {self.title}"


class Skill(models.Model):
    title = models.CharField(max_length=30)
    experience = models.IntegerField()
    cvDoc = models.ForeignKey(CVDoc, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f"{self.title}: {self.experience} years"
