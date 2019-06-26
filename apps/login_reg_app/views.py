from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users
# ======================================================================================================================
def get_user_info(user_id):
  return {'user': Users.objects.get(id=user_id)}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def get_all_users_info():
  return {'users': Users.objects.all()}
# ======================================================================================================================
# ======================================================================================================================
def root(request):
  # Initialize session
  if 'user_logged_in' not in request.session:
    request.session['user_logged_in'] = {}
  return redirect("/users/reg_login")
# ======================================================================================================================
def reg_login(request):
  return render(request, "login_reg_app/reg_login.html")
# ======================================================================================================================
def validate(request):

  # Return true if no errors
  valid = False

  # pass the post data to the method we wrote and save the response in a variable called errors
  errors = Users.objects.basic_validator(request.POST, Users.objects.all())

  # check if the errors dictionary has anything in it
  if len(errors) > 0:

    # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
    for key, value in errors.items():
      messages.error(request, value)

    # Errors found
    return valid

  else:
    # No erros => Valid
    valid = True
    return valid

# ======================================================================================================================
def register(request):

  valid = validate(request)
  if valid:

    # Grab values from form
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password_orig = request.POST['password']

    # Hash Password
    password_hash = bcrypt.hashpw(password_orig.encode(), bcrypt.gensalt())

    # Create row in database
    user = Users.objects.create(
      first_name=first_name,
      last_name=last_name,
      email=email,
      password_hash=password_hash)

    messages.success(request, "Successfully registered")
    return redirect("/users/reg_login")
  else: # not-valid
    # redirect the user back to the form to fix the errors
    return redirect("/users/reg_login")
# ======================================================================================================================
# TODO: Show
def users_showUser(request, user_id):
  return render(request, "login_reg_app/show_user.html", get_user_info(user_id))
# ======================================================================================================================
import bcrypt
def login(request):

  # Grab email from form
  email = request.POST['email-login']

  # Grab row from database
  user = Users.objects.get(email=email)

  # Grab entered password and test against stored hash
  password_login = request.POST['password-login']
  if bcrypt.checkpw(password_login.encode(), user.password_hash.encode()):
    print("password match")

    # Set Session with logged-in users info
    request.session['user_logged_in'] = {
      'id': user.id,
      'first_name': user.first_name,
      'logged_in': True
    }

    return render(request, "login_reg_app/logged_in.html", {'user': user})
  else:
    print("failed password")
    return HttpResponse("You Loose!")

  return 0
# ======================================================================================================================
def logout(request):
  request.session.pop('user_logged_in')
  return redirect("/")
# ======================================================================================================================