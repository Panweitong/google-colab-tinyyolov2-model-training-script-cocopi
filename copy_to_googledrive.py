from shutil import copyfile

import os

project_name = input("Please enter the name of your project inside Google Drive: \n")

google_drive_path = "/content/gdrive/My Drive/"

with open("/content/toolkit/out/" + project_name + "/ImageSets/Main/val.txt") as export_pid:
    imgName = export_pid.readlines()[0].strip()

if not os.path.exists("/content/toolkit/out/" + project_name + "/images"):
    os.mkdir("/content/toolkit/out/" + project_name + "/images")
    for item in os.listdir("/content/toolkit/data/custom/" + project_name + "/JPEGImages"):
        if item == imgName + ".jpg":
            os.system("cp /content/toolkit/data/custom/" + project_name + + "/JPEGImages/" + imgName + ".jpg  /content/toolkit/out/" + project_name + "/images")

try:
	copyfile("/content/toolkit/out/"+ project_name +".kmodel", google_drive_path + project_name +".kmodel")
except IOError as e:
	print("Something went wrong:\n")
	print(str(e))
finally:
	print("Done copying the model file to your Google Drive! No go check it!")