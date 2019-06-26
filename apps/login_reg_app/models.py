from django.db import models
import re # regex module

# Custom manager for validation
class UsersManager(models.Manager):
    def basic_validator(self, postData, users):

      # Validation 1: Does name contain numbers?
      def hasNumbers(inputString):  # https://stackoverflow.com/a/19859308
        return any(char.isdigit() for char in inputString)

      errors = {}
      # add keys and values to errors dictionary for each invalid field

      # Validation 1 and 2:
      # Ensures names are at least of minimum length and do not contain numbers
      min_name_len = 1
      if len(postData['first_name']) < min_name_len or hasNumbers(postData['first_name']):
        errors["first_name"] = "first-name should be at least " + str(min_name_len) + " characters"
      if len(postData['last_name']) < min_name_len or hasNumbers(postData['last_name']):
        errors["last_name"] = "last-name should be at least " + str(min_name_len) + " characters"

      #  Validation 3: Does email have proper form?
      EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # create a regular expression object
      if not EMAIL_REGEX.match(postData['email']):  # test whether a field matches the pattern
        errors["email"] = "email does not have proper form"

      # Validation 4: Does second password match first?
      if(postData['password'] != postData['password-confirm']):
        errors["password"] = "Password entered does not match confirmation"

      # Validation 5: Ensure email is not already in database
      for user in users:
        if user.email == postData["email"]:
          errors["email_in_db"] = "Already registered!"
          break

      return errors
# ======================================================================================================================
# Table-1:
class Users(models.Model):
  #id
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  email = models.CharField(max_length=64)
  password_hash = models.CharField(max_length=128)
  # logged_in = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UsersManager()  # add this line!

  def __repr__(self):
    return f"Users: ({self.first_name}, {self.last_name}, {self.email})"