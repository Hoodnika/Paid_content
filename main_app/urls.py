from django.urls import path
from django.views.decorators.cache import cache_page

from main_app.apps import MainAppConfig
from main_app.views import PublicationListView, PublicationSearchView, PublicationDetailView, PublicationAuthorListView, \
    PublicationCreateView, PublicationUpdateView, PublicationDeleteView, buy_subscription, my_webhook_view

app_name = MainAppConfig.name

urlpatterns = [
    path('main/', cache_page(60)(PublicationListView.as_view()), name='main'),
    path('<int:pk>/', cache_page(30)(PublicationAuthorListView.as_view()), name='publication_owner'),
    path('search/', cache_page(30)(PublicationSearchView.as_view()), name='search'),

    path('publication/<str:slug>/', cache_page(120)(PublicationDetailView.as_view()), name='publication_detail'),
    path('pub/create/', cache_page(360)(PublicationCreateView.as_view()), name='publication_create'),
    path('pub/update/<int:pk>/', cache_page(360)(PublicationUpdateView.as_view()), name='publication_update'),
    path('pub/delete/<int:pk>/', cache_page(30)(PublicationDeleteView.as_view()), name='publication_delete'),

    path('subscriptions/', cache_page(120)(buy_subscription), name='subscription_create'),
    path('webhooks/stripe/', my_webhook_view, name='stripe-webhook'),
]
