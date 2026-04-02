from django.urls import include, path


from subscriber.drf import  functionals




app_name = "story"

urlpatterns = [
   path("signup/", functionals.signup_view, name="signup"),
path("login/", functionals.login_view, name="login"),  
  
]