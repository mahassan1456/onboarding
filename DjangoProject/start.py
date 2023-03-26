
# script to Download Products and save to Database from URL's in excel file

#!/usr/bin/env python

import django
django.setup()
import os
import pandas as pd
import requests
from pproducts.models import Product,ProductImages
df = pd.read_excel('/Users/nefarioussmalls/Documents/Da Portfolio/product_images.xlsx')
df = df.dropna()
folder_name = 'product_dev_img1/'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
x=0
for index,row in df.iterrows():
    try:
        product = Product.objects.get(name=row['Name'].strip())
    except Exception as error:
        print(error)
        continue
    else:
        
        product_folder = f"{row['Name'].lower().replace('/','').replace(' ','_')}"
        inner_folder_path = os.path.join(folder_name,f"{product_folder}/")
        if not os.path.exists(inner_folder_path):
            os.makedirs(inner_folder_path)
        product.images.clear()
        for index, url in enumerate(row['Images'].split(',')):
            try:
                response = requests.get(url)
            except Exception as error:
                print(error)
                print('error',inner_folder_path)
                continue
            else:
                image_path = os.path.join(inner_folder_path, f"{product_folder}-{index}.jpg")
                if not os.path.exists(image_path):
                    print(image_path)
                    with open(image_path,'wb') as f:
                        f.write(response.content)
                    print(f'Downloaded {url} to {image_path}')
            
                image_obj = ProductImages.objects.create(image=f"/media/{image_path}")
                print(f"Product Image Id----{image_obj.id}---")
                product.images.add(image_obj)
                x+=1
                product.save()
                image_obj.save()
                print(f"Added {image_path} to {image_obj}")
print()
print(f'--------------------------------{x}--------------------------------------------')
    
                

    # response = requests.get(row['Images'])
    # print(response)
    # break

# for i, url in enumerate(image_urls):
#     response = requests.get(url)
#     image_path = os.path.join(folder_name, f'image_{i}.jpg')
#     with open(image_path, 'wb') as f:
#         f.write(response.content)
#     print(f'Downloaded {url} to {image_path}')




# # List of image URLs
# image_urls = ['https://example.com/image1.jpg', 'https://example.com/image2.jpg', 'https://example.com/image3.jpg']
#
# # Create a folder to save the downloaded images
# folder_name = 'images'
# if not os.path.exists(folder_name):
#     os.makedirs(folder_name)





#
# # Loop through the list of URLs and download the images
# for i, url in enumerate(image_urls):
#     response = requests.get(url)
#     image_path = os.path.join(folder_name, f'image_{i}.jpg')
#     with open(image_path, 'wb') as f:
#         f.write(response.content)
#     print(f'Downloaded {url} to {image_path}')