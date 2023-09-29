from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from recipe.views import RegisterView, CommentView, RatingView

urlpatterns = [
    # Основные ссылки
    path('', include('backend.routers')),

    # Авторизация через JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Регистрация
    path('register/', RegisterView.as_view()),

    # Комментарии
    path('comments/', CommentView.as_view()),  # Для создания комментов
    path('comments/<slug:recipe_slug>/', CommentView.as_view()),  # Получение комментов к определённому рецепту

    # Рейтинг
    path('rating/', RatingView.as_view()),  # Для создания рейтинга
    path('rating/<slug:recipe_slug>/', RatingView.as_view()),  # Получение рейтинга к определённому рецепту
]
