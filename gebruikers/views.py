# -*- coding: utf-8 -*-

from django.shortcuts import render
from .forms import UserForm, UserCompanyForm, UserLoginForm
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('NFSP_Website:home'))


@user_passes_test(lambda u: not u.is_authenticated, login_url='/', redirect_field_name='')
def register(request):
    registered = False
    if request.method == 'POST':
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        company_form = UserCompanyForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and company_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()

            company = company_form.save(commit=False)
            # Set One to One relationship between
            company.user = user
            # Now save model
            company.save()
            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, company_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        company_form = UserCompanyForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'gebruikers/registration.html',
                          {'user_form': user_form,
                           'company_form': company_form,
                           'registered': registered})


@user_passes_test(lambda u: not u.is_authenticated, login_url='/', redirect_field_name='')
def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        user_login_form = UserLoginForm(data=request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=user_login_form.data['username'], password=user_login_form.data['password'])

        # If we have a user
        if user:
            # Check if the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('gebruik:register'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        user_login_form = UserLoginForm()
        return render(request, 'gebruikers/login.html', {'user_login_form': user_login_form})
