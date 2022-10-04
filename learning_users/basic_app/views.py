from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# importing for login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

#The decorator login_required will guarantee that only a user that is logged in can logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('You are logged in, Nice!')


def register(request):
    
    # Depend on this variable to check if someone is registered or not
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            # Set the user_form data to the variable form and save it directly to the database
            user = user_form.save()
            # Hashes the user's password by using the set_password method that goes to the settings.py file 
            # and set it as the hash and then, saves it to the database
            user.set_password(user.password)
            user.save()
            
            # We set the profile_form data to the profile variabe but we set commit=False
            # so we can manipulate the data before saving to avoid collision errors
            profile = profile_form.save(commit=False)
            
            # Sets up the one to one relationship as we did in models
            # We are linking three files (views.py, forms.py and models.py)
            # We need to do it to add the extras to the profile
            profile.user = user
            
            
            # If we want to upload any file (pic, cv, pdf etc) we will use request.FILES
            if 'profile_pic' in request.FILES:
                # Set the attribute profile_pic to the request.FILES that acts like a dictionary and we will pass 
                # What we created in the models for this attribute.
                profile.profile_pic = request.FILES['profile_pic']
                
            profile.save()
            
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        # If the request was an HTTP request we will pass the instance of the forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    # returning everything to the page
    return render(request, 'basic_app/registration.html',
                                    {'user_form': user_form,
                                     'profile_form':profile_form,
                                     'registered': registered})
    

# Creating the view for the login page
def user_login(request):
    if request.method == 'POST':
        # Grabbing the information from the HTML using the name passed there
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticating the user and password using the imported authenticate
        user = authenticate(username=username, password=password)
        
        # If the user was authenticated
        if user:
            # Checking if the account is active
            if user.is_active:
                # Log the user in
                login(request, user)
                # Send the user back to index page 
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("Account not active")
        
        else:
            print("Someone tried to login and failed!")
            print(f"Username:{username} and Password:{password}")
            return HttpResponse("Invalid Login details supplied!")
    else:
        return render(request,'basic_app/login.html', {})