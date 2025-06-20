import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image, ImageDraw


def avatar_upload_path(instance, filename) -> str:
    return f'avatars/{instance.firstname}{instance.lastname}/{filename}'


class CVDoc(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id', 'lastname'])
        ]
        verbose_name = "CV"
        verbose_name_plural = "CVs"

    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, default='', blank=True)
    profession = models.CharField(max_length=100, default='', blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)

    @property
    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    @property
    def pdf_file_name(self) -> str:
        return f"{self.firstname}{self.lastname}CV.pdf"

    @property
    def thumb(self) -> str | None:
        if not self.avatar:
            return None
        return self._thumb_upload_path(self.avatar.url)


    def _thumb_upload_path(self, path: str = "", new_ext: str = "png") -> str:
        path_spl: list = path.split(".")
        del path_spl[-1]  # drop original extension and save PNG by default after resize
        return ".".join(path_spl) + "_thumb" + "." + new_ext

    def make_thumbnail(self):
        max_size = (50, 50)   # Resize avatar to thumbnail 50x50 max
        avatar_path = self.avatar.path
        img = Image.open(avatar_path)
        img.thumbnail(max_size)
        img.save(self._thumb_upload_path(avatar_path))

    def delete_avatar_files(self):
        if self.avatar:
            # delete avatar and thumbnail image
            avatar_path = self.avatar.path
            thumb_path = self._thumb_upload_path(avatar_path)
            if os.path.isfile(avatar_path):
                os.remove(avatar_path)
            if os.path.isfile(thumb_path):
                os.remove(thumb_path)

    def __str__(self):
        return f"{self.full_name} CV"


class Project(models.Model):
    class Meta:
        ordering = ['startDate']
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    startDate = models.DateField()
    endDate = models.DateField()
    cvDoc = models.ForeignKey(CVDoc, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return f"{self.cvDoc.full_name}'s project {self.title}"


class Skill(models.Model):
    title = models.CharField(max_length=30, verbose_name='Skill')
    experience = models.IntegerField(verbose_name='Years')
    cvDoc = models.ForeignKey(CVDoc, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f"{self.cvDoc.full_name} {self.title}: {self.experience} years"


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
