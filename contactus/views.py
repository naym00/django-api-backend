from helps.response.responsemessage import response as rspn
from helps.common.generic import Generichelps as ghelp
from contactus.serializers import ContactusSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def addcontactus(request):
    errors = []
    phone = request.data.get('phone', '')
    if ghelp().numbervalidate(phone):
        companyName = request.data.get('companyName', '')
        name = request.data.get('name', '')
        corporateEmail = request.data.get('corporateEmail', '')
        comments = request.data.get('comments', '')
        protectDataByNDA = request.data.get('protectDataByNDA', True)

        contactusserializer=ContactusSerializer(data=request.data)
        if contactusserializer.is_valid(raise_exception=True): 
            contactusserializer.save()

            subject = 'Mail From Api Solutions ltd.'
            message = f'companyName: {companyName}, name: {name}, corporateEmail: {corporateEmail}, phone: {phone}, comments: {comments}, protectDataByNDA: {protectDataByNDA}'
            recipient_list = ['nazmulhussain.api@gmail.com']
            ghelp().send_mail_including_attatchment(subject, message, recipient_list)


    else: errors.append({'field': 'phone','message': rspn['field_err_msg']['phone']})
    if errors: return Response({'status': rspn['error_status'], 'message': rspn['error_message'], 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': rspn['success_status'], 'message': rspn['success_message']}, status=status.HTTP_201_CREATED)