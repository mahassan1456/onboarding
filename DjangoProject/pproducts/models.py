from django.db import models
from django.utils import timezone
import json
from PIL import Image
from django_resized import ResizedImageField
from pproducts.helper_functions import user_directory_path_products, user_directory_path_physicians
from django.forms.models import model_to_dict
from pproducts.fields import MyJsonField
from simple_history.models import HistoricalRecords
from woocommerce import API
# from mysite.settings import WOOCOMMERCE_CUSTOMER_KEY, WOOCOMMERCE_CUSTOMER_SECRET,WOOCOMMERCE_API_URL_DEV
from django.utils import timezone, dateformat
from superuseractions.models import UserHistoryTable

















def physicianDefaultProducts():
    return {}

class Specialty(models.Model):
    
    specialty_sp = models.CharField(max_length=100,null=False, default="",blank=True)

    class Meta:
        ordering = ['specialty_sp']

    def __str__(self):
        return f"Specialty - {self.specialty_sp}"
        
class Product(models.Model):
    shop_recovery_id = models.PositiveIntegerField(verbose_name="Shop-Recovery ID",null=True,blank=True)
    name = models.CharField(max_length=100, null=True,blank=False)
    description = models.TextField(null=True,blank=True)
    short_description = models.TextField(max_length=500, null=True,blank=True,default='')
    price = models.CharField(max_length=10, null=True,blank=True, default='')
    quantity = models.PositiveIntegerField(null=True,blank=True)
    category = models.CharField(max_length=50, null=True,blank=True)
    picture = models.ImageField(upload_to=user_directory_path_products, null=True,blank=True)
    manufacturer = models.CharField(max_length=30,null=True,default="",blank=True)
    UPC = models.CharField(max_length=25,null=True, default="",blank=True)
    SKU = models.CharField(max_length=30,null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    previous_specialty_string = models.CharField(max_length=256,null=True,default='')
    created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    
    def returnCreatedAt(self):
        return self.created_at.strftime('%B %d, %Y %I:%M %p')
    
    def returnUpdatedAt(self):
        return self.updated_at.strftime('%B %d, %Y %I:%M %p')
    

    class Meta:
        ordering = ['name']
    
    def save(self,*args,**kwargs):

        super().save(*args,**kwargs)

    def savePreviousTagsAndSave(self):
        if self.specialties.all():
            
            self.previous_specialty_string = self.buildSpecialtiesString()
            
        self.save()
        

    def checkState(self,data_s=[],object_dict={},):
        action_obj = {}
        delta = False
        if data_s:
            for data in data_s:
                if data == 'specialties':
                    print('previosusspstring',self.previous_specialty_string)
                    print('spefl.specialties.all',self.specialties.all())
                    action_obj[data] = {'old':self.previous_specialty_string,'new': self.buildSpecialtiesString() } 
                elif data == 'picture':
                    picture = object_dict['picture']
                    if picture:
                        action_obj[data] = {"old":picture.url,"new": self.picture.url if self.picture else ''}
                else:
                    action_obj[data] = {'old':object_dict.get(data,''),'new': getattr(self,data) }
        return action_obj 
        
    def removeProduct(self,physician):
        pass
    def __str__(self):
        return f"{self.name}"
    
    def countSpecialties(self):
        from pproducts.models import ProductTags

        return ProductTags.objects.filter(products__in=[self]).count()

    def countPhysiciansSuper(self):
        from pproducts.models import Physician
       
        return Physician.objects.filter(productitems__in=[self]).count()
        
    def countPhysicians(self,facility=0):
        from pproducts.models import Physician
        return Physician.objects.filter(productitems__in=[self],facility__id=facility).count()
    # def logHistory(self):
    #     pass

    def buildBullets(self):
        return self.description.split('\n')
    def getPictureURL(self):
        if self.picture:
            return self.picture.url
        return '/media/products/Bauerfeind EpiTrain/elbowbrace3.png'
    
    def buildSpecialtiesString(self):
        return ", ".join(list(map(lambda x: x.tag, list(self.specialties.all()))))


    def logHistory(self,user,created=False):
        time_format = dateformat.format(self.created_at, 'Y-m-d')
        if not created:
            record = self.history.latest()
            record.history_change_reason = f"{user} Updated Product {self.name}"
        else:
            record = self.history.latest()
            record.history_change_reason = f"{user} Created Product {self.name}"
        record.save()
        self.save()
    
    def getFirstImage(self):
        

        if self.images.all():
         
         return self.images.all()[0].image
        return '/media/no_image_available.jpg'
            
    def buildProductDictwImages(self):
        model_dict = model_to_dict(self)
        model_dict.pop('created_at')

        model_dict['picture'] = [image.image for image in self.images.all() ]
        model_dict['specialties'] = self.buildSpecialtiesString()
        model_dict['description'] = model_dict['description'].split('\n')

        return model_dict

    def sendToWooCommerce(self,updateOrCreate=''):
        if updateOrCreate:
            tags= []
            if self.specialties.exists():
                tags = [{"id": tag.shop_recovery_id } for tag in self.specialties.all() ]
            wcapi = API(
                url=WOOCOMMERCE_API_URL_DEV,
                consumer_key=WOOCOMMERCE_CUSTOMER_KEY,
                consumer_secret=WOOCOMMERCE_CUSTOMER_SECRET,
                version="wc/v3"     
            )
            data = {
                "name": self.name,
                "type": "simple",
                "regular_price": self.price,
                "description": self.description,
                "short_description": self.short_description,
                
            }
            try:
                if updateOrCreate == 'create':
                    product = wcapi.post("products", data).json()
                elif updateOrCreate == 'update':
                    product = wcapi.put(f"products/{self.shop_recovery_id}", data).json()
            except (Exception,TimeoutError) as error:
                print(error)
            print(product)
            if isinstance(product,dict):
                self.shop_recovery_id = product['id']
            self.save()

    # def save_no_history(self, *args, **kwargs):
    #     self.skip_history_when_saving = True
    #     try:
    #         ret = self.save(*args, **kwargs)
    #     finally:
    #         del self.skip_history_when_saving
    #     return ret

def user_directory_path_images_product(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'products/{0}_{1}/{2}'.format(instance.product.name,instance.product.id ,filename)
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name='images')
    image = models.CharField(default='',null=True,max_length=256)

class LinkedProductTags(models.Model):
    parentTag = models.ForeignKey(to='pproducts.ProductTags', on_delete=models.CASCADE,null=True, related_name='parenttags')
    physician = models.ForeignKey(to='pproducts.Physician',null=True,on_delete=models.CASCADE,related_name='linkedtags')
    products = models.ManyToManyField(to='pproducts.Product',null=True)
    tag = models.CharField(max_length=50, null=False, default="", unique=False, blank=False)
    description = models.TextField(max_length=1000,null=True,default="")
    created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    

    class Meta:
        ordering = ['tag']
    

class Physician(models.Model):
    shop_recovery_id = models.PositiveIntegerField(null=True,blank=True)
    facility = models.ForeignKey(to="medical.Hospital2",on_delete=models.CASCADE, null=True,default="")
    shop_recovery_name = models.CharField(max_length=40, null=False, default=" ",blank=True)
    firstName = models.CharField(max_length=40, null=False, default=" ",blank=True)
    lastName = models.CharField(max_length=40, null=False, default=" ", blank=True)
    picture = models.ImageField(upload_to=user_directory_path_physicians, null=True,blank=True)
    description =  models.TextField(null=True,blank=True)
    email = models.EmailField(default="",max_length=50,blank=True)
    services = models.CharField(max_length=100, null=True, blank=True)
    specialty_ph = models.ManyToManyField(to='pproducts.ProductTags', null=True, blank=True,related_name="physicians")
    productitems = models.ManyToManyField(to='pproducts.Product', null=True, blank=True)
    productitems_previous = MyJsonField(null=True,blank=True)
    about_me = models.TextField(max_length=512,default="",blank=True)
    products =  MyJsonField(null=True,blank=True,default=physicianDefaultProducts)
    is_onboarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    sd = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)
    user_delete = models.BooleanField(default=False)
    
    # previous_state_products = models.ManyToManyField(to='pproducts.Product', null=True, blank=True,related_name="previous_state_physician")
    def getHospitalName(self):
        if self.facility:
            return self.facility.name
        return "None"
    def returnCreatedAt(self):
        return self.created_at.strftime('%B %d, %Y %I:%M %p')
    
    def returnUpdatedAt(self):
        return self.updated_at.strftime('%B %d, %Y %I:%M %p')
    
    def get_full_name(self):
        return f"Dr. {self.firstName} {self.lastName}, MD"
    
    def buildSpecialtyString(self):

        return ", ".join(list(map(lambda x: x.tag, list(self.specialty_ph.all()))))
    
    def getStatus(self):
        return ''

    def returnPictureURL(self):
        if self.picture:
            return self.picture.url
        return "/media/generic_profile.jpeg"

    def buildLPT(self):
        try:
            if self.products:
                for specialty in self.products.keys():

                    self.removeDifferencefromDeletedTags()
                    products = self.products[specialty]

                    try:
                        tag = ProductTags.objects.get(tag=specialty)
                        print('does it get here')
                        lpt = LinkedProductTags.objects.get(parentTag=tag,physician=self,tag=specialty)
                        
                    except LinkedProductTags.DoesNotExist as error:
                        try:
                            print("creating the Linked Products Tags object")
                            lpt = LinkedProductTags.objects.create(parentTag=ProductTags.objects.get(tag=specialty),physician=self,tag=specialty)
                            # lpt.parentTag = ProductTags.objects.get(tag=specialty)
                            # lpt.physician = self
                            # lpt.save()
                        except Exception as error:
                            print(error)
                    except Exception as error:
                        print(error)
                    else:
                        for product in lpt.products.all():
                            if product.name not in products:
                                lpt.products.remove(product)
                                # At this point of you want to keep the saved data for records and book keeping puproses Do something else
                            
                    for product in products:
                        print(product)
                        print(len(Product.objects.filter(name=product)))
                        product = Product.objects.filter(name=product)[0]
                        lpt.products.add(product)
                        # Two ways to build physicians to onboarded. One is by onboarding a physician to an onboarded hospital. Second is the onboarded hospital onboards after the physician recommends.
                        # In this case products will not be added to product items so it is important
                        self.productitems.add(product)
                       

            self.save()
            lpt.save()
            self.save()
        except Exception as error:
            print("errrrrorrr",error)

    def removeDifferencefromDeletedTags(self):
        specialties = self.specialty_ph.all()
        new_specialties = self.linkedtags.exclude(parentTag__in=specialties)
        new_specialties.delete()
        self.save()

    def buildProductsSet(self,data={},created=False):
       
        try:
            print(data,'productSET')
            print(self.products,'self.products')
            if self.products:
                self.productitems_previous = self.products
            print('potemspre',self.productitems_previous)

            products = { key.split('-')[0]:data.getlist(key) for key in data.keys() if "-" in key}
            print('products',products)
            if len(products):
                self.productitems.clear()
                # check if this still works a
                # for key,value in products.items():
                #     prods = Product.objects.filter(name__in=value)
                #     self.productitems.add(*prods)
                self.products = products
                self.save()
                self.specialty_ph.clear()
                if created:
                    selections = ProductTags.objects.filter(id__in=data.getlist('specialty_ph'))
                else:
                    selections = ProductTags.objects.filter(id__in=data.getlist('selections'))
                self.specialty_ph.add(*selections)
                self.save()
        except Exception as error:
            print(error,"xxxxxx")
            return error
        
        self.buildLPT()
        print('self_products',self.products,)
        self.save()
        return created,products

    def checkState(self,new=False):
        # check for new physcian if yes, then the delta does not needd to be calculated
        if new:
            # convert to model_dict and convert model objects to easily identifiable strings in order to serialize in json form.
            physician_dict = model_to_dict(self)
            physician_dict['specialty_ph'] = [tag.tag for tag in physician_dict['specialty_ph'] ]
            physician_dict['productitems'] = [prod.name for prod in physician_dict['productitems'] ]
            physician_dict.pop('created_at')
            physician_dict['picture'] = physician_dict['picture'].url if physician_dict.get('picture','') else ''

            return physician_dict

        # Data Structure for changes state {'Products':'Removed': {'Specialties': [], 'Products': []}, 'Added':{'Specialties':[],'Products':[]}}}
        # s2 = {'Delta':False,'Products': {'Delta':False,'Removed': {'Delta':False,'Specialties': [], 'Products': []}, 'Added':{'Delta':False',Specialties':[],'Products':[]}},"Additional":{'Delta':False',}}
        Delta = False
        stateJSON = {'delta_specialties':'','delta_products':'','delta_profile':'','Removed': {'Specialties': [], 'Products': {}}, 'Added':{'Specialties':[],'Products':{}} }
        # stateJSON = {'AdditionalDelta':False,'Products': {'Delta':False,'Removed': {'Delta':False,'Specialties': [], 'Products': []}, 'Added':{'Delta':False,'Specialties':[],'Products':[]}}}
        if self.productitems_previous:
            previous_keys = set(self.productitems_previous.keys())
            current_keys = set(self.products.keys())
            removedTags = list(previous_keys.difference(current_keys))
            print('removedTags',removedTags)
            stateJSON['Removed']['Specialties'] = removedTags
            addedTags = list(current_keys.difference(previous_keys))
            print('addedTags',addedTags)
            stateJSON['Added']['Specialties'] = addedTags
            commonTags = previous_keys.intersection(current_keys)
            if removedTags or addedTags:
                Delta = True
                stateJSON['delta_specialties']  = 'Specialties'
            for tag in addedTags:
                stateJSON['Added']['Products'][tag] = self.products[tag]
            for tag in removedTags:
                stateJSON['Removed']['Products'][tag] = self.productitems_previous[tag]
            for tag in commonTags:
                removedProducts = list(set(self.productitems_previous[tag]).difference(self.products[tag]))
                check_removed = stateJSON['Removed']['Products'].get(tag,'')
                if check_removed:
                    stateJSON['Removed']['Products'][tag] = removedProducts
                addedProducts = list(set(self.products[tag]).difference(self.productitems_previous[tag]))
                check_added = stateJSON['Added']['Products'].get(tag,'')
                if check_added:
                    stateJSON['Added']['Products'][tag] = addedProducts
                if removedProducts or addedProducts:
                    stateJSON['delta_products'] = 'Products'
                    Delta = True     
        if Delta:
            stateJSON['entity_id'] = self.id
            stateJSON['entity_name'] = self.get_full_name()
            stateJSON['entity'] = 'Physician'
            return stateJSON
        return {}


    def sendToWooCommerce(self,updateOrCreate=''):
        if updateOrCreate:
            tags= []
            physician = ''
            wcapi = API(
                url=WOOCOMMERCE_API_URL_DEV,
                consumer_key=WOOCOMMERCE_CUSTOMER_KEY,
                consumer_secret=WOOCOMMERCE_CUSTOMER_SECRET,
                version="wc/v3",
                timeout = 10    
            )
            print('in the model function')
            if updateOrCreate == 'create':
                data = {
                    "name": self.shop_recovery_name if  self.shop_recovery_name else self.get_full_name,
                    "description": self.description,
                }
                wcapi.post("products/categories", data).json()
                

            elif updateOrCreate == 'update':
                data = {
                    "id": self.shop_recovery_id,
                    "name": self.shop_recovery_name if  self.shop_recovery_name else self.get_full_name,
                    "description": self.description,
                }
               
                physician = wcapi.put(f"products/categories/{self.shop_recovery_id}", data).json()
            if isinstance(physician,dict):
                self.shop_recovery_id = physician.get('id','')
            self.save()
            return physician
        else:
            return physician
        
    

    # Currently this function is not being Utilized but It will be in the future if more detailed logging is 
    # required which identifies the specific products which were added and removed upon every new update

    def deltaProducts(self, oldSetProducts = {'main':''} ):

        if not self.productitems_previous:
            oldSetProducts['main'] = set(self.productitems.all().values_list('id','name'))
            self.productitems_previous = oldSetProducts
        else:
            currentProducts = {'main':set(self.productitems.all().values_list('id','name')) }
            removedProducts = self.productitems_previous['main'].difference(currentProducts['main'])
            addedProducts = currentProducts['main'].difference(self.productitems_previous['main'])
            self.productitems_previous = currentProducts
        
    def save(self,flag=True,hospital=[],*args,**kwargs):
        
        if hospital:
            self.facility = hospital
        # if not self.productitems_previous:
        #     self.productitems_previous = list(self.productitems.all().values_list())
        # else:
        #     pass
        # self.deltaProducts()



        super().save(*args,**kwargs)
    
    # arguments addedProducts and removedProducts not yet utilized until more detailed logging is required.
    def update_history_record(self,action='',admin='',addedProducts='',removedProducts=''):
        history_record = self.history.latest()
        history_record.history_change_reason = f"{admin.username} {action}  {self.get_full_name} "
        history_record.save()
        self.save()

    def updateJSON(self,specialty,product,physicians):
        product = Product.objects.get(id=product)
    
    def logRecord(self,action='',action_verbose=''):
        uht = UserHistoryTable.objects.create(action=action,entity_type="Hospital",entity_id=self.id,entity_name=self.name,action_verbose=action_verbose,page_link=f"/register/edit/hospital/{self.id}/")
        uht.user = self.user
        uht.save()
        self.save()
        return uht


