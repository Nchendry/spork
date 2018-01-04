from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from django.db import models

class UserManager(models.Manager):
    def validate_registration(self, POST):
        today = datetime.datetime.today()
        print "Hello World "*10
        print POST
        print POST['name']
        errors=[]
        if len(POST['name']) == 0:
            errors.append('Name is a required field')
        elif len(POST['name']) < 2:
            errors.append('Name must have at least three characters')
        if len(POST['username']) == 0:
            errors.append('Username is a required field')
        elif len(POST['name']) < 3:
            errors.append('Username must have at least three characters')
        elif len(User.objects.filter(username=POST['username'])) != 0:
            errors.append('Username is already in use')
        if len(POST['start']) == 0:
            errors.append('Hire date is required')
        if(POST['start'] > str(today)):
            errors.append('Start date must be in the past')
        if len(POST['password']) == 0:
            errors.append('Password is a required field')
        elif len(POST['password']) < 8:
            errors.append('Password must have at least eight characters')
        elif POST['password'] != POST['confirm_password']:
            errors.append('Passwords do not match')
        if len(errors) > 0:
            print errors
            print "false"
            return (False, errors)

        else:
            pwhash = bcrypt.hashpw((POST['password'].encode()), bcrypt.gensalt(5))

            new_user = User.objects.create(
                name = POST['name'],
                username = POST['username'],
                hire_date = POST['start'],
                password = pwhash
            )        
            return (True, new_user)


    def login(self, POST):
        errors = []
        if len(POST['username']) == 0:
            errors.append('Please enter a valid Username')
        if len(POST['password']) == 0:
            errors.append('Password must be entered')
        elif len(self.filter(username=POST['username'])) != 0:
            user = self.filter(username=POST['username'])[0]
            if not bcrypt.checkpw(POST['password'].encode(), user.password.encode()):
                errors.append('Username/Password combination invalid')
        else: 
            errors.append('Username/Password combination invalid')
        if len(errors) > 0:
            return (False, errors)
        return (True, user)

class ItemManager(models.Manager):
    def validateItem(self, POST, id):
        errors = []
        if len(POST['product']) == 0:
            errors.append('Item name is required')
        elif len(POST['product']) < 4:
            errors.append('Item must be at least 4 characters')
        
        if len(errors) > 0:
            return (False, errors)
        else:
            new_item = Item.objects.create(
                product = POST['product'],
                wisher_lister = User.objects.get(id=id),
            )        
        return (True, new_item)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 
    hire_date = models.DateField(auto_now=False, auto_now_add=False)

    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    product = models.CharField(max_length=255)

    wisher_lister = models.ForeignKey(User, related_name="items")
    also_wants = models.ManyToManyField(User, related_name="wanted_by")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager();
