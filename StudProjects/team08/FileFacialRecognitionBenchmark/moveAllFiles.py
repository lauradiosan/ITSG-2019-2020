import shutil
import os
import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
path = currentPath + '/originalPics/'
dest1 = currentPath + '/needToBeRenamed'

filesPaths = []
files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.jpg' in file:
			files.append(file)
			filesPaths.append(os.path.join(r, file))

for f in filesPaths:
    shutil.copy(f, dest1)
	
# for f in folders:
	# for _, _, f2 in os.walk(path):
		# for file in f2:
			# print(f + "/" +file)
			# filename = path + '/' + file
			# shutil.move(path + file, dest1)

# for _, _, f in os.walk(path):
    # for file in f:
		# print(f)
		# print(file)
		# filename = path + '/' + file
		# shutil.move(path + file, dest1)