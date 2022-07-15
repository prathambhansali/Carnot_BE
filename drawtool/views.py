from django.shortcuts import render
from rest_framework.authtoken.models import Token
from Users.models import UserProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from .models import AOI
from .models import Measure
from project_module.models import Project,ProjectProcessedData
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User,Group

from rest_framework.authtoken.models import Token

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def save_aoi(request):
    try:
        data = request.data
        project_data = AOI()
        proj_name = Project.objects.get(name=data.get('project_name'))
        project_data.project = proj_name
        project_data.label = data.get('label')
        project_data.date=data.get('date')
        project_data.description = data.get('desc')
        project_data.polygon = json.dumps(data.get('polygon'))
        project_data.save()
        return Response({"status":"success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def save_measure(request,proj_name,date):
    try:
        data = request.data
        project_data = Measure()
        project_data.project = proj_name+"_"+date
        project_data.label = data.get('label')
        project_data.type = data.get('type')
        project_data.description = data.get('description')
        project_data.measurements = data.get('measurements')
        project_data.polygon = data.get('polygon')
        project_data.save()
        return Response({"status":"success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def get_all_data_by_date(request,proj_name,date):
    try:
        temp=Project.objects.get(name=proj_name)
        data=AOI.objects.filter(project=temp).filter(date=date)
        print(data)
        resp={}
        resp[proj_name]={}
        for d in data:
            try:
                resp[proj_name][d.date]
            except KeyError as e:
                resp[proj_name][d.date]={}
            try:
                resp[proj_name][d.date][d.id]
            except KeyError as e:
                resp[proj_name][d.date][d.id]={}
            t={}
            t['label']=d.label
            t['desc'] = d.description
            t['date_of_creation'] = str(d.creation_date)
            t['polygon']=json.loads(d.polygon)
            resp[proj_name][d.date][d.id]=t
        return Response(resp)
    except Exception as e:
        return Response({"status":"failed","exception":str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def delete_aoi(request,id):
    try:
        tool=AOI.objects.get(id=id)
        tool.delete()
        return Response({"status":"success"})
    except Exception as e:
        return Response({"status": "failed","exception":str(e)})
