from django.http import HttpResponse
from platform import freedesktop_os_release
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import studentdetails, bookdetails, bookreservationdata
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Avg

# Create your views here.

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required
def dash(request):
    freshmandata = studentdetails.objects.filter(year='Freshman').count()
    sophomoredata = studentdetails.objects.filter(year='Sophomore').count()
    juniordata = studentdetails.objects.filter(year='Junior').count()
    seniordata = studentdetails.objects.filter(year='Senior').count()
    totalstudents = studentdetails.objects.all().count()
    average = studentdetails.objects.all().aggregate(result = Avg('gpa'))
    averagegpa = average.get('result')
    averagegpa = float(averagegpa)
    context = {'freshman':freshmandata, 'sophomore':sophomoredata, 'junior':juniordata, 'senior':seniordata, 'total': totalstudents, 'avggpa': averagegpa}
    return render(request, 'books/dash.html', context)

@login_required
def studentdet(request):
    studentdata = studentdetails.objects.all()
    paginator = Paginator(studentdata, 10)
    page = request.GET.get('page')
    pagedata = paginator.get_page(page)
    context = {'data':pagedata}
    return render(request, 'books/studentdet.html', context)

@login_required
def bookdet(request):
    cursorobj = connection.cursor()
    cursorobj.execute("select * from books_bookdetails order by numcheckedout desc")
    bookdata = dictfetchall(cursorobj)
    paginator = Paginator(bookdata, 10)
    page = request.GET.get('page')
    pagedata = paginator.get_page(page)
    context = {'data':pagedata}
    return render(request, 'books/bookdet.html', context)

@login_required
def bookres(request):
    studentdata = studentdetails.objects.all()
    bookdata = bookdetails.objects.all()
    cursorobj = connection.cursor()
    cursorobj.execute("select * from books_bookdetails where currentlyout= false")
    booksin = dictfetchall(cursorobj)
    context = {'student': studentdata, 'book': bookdata, 'booksin': booksin}
    return render(request, 'books/bookres.html', context)

@login_required
def savereservation(request):
    if('studentid' and 'booktitle' in request.GET):
        student = request.GET.get('studentid')
        book = request.GET.get('booktitle')
        studentbooksreserved = bookreservationdata.objects.filter(studentid=student).count()
        bookedonce = bookreservationdata.objects.filter(booktitle=book).count()
        if studentbooksreserved < 5 and bookedonce < 1:
                data = bookreservationdata(studentid = student, booktitle = book)
                data.save()
                cursorobj = connection.cursor()
                cursorobj.execute("update books_bookdetails set currentlyout = true, numcheckedout = numcheckedout + 1 where booktitle = '%s'" % book)
                return HttpResponse("Success")
        else:
            print("This student has already reserved their allotted four books")
            return HttpResponse("Error")

