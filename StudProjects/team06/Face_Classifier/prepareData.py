import os
import shutil
import glob

import os

for subdir, dirs, files in os.walk("dataset/lfw_home/lfw_funneled"):
    print()
    if(len(files)==0):
        continue
    if(files[0][0] == '.'):
        continue
    test = True
    once = True
    if subdir.split(os.sep)[-1] == "train":
        if len(files)<5:
            print(subdir)
            shutil.rmtree(os.path.abspath("dataset/lfw_home/lfw_funneled/"+subdir.split(os.sep)[-2]))

test = False
# for file in files:
#     if file[0]!='.':
#         if test:
#             shutil.move(dirs+file,str(path)+"/test/"+file)
#             test = True
#         else:
#             shutil.move(str(path) + file, str(path) + "/train/" + file)