# first case is key exists for a none IMAGE type
    def convertObject(self,product):
        modelToDict = model_to_dict(product)
        if "picture" in modelToDict:
            modelToDict['picture'] = "N/A"
        if "created_at" in modelToDict:
            modelToDict['created_at'] = str(modelToDict['created_at']) if modelToDict.get("created_at",False) else None
        if "updated_at" in modelToDict:
            modelToDict['updated_at'] = str(modelToDict['updated_at']) if modelToDict.get("updated_at",False) else None
        print("function convert object", modelToDict)
        return modelToDict
        
    def updateProductsList(self,specialty,product):

        product_dict = self.convertObject(product=product)
      
        if "picture" in product_dict:
            product_dict['picture'] = "N/A"
        

        tag = self.specialty_ph.filter(tag=specialty)
        
        if tag and specialty in self.products:
            self.products[specialty].append(product_dict)
            self.linkedtags.filter(tag=specialty)[0].products.add(product)

        else:
            self.products[specialty] = [product_dict]
            newTag = ProductTags.objects.filter(tag=specialty)[0]
            self.specialty_ph.add(newTag)
            linkedTag = LinkedProductTags.objects.create(parentTag=newTag,physician=self,tag=specialty)
            linkedTag.products.add(product)
            linkedTag.save()
            self.linkedtags.add(linkedTag)

        self.productitems.add(product)
   
        self.save(flag=False)
    # def save_no_history(self, *args, **kwargs):
    #     self.skip_history_when_saving = True
    #     try:
    #         ret = self.save(*args, **kwargs)
    #     finally:
    #         del self.skip_history_when_saving
    #     return ret

    # Builds data structure to loop through products, specialties in Django Templates.
    # 
    def buildProductList(self):
        holding_cell = {}
        for outerindex,specialty in enumerate(self.linkedtags.all()):
            holding_cell[specialty.tag] = []
            for innerindex,product in enumerate(specialty.parentTag.products.all()):
                if product in self.linkedtags.all()[outerindex].products.all():
                    couple = (specialty,(product,"checked"))
                else:
                    couple = (specialty,(product,""))
                holding_cell[specialty.tag].append(couple)
        # Holding Cell Data Structure - Type- Dictionary Sample - {'Anterior Hip' [(linkedtag_object,(product_object,"checked" or ""))]}
        return holding_cell


    def resizeImage(self,height=100,width=100):
        img = Image.open(self.picture.path)
        if img.height > 100 or img.width > 100:
            new_img = (width, height)
            img.resize(new_img)
            img.save(self.picture.path)
        self.save()
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    class Meta:
        ordering = ['firstName']

