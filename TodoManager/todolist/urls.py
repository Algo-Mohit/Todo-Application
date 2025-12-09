from django.urls import path , include
from todolist import views

urlpatterns = [
    path('',views.home,name="home"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('todolist/delete/<task_id>/',views.task_delete,name="task_delete"),
    path('todolist/edit/<task_id>/',views.task_edit,name="task_edit"),
    path('todolist/update_status/<task_id>/',views.update_status,name="update_status"),
    path('todolist/',views.todolist,name="todolist"),

]
 