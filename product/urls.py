from django.urls import path

from product.views import ProductView, ProductDetails, ProductSlugDetails, ProductFeature, ProductFeatureDetails

app_name = 'product'
urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    # path('<pk>', ProductDetails.as_view(), name='details'),
    path('<slug>/', ProductSlugDetails.as_view(), name='details'),
    # path('feature/', ProductFeature.as_view(), name='feature'),
    # path('feature/<pk>', ProductFeatureDetails.as_view(), name='feature_details'),
]
