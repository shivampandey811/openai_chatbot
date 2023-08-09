from django.shortcuts import render,HttpResponse
import openai
from django.http import JsonResponse
from .models import *

openai.api_key = 'YOUR_API_KEY'

def generate_chatbot_response(user_message,topic):
    # Call the OpenAI API to generate a chatbot response
    response = openai.Completion.create(
        # model="gpt-3.5-turbo",
        engine='text-davinci-003',
        prompt=user_message,
        max_tokens=4000,
        temperature=0.9,
        n=1,
        stop=None
    )    
    # chatbot_response = response.choices[0].text.strip()
    import re


    chatbot_response = response.choices[0].text.strip()
    print(chatbot_response)
    

    # from fpdf import FPDF    
    # pdf = FPDF()
    # # Add a page
    # pdf.add_page()
    # # Add content to the PDF    
    # pdf.set_font("Helvetica","B", size=12)                      

    # pdf.multi_cell(200, 10, txt=chatbot_response)
    # chatbot_response = chatbot_response.encode("utf-8", "replace").decode("utf-8")

    # pdf.set_auto_page_break(auto=True, margin=15)
    # pdf.output(f"/Users/admin/Desktop/chatbot/pdf/{topic}.pdf")



    formatted_response = re.sub(r'(?<=\d)\s', r'\n', chatbot_response)

    print(formatted_response)

    return chatbot_response   


def process_message(request):

    user_message = request.POST.get('message')
    l1=['bye','tata','good night']
    if user_message in l1 :
        print("------Getting results----------")
        response_data="Thank you.!! Have a good day" 
        return JsonResponse(response_data)
    else:

        print("------Getting results----------")
        print(user_message)
        topic=user_message
        # user_message="give me the syllabus to learn in full details with all module and topics "+ user_message +"and provide me the tutorial links to study"
        chatbot_response = generate_chatbot_response(user_message,topic)  
        syllabus(question=topic,answer=chatbot_response).save()
        



        # Prepare the response JSON
        response_data = {
            'message': chatbot_response
        }

        return JsonResponse(response_data)

def chatbot_view(request):
    question=syllabus.objects.all()
    return render(request, 'chatbot.html',{"data":question})






def process_message_onclick(request,user_message):
       # print(user_message)
        # topic=user_message
        # user_message="give me the syllabus to learn"+ user_message +"and provide me the tutorial links to study"
        # chatbot_response = generate_chatbot_response(user_message,topic)  
        # response_data = {
        #     'message': chatbot_response
        # }

        # return JsonResponse(response_data)
    question=syllabus.objects.all()
    return render(request, 'chatbot.html',{"data":question,"user_message":user_message})

    
    




from django.http import FileResponse
from django.shortcuts import get_object_or_404

def download_pdf(request,file_name):
    print(file_name)
    # Replace 'path_to_pdf' with the actual path to your PDF file
    pdf_path = f"/Users/admin/Desktop/chatbot/pdf/{file_name}.pdf"
    pdf_file = open(pdf_path, 'rb')
    response = FileResponse(pdf_file, content_type='application/pdf')
    filename=f"{file_name}.pdf"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    print("downloaded succesfully")
    return response

     
