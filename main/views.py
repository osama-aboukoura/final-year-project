from django.http import HttpResponse

# Create your views here.
def index (request):
    return HttpResponse("<h1>Welcome Page. Sign up / Sign In</h1>")
