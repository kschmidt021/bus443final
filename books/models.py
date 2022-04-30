from django.db import models

class studentdetails(models.Model):
    studentid = models.IntegerField()
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=500)
    major = models.CharField(max_length=500)
    year = models.CharField(max_length=500)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)

class bookdetails(models.Model):
    bookid = models.IntegerField()
    booktitle = models.CharField(max_length=500)
    authorname = models.CharField(max_length=500)
    currentlyout = models.BooleanField()
    numcheckedout = models.IntegerField()

class bookreservationdata(models.Model):
    studentid = models.IntegerField()
    booktitle = models.CharField(max_length=500)
    