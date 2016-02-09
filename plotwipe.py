import os
folder = os.path.join('utakeout','static','img','plot')
delete_count = 0
for file in os.listdir(folder):
	file_path = os.path.join(folder,file)
	if os.path.isfile(file_path):
		os.remove(file_path)
		print '{} was deleted.'.format(file_path)
		delete_count += 1

print '{} total files were deleted.'.format(delete_count) 

