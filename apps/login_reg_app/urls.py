from django.conf.urls import url
from . import views

urlpatterns = [
    # 1. Root
    url(r'^$', views.root),

    # 2. Show row
    url(r'^users/(?P<user_id>\d+)$', views.users_showUser),  # localhost:8000/shows/<id>

    # 3. Register and Login
    url(r'^users/reg_login', views.reg_login),
    url(r'^users/reg', views.register),
    url(r'^users/login', views.login),
    url(r'^users/logout', views.logout),
]