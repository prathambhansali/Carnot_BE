from json import decoder
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from project_module.models import Project
from rest_framework.authtoken.models import Token
from .models import PasswordReset, UserProfile
from django.db import transaction
from rest_framework.response import Response
from rest_framework.authentication import (TokenAuthentication, authenticate,
                                           get_user_model)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR



def UserCreated(mail_list):
    sender_email = 'prathmesh@datasee.ai'
    # sender_email = 'info@datasee.ai'
    subject = 'Account Created'

    send_mail(subject, "", sender_email, mail_list,
              html_message=render_to_string('user_created.html'), fail_silently=False)
    return True


def AccountCreated(mail_list, data):
    sender_email = 'prathmesh@datasee.ai'
    # sender_email = 'info@datasee.ai'

    html_message = render_to_string('account_created.html', {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'company': data['company'],
        'mobile_number': data['mobile_number'],
        'company': data['company']})
    subject = 'User Created'

    send_mail(subject, "", sender_email, mail_list,
              html_message=html_message, fail_silently=False)
    return True


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def home(request):
    try:
        username = request.data['username']
        password = request.data['password']

        if username == "" or password == "":
            return Response({"status": "failure"})
        if username is not None or password is not None:
            try:
                User = get_user_model()
                user = authenticate(username=User.objects.get(
                    email=username), password=password)
            except:
                user = authenticate(username=username, password=password)

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                userProfile = UserProfile.objects.get(user=user)
                response = Response({"status": "success", "user": username, "token": token.key, "firstname": user.first_name,
                                    "lastname": user.last_name, "email": user.email, "privilege": userProfile.priviledge})
                response.set_cookie(key="token", value=token, max_age=900)

                return response
            else:
                return Response({"status": "failure"})
        else:
            return Response({"status": "Enter User name and password"})
    except decoder.JSONDecodeError as e:
        return Response({"status": "failed", "exception": str(e)})
    except Exception as e:
        return Response({"status": "failed", "exception": str(e)})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create(request):
    try:
        data = request.data
        if authenticate(username=data['username'], password=data['password']) is None:
            try:
                User = get_user_model()
                user = User.objects.create_user(
                    username=data['username'], email=data['email'], is_staff=True)
                user.set_password(data['password'])
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                profile = UserProfile()
                profile.user = user
                profile.mobile_number = data['mobile_number']
                profile.email = data['email']
                profile.company = data['company']
                profile.priviledge = "admin"
                profile.profile_pic = data["profile_pic"]
                mygroup, created = Group.objects.get_or_create(
                    name=data['company'])
                mygroup.save()
                myuser = User.objects.get(username=data['username'])
                myuser.groups.add(mygroup)
                profile.save()
                # AccountCreated(['sanjay@datasee.ai', 'afzal@datasee.ai', 'adhityan@datasee.ai'], data)
                # UserCreated([data['email']])

                try:
                    company = Group.objects.get(name="DEMOS")
                    test = Project.objects.filter(organization=company)
                    mygroups = Group.objects.get(name=data['company'])
                    for i in test:
                        i.clients.add(mygroups)
                        i.save()
                except Exception as e:
                    pass
            except Exception as e:
                return Response({"status": "User Already"})

            return Response({"status": "success"}, status=HTTP_200_OK)
        else:
            return Response({"status": "User Already exists"})

    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def add_subuser(request):
    try:
        data = request.data
        if authenticate(username=data['username'], password=data['password']) is None:
            try:
                User = get_user_model()
                user = User.objects.create_user(
                    username=data['username'], email=data['email'], is_staff=True)
                user.set_password(data['password'])
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                profile = UserProfile()
                profile.user = user
                profile.mobile_number = data['mobile_number']
                profile.email = data['email']
                userProfile = UserProfile.objects.get(user=request.user)
                profile.company = userProfile.company
                profile.priviledge = "user"
                profile.profile_pic = data["profile_pic"]
                myuser = User.objects.get(username=data['username'])
                mygroup = Group.objects.get(name=userProfile.company)
                myuser.groups.add(mygroup)
                profile.save()
            except Exception as e:
                return Response({"status": "User Already "})
            updated_list = global_subuser(request.user)
            return Response({"status": "success", "updated_list": updated_list}, status=HTTP_200_OK)
        else:
            return Response({"status": "User Already exists"})

    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def update_profile(request):
    pass


def global_subuser(user):
    user_group = list(user.groups.values_list('name', flat=True))
    company = Group.objects.get(name=user_group[0])
    all_users = UserProfile.objects.filter(company=company)
    t_list = []
    for i in all_users:
        temp = {}
        temp_user = get_user_model().objects.get(username=i.user)
        temp["Username"] = temp_user.username
        temp["Full name"] = temp_user.first_name + " " + temp_user.last_name
        temp["E mail"] = temp_user.email
        temp["Privilege"] = i.priviledge
        temp["Created"] = temp_user.date_joined
        t_list.append(temp)
    return t_list


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def get_subuser(request):
    x = global_subuser(request.user)
    return Response(x, status=HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
@transaction.atomic
def generate_link(request):
    try:
        user = User.objects.get(
            email=request.data['email'], username=request.data['username'])
        if user:
            # data = {
            #     'domain': '127.0.0.1:8000/carnot/auth/recovery',
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            #     'protocol': 'http',
            # }
            data = {
                # 'domain': 'asset.datasee.ai/carnot/auth/recovery',
                'domain': 'carnot-app.herokuapp.com/carnot/auth/recovery',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https',
            }
            PasswordReset.objects.filter(user=user).delete()
            # PasswordReset.objects.filter(user=user).update(is_active=False)
            PasswordReset.objects.create(user=user, token=data['token'])
            sender_email = 'prathmesh@datasee.ai'
            # sender_email = 'info@datasee.ai'
            send_mail("Password Reset Requested", "", sender_email, [user.email], html_message=render_to_string(
                "password_reset_email.html", data), fail_silently=False)

        return Response({"message": "Token Link Generated"}, status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "User Not Found"}, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
@transaction.atomic
def reset_password(request):
    uid, token, password = request.data['uid'], request.data['token'], request.data['password']
    if uid != "" and token != "" and password != "":
        try:
            user = User.objects.get(id=int(urlsafe_base64_decode(uid)))
            token = PasswordReset.objects.filter(
                user=user, token=token, is_active=True).update(is_active=False)
            if token != 0:
                user.set_password(request.data['password'])
                user.save()
            else:
                return Response({"message": "Token Not Exist"}, status=HTTP_404_NOT_FOUND)
            return Response({"message": "Password Updated Successfully"}, status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User Not Found"}, status=HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "Invalid Data"}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "User id or token or password not available"}, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def verify_email(request):
    email = request.data['email']
    if email != "":
        try:
            if User.objects.get(email=email): 
                return Response({"message": False}, status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": True}, status=HTTP_200_OK)
        except Exception:
            return Response({"message": "Something Went Wrong"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Invalid Data"}, status=HTTP_404_NOT_FOUND)
