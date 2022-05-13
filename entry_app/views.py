from django.shortcuts import render
from Music_platform.settings import AUTH_USER_MODEL as user
from django.views.generic import TemplateView


# Create your views here
class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request):
        if request.user.is_authenticated:
            pass
        else:
            return render(request, self.template_name, {})


# change both to class (from this guide:  https://www.youtube.com/watch?v=oDCmxpEJS_0)
def login():
    pass


def register():
    pass
