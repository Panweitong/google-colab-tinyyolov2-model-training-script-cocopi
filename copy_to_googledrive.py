from shutil import copyfile
import shutil
import os

project_name = input(
    "Please enter the name of your project inside Google Drive: \n")

google_drive_path = "/content/gdrive/My Drive/"

# if not os.path.exists(google_drive_path + project_name):
#     os.mkdir(google_drive_path + project_name)

# if not os.path.exists(google_drive_path + project_name + "/images"):
#     os.mkdir(google_drive_path + project_name + "/images")

with open("/content/toolkit/data/custom/" + project_name + "/ImageSets/Main/val.txt") as export_pid:
    imgName = export_pid.readlines()[0].strip()

if not os.path.exists("/content/toolkit/out/" + project_name + "/images"):
    os.mkdir("/content/toolkit/out/" + project_name + "/images")
    for item in os.listdir("/content/toolkit/data/custom/" + project_name + "/JPEGImages"):
        if item == imgName + ".jpg":
            os.system("cp /content/toolkit/data/custom/" + project_name + "/JPEGImages/" +
                      imgName + ".jpg  /content/toolkit/out/" + project_name + "/images")

if not os.path.exists("/content/toolkit/out/" + project_name + "/" + project_name):
  os.mkdir("/content/toolkit/out/" + project_name + "/" + project_name)

if not os.path.exists("/content/toolkit/out/" + project_name + "/" + project_name+ "/images"):
  os.mkdir("/content/toolkit/out/" + project_name + "/" + project_name+ "/images")

try:
	copyfile("/content/toolkit/out/" + project_name + "/model/yolov2_among.bin","/content/toolkit/out/" + project_name + "/" + project_name + "/" + project_name + ".bin")
	copyfile("/content/toolkit/out/" + project_name + "/model/yolov2_among.param","/content/toolkit/out/" + project_name + "/" + project_name + "/" + project_name + ".param")
	copyfile("/content/toolkit/out/" + project_name + "/images/" + imgName + ".jpg","/content/toolkit/out/" + project_name + "/" + project_name + "/images/" + imgName + ".jpg")
except IOError as e:
	print("Something went wrong:\n")
	print(str(e))

try:
    target_dir = "/content/toolkit/out/"+ project_name + "/"
    target_dir = "/content/toolkit/out/"+ project_name + "/"
    target = target_dir + project_name
    source = "/content/toolkit/out/"+ project_name + "/" + project_name
    new_path = shutil.make_archive(target,'zip',source)
    if new_path:
        copyfile("/content/toolkit/out/"+ project_name + "/" + project_name + ".zip", google_drive_path + project_name + ".zip")
except IOError as e:
	print("Something went wrong:\n")
	print(str(e))
finally:
	print("Done copying the model file to your Google Drive! No go check it!")