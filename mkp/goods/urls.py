from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('',GoodsList.as_view(), name='goods'),
    path('category/', category, name='categories'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('good/<slug:good_slug>/', ShowGood.as_view(), name='good'),
    path('add_good', AddGood.as_view(), name='add_good'),
    path('category/<slug:cat_slug>/', GoodCategory.as_view(), name='category'),
    path('brand/<slug:brand_slug>/', GoodBrand.as_view(), name='brand'),
    path('update_stock/', update_stock, name='update_stock'),
    path('prom/export.xlsx', ExportFileView.as_view(), name='prom'),
    path('export/', ExportView.as_view(), name='export'),
    path('import/', ImportView.as_view(), name='import'),
    path('update-export/', update_export_file, name='update_export_file'),
    path('search-goods/', search_goods, name='search_goods'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)