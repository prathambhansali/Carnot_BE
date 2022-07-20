from django.db import models
from django.utils import timezone
from project_module.models import Project, ProjectData


class UploaderLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.ForeignKey(ProjectData, on_delete=models.CASCADE)
    uploaded_by = models.CharField(max_length=50, blank=True, null=True)
    allfiles = models.TextField(default="")
    upload_time = models.DateTimeField(default=timezone.now)
    total_number_of_files = models.IntegerField(default=0)
    number_of_files_uploaded = models.IntegerField(default=0)
    filesuploaded = models.TextField(default="")

    def __str__(self):
        return self.project
