from django.db import models

# Create your models here.
# from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):

    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    )

    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    title = models.CharField(max_length=255)

    file = models.FileField(upload_to='uploads/')

    file_type = models.CharField(max_length=20,choices=FILE_TYPES)

    extracted_text = models.TextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title