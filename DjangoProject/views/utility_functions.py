#  searchterm = request.POST.get('search','')
#         searchTerms = searchterm.split()
#         if request.user.is_superuser:
#             hospital = Hospital2.objects.filter(name__icontains=searchterm)
#             print('hospital',hospital)
#             physician_set = hospital[0].physician_set.all() if hospital else ''
#         print('ps',physician_set)
#         if physician_set:
#             for i in range(len(physician_set)):
#                 if i == 0:
#                     specialty_set = physician_set[i].specialty_ph.all()
#                 else:
#                     specialty_set = specialty_set | physician_set[i].specialty_ph.all()

#         else:
#             for i in range(len(searchTerms)):
#                 if i == 0:
#                     specialty_set = ProductTags.objects.filter(tag__icontains=searchTerms[i])
#                 else:
#                     specialty_set = specialty_set | ProductTags.objects.filter(tag__icontains=searchTerms[i])
#                 specialty_set = specialty_set | ProductTags.objects.filter(products__name__icontains=searchTerms[i])
#                 specialty_set = specialty_set | ProductTags.objects.filter(physicians__firstName__icontains=searchTerms[i])
#                 specialty_set = specialty_set | ProductTags.objects.filter(physicians__lastName__icontains=searchTerms[i])

def returnSearch(searchTerms,object_set,searchMapping):
    
    objects = ''
    category,searchTerms_Z = searchTerms.split("=")
    category = category.strip().lower()
    searchTerm = searchTerms_Z.strip().lower()
    if searchMapping.get(category,''):
        index = {category: {searchMapping[category]:searchTerm}}
        objects = object_set.filter(**index[category])
    
    return objects
  





