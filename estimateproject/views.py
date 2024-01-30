from helps.response.responsemessage import response as rspn
from helps.common.generic import Generichelps as ghelp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from estimateproject.models import *
from rest_framework import status
import json


@api_view(['POST'])
def addestimateproject(request):
    errors = []

    challenges = json.loads(request.data.get('challenges', str({})).replace("'", "\""))
    alreadyHave = json.loads(request.data.get('alreadyHave', str({})).replace("'", "\""))
    timeframe = json.loads(request.data.get('timeframe', str({})).replace("'", "\""))
    projectType = request.data.get('projectType', '')
    yourRole = request.data.get('yourRole', '')
    servicesNeeded = request.data.get('servicesNeeded', '')
    preferredContactTime = request.data.get('preferredContactTime', '')
    attachment = request.FILES.get('attachment')
    attachmentname = str(attachment)
    projectDetails = request.data.get('projectDetails', '')
    userDetails = json.loads(request.data.get('userDetails', str({})).replace("'", "\""))
    newsletterSubscription = json.loads(request.data.get('newsletterSubscription', True))

    name=userDetails.get('name', '')
    email=userDetails.get('email', '')
    phone=userDetails.get('phone', '')

    if not ghelp().emailvalidate(email): errors.append({'field': 'email','message': rspn['field_err_msg']['email']})
    if not ghelp().numbervalidate(phone): errors.append({'field': 'phone','message': rspn['field_err_msg']['phone']})
    if not ghelp().attachmentvalidate(attachmentname): errors.append({'field': 'attachment','message': rspn['field_err_msg']['attachment']})
    

    if errors: return Response({'status': rspn['error_status'], 'message': rspn['error_message'], 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        userdetails = Userdetails.objects.create(name=userDetails.get('name', ''), email=userDetails.get('email', ''), phone=userDetails.get('phone', ''))

        estimateproject = Estimateproject.objects.create(
            projectType=projectType, 
            yourRole=yourRole, 
            servicesNeeded=servicesNeeded,
            preferredContactTime = preferredContactTime,
            attachment = attachment,
            attachmentname = attachmentname,
            projectDetails = projectDetails,
            userDetails = userdetails,
            newsletterSubscription = newsletterSubscription
            )

        for key in challenges.keys():
            Challenge.objects.create(fieldName=key, value=challenges[key], estimateProject=estimateproject)

        for key in alreadyHave.keys():
            Alreadyhave.objects.create(fieldName=key, value=alreadyHave[key], estimateProject=estimateproject)

        for key in timeframe.keys():
            Timeframe.objects.create(fieldName=key, value=timeframe[key], estimateProject=estimateproject)

        subject = 'Mail From Api Solutions ltd.'
        message = f'challenges: {challenges}, alreadyHave: {alreadyHave}, timeframe: {timeframe}, projectType: {projectType}, yourRole: {yourRole}, servicesNeeded: {servicesNeeded}, preferredContactTime: {preferredContactTime}, projectDetails: {projectDetails}, userDetails: {userDetails}, newsletterSubscription: {newsletterSubscription}'
        recipient_list = ['naymhsain00@gmail.com', 'nazmulhussain.api@gmail.com']
        attachments = [f'media/{estimateproject.attachment}']
        ghelp().send_mail_including_attatchment(subject, message, recipient_list, attachments)
            
        return Response({'status': rspn['success_status'], 'message': rspn['success_message']}, status=status.HTTP_201_CREATED)