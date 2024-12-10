from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import Schedule,Seat,booking_history
from .forms import BusSearchForm,BookingForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
from io import BytesIO
from django.contrib.auth.models import User
import logging
import traceback

logger = logging.getLogger(__name__)

def home(request):
    # print("Is user authenticated:", request.user.is_authenticated)
    return render(request,'home.html')

@login_required
def search_buses(request):
    # print("Is user authenticated:", request.user.is_authenticated)
    # print("User :", request.user)
    print(request)
    form = BusSearchForm()
    results = []

    if request.method == "GET" and 'from_city' in request.GET:
        form = BusSearchForm(request.GET)
        if form.is_valid():
            from_city = form.cleaned_data['from_city']
            to_city = form.cleaned_data['to_city']
            journey_date = form.cleaned_data['journey_date']

            results = Schedule.objects.filter(
                route__from_city=from_city,
                route__to_city=to_city,
                departure_date=journey_date
                
                
            )

    return render(request, 'search_buses.html', {'form': form, 'results': results})

def view_seats(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    seats = Seat.objects.filter(schedule=schedule)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # seat_number = form.cleaned_data['seat_number']
            seat_number = request.POST.get('seat_number')
            print(seat_number)
            seat = Seat.objects.get(schedule=schedule, seat_number=seat_number)
            if not seat.is_booked:
                seat.is_booked = True
                seat.save()
                schedule.available_seats -= 1
                schedule.save()
                booking=booking_history.objects.create(seat=seat, name=form.cleaned_data['name'], email=form.cleaned_data['email'])
                # return redirect('view_seats', schedule_id=schedule_id)
                # 
                pdf_buffer = generate_ticket_pdf(booking)
                response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
                send_ticket_email(booking)
                return response
            else:
                form.add_error('seat_number', 'Seat is already booked')
    else:
        form = BookingForm()
    return render(request, 'view_seats.html', {'schedule': schedule, 'seats': seats,'form':form})

def signup(request):
    # if request.method == 'POST':
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=raw_password)
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     form = SignUpForm()
    # return render(request, 'signup.html', {'form': form})
    
    
    
    # if request.method == 'POST':
        
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
        
    #     try:
    #         user = User.objects.create_user(username=username, password=password)
    #         user.save()
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         print("User registered and logged in successfully")
    #         return redirect('home')
    #     except:
    #         messages.error(request, 'Registration failed')
    
    # return render(request, 'signup.html')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Detailed print statements for debugging
        print(f"Received username: {username}")
        print(f"Received password: {password}")
        print(f"Received confirm password: {confirm_password}")
        
        try:
            # Explicit user creation with more detailed error handling
            user = User.objects.create_user(
                username=username, 
                email=username,  # Use email as username if that's your intent
                password=password
            )
            user.save()
            
            print(f"User created: {user.username}")
            
            # Authenticate and login
            authenticated_user = authenticate(username=username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                print("User authenticated and logged in")
                messages.success(request, 'Registration successful')
                return redirect('home')
            else:
                print("Authentication failed")
                messages.error(request, 'Authentication failed')
                return render(request, 'signup.html')
        
        except Exception as e:
            # Extensive error logging
            print(f"Error creating user: {str(e)}")
            print(traceback.format_exc())
            logger.error(f"User creation error: {str(e)}")
            logger.error(traceback.format_exc())
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def login_view(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            
            return redirect('home')
        else:
            
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def generate_ticket_pdf(booking):
    # Render the ticket template
    html_string = render_to_string('ticket_template.html', {'booking': booking})
    html = HTML(string=html_string)

    # Create a response object
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
    
    # # Write the PDF to the response
    # html.write_pdf(response)

    # return response
    pdf_buffer = BytesIO()
    html.write_pdf(pdf_buffer)
    pdf_buffer.seek(0)  # Go to the beginning of the BytesIO buffer

    return pdf_buffer

def send_ticket_email(booking):
    # Generate the PDF
    pdf_buffer = generate_ticket_pdf(booking)

    # Create the email
    email = EmailMessage(
        subject='Your Ticket',
        body='Please find your ticket attached.',
        from_email='das05bishal@gmail.com',  # Replace with your email
        to=[booking.email],  # Assuming booking has a user attribute with email
    )

    # Attach the PDF
    email.attach(f'ticket_{booking.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send()