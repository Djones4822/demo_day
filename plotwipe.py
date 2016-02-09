import os
folder = os.path.join('utakeout','static','img','plot')
for file in os.listdir(folder):
	file_path = os.path.join(folder,file)
	if os.path.isfile(file_path):
		os.remove(file_path)