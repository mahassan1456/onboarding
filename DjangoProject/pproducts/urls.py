
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'pproducts'


urlpatterns = [
    
    path('addphysician/', view=views.addphysician,name='addphysician'),
    path('refresh/', views.rfsh_products,name='rfsh_products'),
    path('products/', views.products, name='products' ),
    path('physician/', view=views.physician, name='physician'),
    path('downloadxls/', views.downloadXLS, name='downloadxls'),
    path('editphysician/<int:id>/', views.edit_physician, name='edit_physician'),
    path('displayproducts/', views.displayProducts,name='displayproducts'),
    path('addproducts/physician/<int:id>/', views.product2physician,name='product2physician'),
    path('product/addnew/', view = views.addProduct, name="addproduct"),
    path('products/tags/', views.addTags, name="addtags" ),
    path('product/edit/<int:id>/', views.editproduct, name="editproduct"),
    path('products/addnewtags/<int:id>/', views.addTags2Physician1, name="addtags2physician" ),
    path('products/tags/<int:id>/', views.editTags, name='edittags'),
    path('addhospital/admin/<int:id>/', view=views.assignFacilityAdmin, name="assignfacility" ),
    path('remove/physician/<int:id>/', views.removephysician, name="removephysician"),
    path('redesign/', view=views.products_redesign, name='products_redesign'),
    path('filterproducts/script/',view=views.filterProducts),
    path('filter/hospital/', views.buildHospital, name='buildhospital'),
    path('remove/product/<int:id>/', views.removeProduct, name='removeProduct'),
    path('response/buildspecialties/', view=views.buildSpecialties, name='buildSpecialties'),
    path('products/allorcurrent/', views.filterAllorCurrent,name='filterAllOrCurrent'),
    path('fromwoocommerce',views.pullFromWooCommerce,name="fromwoo")
    # path('filterproducts/<int:id>/', views.filterProducts, name="filterproducts")
    
    # path('products/addtags/physician/', view=views.AddTags2Physician, name="add2phys")

]

# def addTags2Physician(request):
#     print("test")
#     header = 'Add Specialty'
#     button_text = 'Update Physician'
#     queryset = ProductTags.objects.all().order_by('tag')
#     if request.method == "POST":
#         pass
#     form = AddTags2Physician()

#     return render(request, template_name='pproducts/addphysician.html', context={'form':form, 'button_text': button_text, 'header': header, 'tags': queryset})