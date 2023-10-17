# import os
# import numpy as np
# import hashlib
# import imagehash
# from PIL import Image

# def alpharemover(image):
#     if image.mode != 'RGBA':
#         return image
#     canvas = Image.new('RGBA', image.size, (255,255,255,255))
#     canvas.paste(image, mask=image)
#     return canvas.convert('RGB')

# def with_ztransform_preprocess(hashfunc, hash_size=8):
#     def function(path):
#         image = alpharemover(Image.open(path))
#         image = image.convert("L").resize((hash_size, hash_size), Image.LANCZOS)
#         data = image.getdata()
#         quantiles = np.arange(100)
#         quantiles_values = np.percentile(data, quantiles)
#         zdata = (np.interp(data, quantiles_values, quantiles) / 100 * 255).astype(np.uint8)
#         image.putdata(zdata)
#         return hashfunc(image)
#     return function
  
# dhash_z_transformed = with_ztransform_preprocess(imagehash.dhash, hash_size = 8)

# hashes = set()
# for filename in os.listdir('feedback'):
#     path = os.path.join('feedback', filename)
#     digest = dhash_z_transformed(path)
#     if digest not in hashes:
#         hashes.add(digest)
#     else:
#         os.remove(path)
#         print("found and removed duplicate")
# print("duplicates removed");


#---------------------

import os
from PIL import Image
import imagehash
from collections import defaultdict

# Function to calculate the perceptual hash for an image file
def calculate_phash(file_path):
    img = Image.open(file_path)
    phash = imagehash.phash(img)
    return phash

# Specify the folder path containing the images
folder_path = 'feedback'

# Create a dictionary to store image hashes and their paths
image_hashes = defaultdict(list)

# List all image files in the folder
image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Identify and store perceptual hashes for images
for file in image_files:
    file_path = os.path.join(folder_path, file)
    phash = calculate_phash(file_path)
    image_hashes[phash].append(file_path)

# Identify and remove similar images
for hash_value, file_paths in image_hashes.items():
    if len(file_paths) > 1:
        print(f'Similar images with hash {hash_value}:')
        for file_path in file_paths[1:]:
            print(f'Removing {file_path}')
            os.remove(file_path)

print('Similar image removal process completed.')
