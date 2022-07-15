from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
#from .fileuploadutils import chunkOperationUtil
from django.contrib.auth.models import User,Group
#from .Utils import chunkOperation
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from Users.models import *
from .models import UploaderLog
from project_module.models import Project,ProjectData

# from projects.models import Sectors
# from .ChunkUtils import chunkOperation
# from .ChunkUtils  import user_files_info,uploadpath,file_list
import os
import json
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template,render_to_string


# Create your views here.

uploadpath="/home/tapl/Documents/FTP_FOR_PANDA/"

@csrf_exempt
def upload(request,project_name):
    print("From home upload")
    print(request.POST)
    flowChunkNumber = str(request.POST.get('flowChunkNumber'))
    flowChunkSize = str(request.POST.get('flowCurrentChunkSize'))
    flowFileName = request.POST.get('flowFilename')
    flowTotalSize = str(request.POST.get('flowTotalSize'))
    flowTotalChunks = str(request.POST.get('flowTotalChunks'))
    flowRelativePath = str(request.POST.get('flowRelativePath'))
    try:
        file=request.FILES['file'].read()
    except Exception as e:
        return JsonResponse(data={"status": "failed"},safe=False)
    try:
        project=project_name
        print("Project is ", project)
    except Exception as e:
        project=""
    # upload = UploaderLog.objects.filter(project=project_name)
    print(uploadpath)
    try:
        os.mkdir(uploadpath)
    except Exception as e:
        print(e)
        print("Exception is e ",e)
    dirs=flowRelativePath.split("/")
    del dirs[-1]
    print(dirs)
    path=os.path.join(uploadpath,*dirs)
    try:
        os.makedirs(path)
    except Exception as e:
        print("Exception is e ",str(e))
        pass
    try:
        i=0
        flag=True
        while i <=5 and flag:
            flag=retry(path+"/"+flowFileName,file,flowChunkSize)
            i=i+1

        if os.path.exists(path+"/"+flowFileName):
            temp=json.loads(upload.filesuploaded)
            temp[flowRelativePath]=flowFileName
            # upload.filesuploaded=json.dumps((temp))
            # upload.save()
            print(temp)
            import time
            time.sleep(1.0)
        else:
            print("Path doesnt exist ",path+"/"+flowFileName)
    except Exception as e:
        print("Exception occured is ",e)
    return JsonResponse(data={"status": "success"},safe=False)

def retry(path,file,flowChunkSize):
    try:
        print("From retry upload")
        if not os.path.exists(path):
            with open(path,"wb") as out:
                out.write(file)
        elif not str(os.path.getsize(path))==str(flowChunkSize):
            with open(path, "wb") as out:
                out.write(file)
        else:
            print("File already exixsts")
    except FileExistsError as e:
        print("Exception im ",e)
        return False
    except Exception as e:
        print("Exception is ",e)
        return True
    return False


@csrf_exempt
def store_files_meta_info(request,project_name):
    print("From store upload")
    data=json.loads(request.body)
    Project_Name = Project.objects.get(name=project_name)
    upload_queryset=list(UploaderLog.objects.filter(project=Project_Name))
    print("query set ",upload_queryset)
    if len(upload_queryset)==0:
        upload=UploaderLog()
        upload.project=Project_Name
        upload.uploaded_by=request.user.username
        upload.relative_path=uploadpath+project_name
        upload.total_number_of_files=data['total']
        upload.allfiles=json.dumps(data["allfiles"])
        upload.number_of_files_uploaded = 0
        upload.filesuploaded="{}"
        upload.save()
    else:
        upload=upload_queryset[0]
        upload.uploaded_by = request.user.username
        upload.relative_path = uploadpath + project_name
        upload.total_number_of_files = data['total']
        upload.number_of_files_uploaded=0
        upload.allfiles = json.dumps(data["allfiles"])
        upload.filesuploaded = "{}"
        upload.save()

    return JsonResponse(data={"data":"all ok"},safe=False)