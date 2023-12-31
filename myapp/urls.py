from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import UpdateClusterTxtFileView

urlpatterns = [
    path("getAnswer/<int:cluster_id>/", views.getReply, name="getAnswer"),
    path("", views.home, name="home"),
    path("register/", views.register.as_view(), name="register"),
	path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html',authentication_form=LoginForm), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='myapp/home.html'), name='logout'),
	path('profile/', views.profile, name='profile'),
	path('create_cluster/', views.create_cluster, name='create_cluster'),
	path('updatebot/<int:pk>/', UpdateClusterTxtFileView.as_view(), name='updatebot'),
	path('deletebot/<int:cluster_id>/', views.deletebot, name='deletebot'),
	path('gettemplate/<int:cluster_id>/', views.gettemplate, name='gettemplate'),
	# path('cluster/<int:cluster_id>/', views.cluster_details, name='cluster_details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)