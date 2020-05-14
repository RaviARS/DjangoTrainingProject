from django.urls import path
from .views import CustomerList, CustomerDetails

urlpatterns = [

    path('details/', CustomerList.as_view()),
    path('detail/<int:id>/', CustomerDetails.as_view()),

]
