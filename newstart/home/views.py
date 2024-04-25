from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    response = """
<body>
<h1>LETS MAKE A NEW START</h1>
<p>I AM TARANG KHARKAR, I WILL NEVER STOP</p>
<p>I AM UNSTOPABLE</p>
</body>
"""

    data = [
        {"name": "Tarang", "age": 19}, {"name": "Tanmay", "age": 24}, {"name": "Aditya", "age": 18},
        {"name": "Gagan", "age": 17}
    ]
    return render(request, "home.html", context = {"data": data})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")