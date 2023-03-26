from django.apps import AppConfig


class ViewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "views"

    def ready(self):
        from . import signals
        return super().ready()
    


# def buildProductCards1(request):
#     productTagProducts = ''
#     buildAllTab = ''
#     model = ''
#     products = ''
#     physician = request.POST.get('physician','')
#     hospital = request.POST.get('hospital','')
#     specialty = request.POST.get('specialty','')
#     buildSpecial = False

#     print('specccc',specialty)
    
#     if specialty:
#         try:
#             specialty_model = ProductTags.objects.get(tag=specialty)
#         except (ProductTags.DoesNotExist,Exception) as error:
#             print(error)

#         if hospital and physician:
#             print('here2')

#         elif hospital:
#             print('here3')
#             hospital = int(hospital)
#             try:
#                 hospital_model = Hospital2.objects.get(id=hospital)
#             except (Hospital2.DoesNotExist,Exception):
#                 print(error)
#             else:
#                 physician_set = hospital_model.physician_set.all()
#                 product_array_set = set()
            
#                 for physician_ in physician_set:
#                     prods = physician_.productitems.all() if specialty == 'all' else physician_.productitems.filter(specialties__tag__in=[specialty])
#                     print("prods",prods)
#                     for prod in prods:
#                         product_tuple = (prod, prod.getPictureURL() ,prod.buildSpecialtiesString() )
                    
                    
#                         product_array_set.add(product_tuple)
            
#                 productTagProducts = [(model_to_dict(prodTup[0]),prodTup[1],prodTup[2])  for prodTup in product_array_set ]
#                 buildSpecial = True
            
#         elif physician:
#             print('here4')
#             buildAllTab = True
#             try:
#                 if physician == 'all':
#                     if specialty == 'all':
#                         products = Product.objects.all()
#                     else:
#                         products = specialty_model.products.all()
#                 else:
#                     try:
#                         physician = int(physician)
#                         model = Physician.objects.get(id=physician)
#                         prods = specialty_model.products.all()
#                     except (Physician.DoesNotExist,Exception) as error:
#                         print(error)
#                         return
#                     if specialty == 'all':
#                         prods = Product.objects.all()
#                         productTagProducts1 = [(model_to_dict(prod),prod.getPictureURL(),specialty,True if prod in model.productitems.all() else False) for prod in prods]
#                         print('24',productTagProducts1)
#                         productTagProducts = [(model_to_dict(Product.objects.get(id=prod['id'])),Product.objects.get(id=prod['id']).getPictureURL(),key,True) for key,value in model.products.items() for prod in value]
#                         buildSpecial = True
#                     else:
#                         productTagProducts1 = [(model_to_dict(prod),prod.getPictureURL(),specialty,True if prod in model.productitems.all() else False) for prod in prods]
#                         print('24',productTagProducts1)
#                         products = model.linkedtags.filter(tag=specialty)[0].products.all()

#             except (Physician.DoesNotExist,Exception) as error:
#                 print(error)
#                 return HttpResponse(f"Error-{error}")
            
#         else:
#             print('here5')

#             if specialty == 'all':
#                 try:
#                     products = Product.objects.all()
#                 except (Product.DoesNotExist,Exception) as error:
#                     print(error)
                

#             else:
#                 try:
                    
#                     model = ProductTags.objects.get(tag=specialty)
#                     products = model.products.all()
                    
#                 except (ProductTags.DoesNotExist,Exception) as error:
#                     print(error)

#         if not buildSpecial:
#             productTagProducts = [( model_to_dict(prod), prod.getPictureURL(), prod.buildSpecialtiesString() )  for prod in products]
#         for product in productTagProducts:
                    
#                     product[0].pop('picture')
#                     product[0].pop('created_at')
#         print(productTagProducts)
#         print("did it come here")
#         return JsonResponse(data={'dataset':productTagProducts,'buildAll':buildAllTab})
