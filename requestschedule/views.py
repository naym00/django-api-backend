from requestschedule.serializers import RequestscheduleSerializer
from requestschedule.models import Userdetails, Requestschedule
from helps.response.responsemessage import response as rspn
from helps.common.generic import Generichelps as ghelp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

@api_view(['POST'])
def addrequestschedule(request):
    errors = []
    service = request.data.get('service', '')
    date = request.data.get('date', datetime.today().strftime('%Y-%m-%d'))
    time = request.data.get('time', datetime.now().strftime('%H:%M:%S'))
    budget = request.data.get('budget', '')
    description = request.data.get('description', '')
    userDetails = request.data.get('userDetails', {})

    if not userDetails: errors.append({'field': 'userDetails','message': rspn['required_error']['userDetails']})
    if userDetails:
        name = userDetails.get('name', '')
        phone = userDetails.get('phone', '')

        if not ghelp().datevalidate(date):
            errors.append({'field': 'date','message': rspn['field_err_msg']['date']})
        if not ghelp().datevalitime(time, condition=False):
            errors.append({'field': 'time','message': rspn['field_err_msg']['time']})
        if not ghelp().numbervalidate(phone):
            errors.append({'field': 'phone','message': rspn['field_err_msg']['phone']})

    if errors: return Response({'status': rspn['error_status'], 'message': rspn['error_message'], 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        userdetails = Userdetails.objects.create(name=name, phone=phone)
        requestschedule = Requestschedule.objects.create(service=service, date=date, time=time, budget=budget, description=description, userDetails=userdetails)

        subject = 'Mail From Api Solutions ltd.'
        message = f'service: {service}, date: {date}, time: {time}, budget: {budget}, description: {description}, name: {name}, phone: {phone}'
        recipient_list = ['nazmulhussain.api@gmail.com','mustafatanim59@gmail.com','sathy754@gmail.com']
        ghelp().send_mail_including_attatchment(subject, message, recipient_list)

        RequestscheduleSerializer(requestschedule, many=False)
        return Response({'status': rspn['success_status'], 'message': rspn['success_message_re']}, status=status.HTTP_201_CREATED)
    # return Response({'status': rspn['success_status'], 'message': rspn['success_message']}, status=status.HTTP_201_CREATED)