# class JsonProducts(models.Model):
#     physician = models.OneToOneField(Physician,on_delete=models.CASCADE, null=True,related_name='jsonproducts')
#     products = MyJsonField(null=True)
#     bytes = models.BinaryField(null=True)


    

class ProductTags(models.Model):
    shop_recovery_id = models.PositiveIntegerField(verbose_name="Shop Recovery Id",null=True, blank=True)
    tag = models.CharField(max_length=50, null=False, default="", unique=True)
    shop_recovery_name = models.CharField(max_length=50, null=False, default="",blank=True)
    description = models.TextField(max_length=512, null=True, default="",blank=True)
    products = models.ManyToManyField(Product, related_name='specialties', null=True, default="none",blank=True)
    related_specialty = models.ManyToManyField(Specialty,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
   
    
    class Meta:
        ordering = ['tag']

    def __str__(self):
        return f"{self.tag.upper()}"
    def __repr__(self):
        return f"{self.tag.upper()}"
    
    def returnProductsString(self):
        return ", ".join([product.name for product in self.products.all().order_by('name')])
    
    def getTag(self):
        
        if self.tag.find(" ") != -1:
            return "_".join(self.tag.split(" "))
        else:
            return self.tag
    def tagToDB(self):
        if self.tag.find("_") != -1:
            return " ".join(self.tag.split("_"))


    # def save_no_history(self, *args, **kwargs):
    #     self.skip_history_when_saving = True
    #     try:
    #         ret = self.save(*args, **kwargs)
    #     finally:
    #         del self.skip_history_when_saving
    #     return ret
    
    def sendToWooCommerce(self,updateOrCreate=''):
        if updateOrCreate:
            
            wcapi = API(
                url=WOOCOMMERCE_API_URL_DEV,
                consumer_key=WOOCOMMERCE_CUSTOMER_KEY,
                consumer_secret=WOOCOMMERCE_CUSTOMER_SECRET,
                version="wc/v3",
                timeout = 10    
            )

            if updateOrCreate == 'update':
                data=    {
                    
                "id": self.shop_recovery_id,
                "name":self.shop_recovery_name if self.shop_recovery_name else self.tag ,
                "description": self.description,
                                }
                tag = wcapi.put(f"products/tags/{self.shop_recovery_id}", data).json()

            elif updateOrCreate == 'create':
                data=    {
                "name":self.shop_recovery_name if self.shop_recovery_name else self.tag ,
                "description": self.description,
                                }
                tag = wcapi.post("products/tags", data).json()
            self.shop_recovery_id = tag['id']
            self.save()
            return tag
                
                
            
    def logHistory(self,user,created=False):
        time = dateformat.format(timezone.now(), 'Y-m-d')
        if not created:
            record = self.history.latest()
            record.history_change_reason = f"{user} Updated tag {self.tag} {time} at"
        else:
            record = self.history.latest()
            record.history_change_reason = f"{user} Created Tag {self.tag} {time} at"
        record.save()
        self.save()
# class ProductTags1(models.Model):
#     shop_recovery_id = models.PositiveIntegerField(verbose_name="Shop Recovery Id",null=True, blank=True)
#     tag = models.CharField(max_length=50, null=False, default="", unique=True)
#     shop_recovery_name = models.CharField(max_length=50, null=False, default="",blank=True)
#     description = models.TextField(max_length=512, null=True, default="",blank=True)
#     products = models.ManyToManyField(Product, related_name='specialties', null=True, default="none",blank=True, s)
#     related_specialty = models.ManyToManyField(Specialty,null=True,blank=True)
#     created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
#     history = HistoricalRecords()
    
#     class Meta:
#         ordering = ['tag']

#     def __str__(self):
#         return f"{self.tag.upper()}"
#     def __repr__(self):
#         return f"{self.tag.upper()}"
    
#     def returnProductsString(self):
#         return ", ".join([product.name for product in self.products.all().order_by('name')])

#     def save_no_history(self, *args, **kwargs):
#         self.skip_history_when_saving = True
#         try:
#             ret = self.save(*args, **kwargs)
#         finally:
#             del self.skip_history_when_saving
#         return ret
    
#     def sendToWooCommerce(self,updateOrCreate=''):
#         if updateOrCreate:
            
#             wcapi = API(
#                 url=WOOCOMMERCE_API_URL_DEV,
#                 consumer_key=WOOCOMMERCE_CUSTOMER_KEY,
#                 consumer_secret=WOOCOMMERCE_CUSTOMER_SECRET,
#                 version="wc/v3",
#                 timeout = 10    
#             )

#             if updateOrCreate == 'update':
#                 data=    {
                    
#                 "id": self.shop_recovery_id,
#                 "name":self.shop_recovery_name if self.shop_recovery_name else self.tag ,
#                 "description": self.description,
#                                 }
#                 tag = wcapi.put(f"products/tags/{self.shop_recovery_id}", data).json()

#             elif updateOrCreate == 'create':
#                 data=    {
#                 "name":self.shop_recovery_name if self.shop_recovery_name else self.tag ,
#                 "description": self.description,
#                                 }
#                 tag = wcapi.post("products/tags", data).json()
#             self.shop_recovery_id = tag['id']
#             self.save()
#             return tag
                
                
            
#     def logHistory(self,user,created=False):
#         time = dateformat.format(timezone.now(), 'Y-m-d')
#         if not created:
#             record = self.history.latest()
#             record.history_change_reason = f"{user} Updated tag {self.tag} {time} at"
#         else:
#             record = self.history.latest()
#             record.history_change_reason = f"{user} Created Tag {self.tag} {time} at"
#         record.save()
#         self.save_no_history()

# class LinkedProductTags(models.Model):
#     parentTag = models.ForeignKey(ProductTags, on_delete=models.CASCADE,null=True, related_name='parenttags')
#     physician = models.ForeignKey(Physician,null=True,on_delete=models.CASCADE,related_name='linkedtags')
#     products = models.ManyToManyField(Product,null=True)
#     tag = models.CharField(max_length=50, null=False, default="", unique=False, blank=False)
#     description = models.TextField(max_length=1000,null=True,default="")
#     created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    

#     class Meta:
#         ordering = ['tag']

"""
1. First Create A User
2. Link

"""

# class BodyParts(models.Model):
#     bodypart = models.CharField(max_length=100,null=False,default="")
#     specialty = models.ManyToManyField(Specialty)

# class ImageTest(models.Model):
#     picture = models.ImageField(upload_to='products/testing/',null=True)


# def buildProducts(request):

#     specialty = request.POST.getlist('lookup','')[0].strip().title()
#     print('spppecialty',specialty)
#     specialty_products= ProductTags.objects.filter(tag=specialty)[0].products.all().order_by('name')
#     products = list(specialty_products.values_list('name','picture','short_description','id'))
#     for i in range(len(specialty_products)):
#         products[i] = list(products[i])
#         products[i][1] = specialty_products[i].getFirstImage()
#     print(products)
#     return JsonResponse(data={'dataset':products,'specialty':specialty})
