# Pythono3 code to rename multiple 
# files in a directory or folder 

# importing os module 
import os 

currentPath = os.path.dirname(os.path.abspath(__file__))
filesPath = currentPath + '/needToBeRenamed/'

# Function to rename multiple files 
def main(): 
	i = 1
	
	for filename in os.listdir(filesPath): 
		dst ="User." + str(i) + "." + str(i) + ".jpg"
		src =filesPath + filename 
		dst =filesPath + dst 
		
		# rename() function will 
		# rename all the files 
		os.rename(src, dst)
		
		i += 1

# Driver Code 
if __name__ == '__main__': 
	
	# Calling main() function 
	main() 
