from django.db import models
from datetime import datetime
from project_module.models import Project, ProjectProcessedData

measures = (
    ('line', 'line'),
    ('poly', 'poly'),
    ('point', 'point'),
)


class AOI(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # date = models.ForeignKey(ProjectProcessedData, on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    label = models.CharField(max_length=255, default="Undefined")
    description = models.CharField(max_length=255, default="")
    creation_date = models.DateTimeField(default=datetime.now())
    polygon = models.TextField(default=[], null=True, blank=True)

    def __str__(self):
        return self.project.name + "_" + self.label


class Measure(models.Model):
    project = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=measures, default='')
    label = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")
    creation_date = models.DateTimeField(default=datetime.now())
    measurements = models.CharField(max_length=255, default="")
    polygon = models.TextField(default={}, null=True, blank=True)

    def __str__(self):
        return self.label + "_" + self.project
