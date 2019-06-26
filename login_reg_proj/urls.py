from django.conf.urls import url, include
urlpatterns = [
    url(r'^', include('apps.login_reg_app.urls')),
    # url(r'^admin/', admin.sites.urls)
]