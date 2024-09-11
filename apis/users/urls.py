from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


from .views import CreateUserView, ChangePasswordView, UserUpdateView, DeactivateUserView

app_name = 'users'
urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("deactivate/", DeactivateUserView.as_view(), name="deactivate"),
    path("user-update/", UserUpdateView.as_view(), name="user_update"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
