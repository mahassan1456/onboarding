
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
import json
from io import BytesIO as IO
import pandas as pd




def debuggingCode(function,line,var_names):

    print(f"Function: {function} Line: {line} Variables: {var_names}")



def sortDict(dictionary):
    """sorts keys by converting to dictionary keys and looping through 
    them after sorting and in the process bringing in the  values in the correct order"""
    myKeys = list(dictionary.keys())
    myKeys.sort()
    sorted_dict = {i: dictionary[i] for i in myKeys}
    return sorted_dict

def compareModels(model1, model2):
    from django.forms.models import model_to_dict

    return list(model_to_dict(model1)) == list(model_to_dict(model2))

def models2json(productsStr):
    
    productsJSON = {}
    for specialty,product in productsStr.items():
        productlist = []
        for x in product:
            if type(x) == str:
                productlist.append(json.loads(x))
            else:
                productlist.append(x)
        productsJSON[specialty] = productlist
    return productsJSON

def user_directory_path_physicians(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'physician/{0}_{1}/{2}'.format(instance.firstName,instance.lastName ,filename)

def user_directory_path_products(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'products/{0}/{1}'.format(instance.name,filename)

def user_directory_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'products/{0}_{1}/{2}'.format(instance.firstName,instance.lastName ,filename)

# convert from dataframe to excel respone object
def returnExcelResponse(dataframe,sheet='default',file_name='excelfile'):
    byteStream = IO()
    # Assign the memory buffer to the excel byte stream so  excelwriter can know where and what is it is writing to IO can know how to represent it in memory
    xls_bytestream = pd.ExcelWriter(byteStream, engine='xlsxwriter')
    #write excel file to memory which is the XLS Bytestream
    dataframe.to_excel(xls_bytestream,sheet_name=sheet)
    xls_bytestream.close()
    #Byte stream is finished writing to memory but the cursor is at the end of the stream. Seek back to beginning so User can download from beginning.
    byteStream.seek(0)
    # create an HTTP response with the bytestream to be downloaded by the user. Content Type
    response = HttpResponse(byteStream)
    response["Content-Type"] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename={r}.xlsx'.format(r=file_name)

    return response
# creates a tuple e.g (<Product Object>, "checked" || or "") to rebuild selections of previously selected products
def rebuildProductList(physician):
    from pproducts.models import ProductTags
    # physician_specialties = ProductTags.objects.filter(id__in=physician.specialty_ph.values_list('id', flat=True))
    physician_specialties = ProductTags.objects.filter(physicians=physician)
    productIdsforPhysician = physician.productitems.values_list('id', flat=True)
    labeled_specialty_set = {specialty.tag: specialty.products.all() for specialty in physician_specialties }
    allProducts = {specialty: [ (product,"checked") if product.id in productIdsforPhysician else (product, "") for product in products ]  for specialty,products in labeled_specialty_set.items() }
    return allProducts, physician_specialties

def uploadToWooCommerce(json={},product=''):

    data = {
    "name": product.name,
    "type": "",
    "regular_price": "",
    "description": product.description,
    "short_description": "",
    "categories": [
        {
            "id": 9
        },
        {
            "id": 14
        }
    ]
}



