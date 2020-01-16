import os
import shutil
import glob

import os

for subdir, dirs, files in os.walk("datasetkids"):
    print()

    if(files[0][0] == '.'):
        continue
    test = True
    once = True
    # if len(files)<5:
    #     shutil.rmtree(subdir)

    for file in files:
        if test:
            os.mkdir(os.path.abspath(subdir)+"/test/")
            shutil.move(os.path.abspath(subdir)+"/"+file,os.path.abspath(subdir)+"/test/")
            test = False
        else:
            if once:
                os.mkdir(os.path.abspath(subdir) + "/train/")
                once = False
            shutil.move(os.path.abspath(subdir) + "/"+ file, os.path.abspath(subdir) + "/train/")
test = False
# for file in files:
#     if file[0]!='.':
#         if test:
#             shutil.move(dirs+file,str(path)+"/test/"+file)
#             test = True
#         else:
#             shutil.move(str(path) + file, str(path) + "/train/" + file)