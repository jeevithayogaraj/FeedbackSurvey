from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import date
from datetime import date, timedelta
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings  
import pandas as pd
from django.http import HttpResponse
import io
from django.http import HttpResponse
from openpyxl import Workbook




# ... Other view functions ...

def custom_login(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

 

        user = None  # Initialize the user variable

 

        # Try to authenticate the user with the provided credentials

        if User.objects.filter(username=username).exists():

            user = auth.authenticate(username=username, password=password)

        else:

            user = User.objects.filter(email=username).first()

            if user:

                user = auth.authenticate(username=user.username, password=password)

 

        if user is not None:

            auth.login(request, user)

            messages.success(request, "You have been successfully logged in.")

            return redirect('dashboard')  # Replace 'dashboard' with the URL name of your desired landing page after login

        else:

            messages.error(request, "Invalid credentials")  # Set the error message

            return redirect('login')  # Replace 'login' with the URL name of your login page

 

    else:

        messages.get_messages(request)  # Clear any messages from previous requests

        return render(request, "html/login.html")

 

# ... Other view functions ...

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def dashboard(request):
    # Get the current date
    today = date.today()
    reviews = Review.objects.all()  # Retrieve all reviews

    data = Review.objects.filter(created_at__date=today)
    daily_report_count = Review.objects.filter(created_at__date=date.today()).count()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=1, month=today.month % 12 + 1) - timedelta(days=1)

    # Fetch data from the database for the entire month
    monthly_report_count = Review.objects.filter(created_at__date__range=[first_day_of_month, last_day_of_month]).count()
 

    # Calculate the start and end dates for the current week
    start_of_week = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    end_of_week = start_of_week + timedelta(days=6)  # End of the week (Sunday)
    # Fetch data from the database for the entire week
    weekly_report_count = Review.objects.filter(created_at__date__range=[start_of_week, end_of_week]).count()
    # Fetch all available data from the database
    all_reports = Review.objects.all()

    # Calculate the count of all reports
    overall_report_count = all_reports.count()
    # Fetch data from the database for your dashboard here, e.g., latest reviews

    latest_reviews = Review.objects.all().order_by('-created_at')[:5]
    


    
    # Pass the counts as context variables
    context = {
        'daily_report_count': daily_report_count,
        'monthly_report_count': monthly_report_count,
        'weekly_report_count': weekly_report_count,
        'overall_report_count': overall_report_count,
        'latest_reviews': latest_reviews, 
        'reviews':reviews,
        

    }
    return render(request, 'html/dashboard.html', context) 

# ...

from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST['username']
        email = request.POST['your_email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # Corrected field name

        # Check if passwords match
        if password == confirm_password:
            # Check if the user with the provided email already exists
            if User.objects.filter(email=email).exists():
                return render(request, 'html/login.html', {'error': 'Email is already taken.'})

            # Create a new user (no need to pass confirm_password)
            user = User.objects.create_user(username=username, email=email, password=password)

            # Log the user in
            auth_user = authenticate(request, username=username, password=password)

            if auth_user is not None:
                login(request, auth_user)

                # Redirect to a success page or user profile
                return redirect('login')  # Replace 'login' with the URL name of your login page

        else:
            return render(request, 'html/signup.html', {'error': 'Passwords do not match.'})

    return render(request, 'html/signup.html')


def logout(request):

    auth.logout(request)

    return redirect('login')


# Add this line to import settings

# Your other imports and code


def form(request):
    if request.method == 'POST':
        name = request.POST['name']
        department = request.POST['department']
        review_text = request.POST['review']
        rating = request.POST.get('rating[]')

        # Create and save the review
        review = Review.objects.create(name=name, department=department, review=review_text, rating=rating)

        # Prepare context data for the email template
        email_context = {
            'name': name,
            'department': department,
            'rating': rating,
            'review_text': review_text,
        }
         # Load the email template
        email_message = render_to_string('html/email_temp.html', email_context)
       

        # Replace placeholders in the template with actual values
        for key, value in email_context.items():
            email_message = email_message.replace('{{ ' + key + ' }}', value)

        # Send an email
        subject = 'New Review Submitted'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]  # Replace with the email address where you want to receive notifications

        send_mail(subject, '', from_email, recipient_list, html_message=email_message)

        # Redirect to a thank-you page or the same page after submission
        return redirect('successful')

    return render(request, 'html/form.html')






def review_list(request):
    reviews = Review.objects.all()  # Retrieve all reviews
    return render(request, 'html/review_list.html', {'reviews': reviews})


def successful(request):
    return render(request,'html/successful.html')

def fetch_data_for_today(request):
    # Get the current date
    today = date.today()

    # Fetch data from the database for today's date
    data = Review.objects.filter(created_at__date=today)
    

    # Pass the data and context to a template for rendering
    return render(request, 'html/fetch_data_for_today.html', {'data': data})


def fetch_data_for_week(request):
    # Get the current date
    today = date.today()
    
    # Calculate the start date of the current week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    
    # Calculate the end date of the current week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Fetch data from the database for the current week
    data = Review.objects.filter(created_at__date__range=[start_of_week, end_of_week])
    
    # Pass the data to a template for rendering
    return render(request, 'html/fetch_data_for_week.html', {'data': data})



def fetch_data_for_month(request):
    # Get the current date
    today = date.today()
    
    # Calculate the start date of the current month
    start_of_month = today.replace(day=1)
    
    # Calculate the end date of the current month
    next_month = today.replace(day=28) + timedelta(days=4)
    end_of_month = next_month - timedelta(days=next_month.day)
    
    # Fetch data from the database for the current month
    data = Review.objects.filter(created_at__date__range=[start_of_month, end_of_month])
    
    # Pass the data to a template for rendering
    return render(request, 'html/fetch_data_for_month.html', {'data': data})

def fetch_overall_report(request):
    # Fetch all available data from the database
    data = Review.objects.all()
    daily_report_count = Review.objects.filter(created_at__date=date.today()).count()
    context={
        'daily_report_count':daily_report_count,
        'data':data,
    }

    # Pass the data to a template for rendering
    return render(request, 'html/fetch_overall_report.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def base(request):
    return render(request,'html/base.html')

def email_temp(request):
    return render(request,'html/email_temp.html')

def report_view(request):
    # Retrieve the latest five records ordered by the 'created_at' field
    latest_reviews = Review.objects.order_by('-created_at')[:5]

    return render(request, 'html/table.html', {'reviews': latest_reviews})



def download_excel(request):
    # Create a new Workbook and add a Worksheet
    wb = Workbook()
    ws = wb.active

    # Define the headers
    headers = ['Name', 'Department', 'Review', 'Ratings']

    # Write headers to the worksheet
    ws.append(headers)

    # Get your data and add it to the worksheet
    reviews = Review.objects.all()
    for review in reviews:
        row = [review.name, review.department, review.review, f'{review.rating}/5']
        ws.append(row)

    # Create an in-memory stream for the Excel file
    excel_stream = io.BytesIO()
    
    # Save the Workbook to the stream
    wb.save(excel_stream)
    
    # Set the stream's position to the beginning
    excel_stream.seek(0)

    # Create a response with the Excel file
    response = HttpResponse(
        excel_stream.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Set the filename for the Excel file download
    response["Content-Disposition"] = 'attachment; filename="reviews.xlsx"'

    return response

