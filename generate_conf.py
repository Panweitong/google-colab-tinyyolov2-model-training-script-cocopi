import os

conf_directory_name = "conf"
google_drive_path = "/content/toolkit/data/custom/"

google_drive_project_path = input(
    "Please enter the name of your project inside Google Drive: \n")
project_name = google_drive_project_path
current_directory_path = os.getcwd()

max_batches = input("Please enter the max batches you would like to train: \n")


def generate_cfg():
    f = open("/content/toolkit/" + conf_directory_name +
             "/" + project_name + "/" + project_name + ".cfg", "w")
    cfg_content = ["max_batches = " + str(max_batches) + "\n"]
    # ["[net]\n", "Training\n", "batch=64\n", "subdivisions=16\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches=" + str(int(float(classes_count))*2000) +"\n", "policy=steps\n", "steps=" + str(int(float(classes_count))*0.8) + "," + str(int(float(classes_count))*0.9) + "\n", "scales=.1,.1\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "filters=" + str((int(float(classes_count)) + 5) * 5) + "\n", "activation=linear\n\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes=" + str(int(float(classes_count))) + "\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n\n", "absolute=1\n", "thresh = .6\n", "random=1"]
    f.writelines(cfg_content)
    f.close()


def generate_training_bash():
    image_count_sum = 0
    for each in os.listdir(google_drive_path + project_name + "/JPEGImages"):
        if ".jpg" in each:
            image_count_sum += 1

    TRAIN_CLI = "python " + current_directory_path + "/train.py"
    TRAIN_PARAMETER = "-d custom --cuda -v slim_yolo_v2 -hr -ms --num_workers 3"
    TRAIN_PROJECT_DATA = "--dataset_folder " + google_drive_path + project_name
    TRAIN_PROJECT_CFG = "--max_epoch " + str(max_batches)
    TRAIN_MODEL_PATH = "--save_folder " + \
        current_directory_path + "/weights/custom/" + project_name
    EVAL_EPOCH = "--eval_epoch " + str(int(max_batches) + 10)
    BATCH_SIZE = "--batch_size " + \
        str(1 if int(image_count_sum / 100) ==
            0 else int(image_count_sum / 100))
    # EVAL_EPOCH = "--eval_epoch 10"
    CMD_SEP = " "

    TRAINING_FULL_COMMAND = TRAIN_CLI + CMD_SEP + TRAIN_PARAMETER + CMD_SEP + TRAIN_PROJECT_DATA + \
        CMD_SEP + TRAIN_PROJECT_CFG + CMD_SEP + TRAIN_MODEL_PATH + \
        CMD_SEP + EVAL_EPOCH + CMD_SEP + BATCH_SIZE

    f = open("/content/toolkit/" + conf_directory_name + "/" + project_name + "/start-train.sh", "w")
    train_check_content = [
        "nohup " + TRAINING_FULL_COMMAND + " > " + current_directory_path + "/" +
        conf_directory_name + "/" + project_name + "/" + "nohup.log 2>&1 &\n",
        # "OUTPUT_PID=$!\n",
        # "echo ${OUTPUT_PID} > " + current_directory_path + "/" +
        # conf_directory_name + "/" + project_name + "/save_pid.txt\n",
        # "\n",
        # "echo '${OUTPUT_PID}'\n",
        #"cpulimit -l 40 -p ${OUTPUT_PID} > /dev/null &\n",
    ]

    f.writelines(train_check_content)
    f.close()


def generate_testing_bash():
    TRAIN_CLI = "python " + current_directory_path + "/test.py"
    TRAIN_PARAMETER = "-d custom -v slim_yolo_v2"
    TRAIN_PROJECT_DATA = "--dataset_folder " + google_drive_path + project_name
    TRAINED_MODEL = "--trained_model " + current_directory_path + \
        "/weights/custom/" + project_name + "/slim_yolo_v2_last.pth"
    OTHER = "--visual_threshold 0.3 -size 224 --test --test_result_folder " + \
        current_directory_path + "/out/" + project_name
    CMD_SEP = " "

    TRAINING_FULL_COMMAND = TRAIN_CLI + CMD_SEP + TRAIN_PARAMETER + CMD_SEP + \
        TRAIN_PROJECT_DATA + CMD_SEP + TRAINED_MODEL + CMD_SEP + OTHER

    f = open(current_directory_path + "/" + conf_directory_name + "/" + project_name + "/test-train.sh", "w")
    bash_content = [
        # "cd "+CURRENT_DIR+"/tools\n",
        # "FILE='./"+name+"_test_result.log'\n",
        # "STRING='milli-seconds'\n",
        "nohup " + TRAINING_FULL_COMMAND + " > " + current_directory_path + \
        "/conf/" + project_name + "/" + project_name + "_test_result.log 2>&1 &\n",
        "TEST_PID=$!\n",
        # "cpulimit -l 20 -p ${TEST_PID} > /dev/null &\n",
        "echo ${TEST_PID} > " + current_directory_path + \
        "/conf/" + project_name + "/save_test_pid.txt\n",
        # "while true\n",
        # "do\n",
        # "    sleep 1\n",
        # "    if  grep -q $STRING $FILE ; then\n",
        # "        echo 'Done testing' ;\n",
        # "        kill -9 $TEST_PID\n",
        # "        sleep 2\n",
        # "        break\n",
        # "    fi\n",
        # "done\n",
        "sleep 8\n",
        # "cp "+name+"_test_result.log "+CURRENT_DIR+ "/toolkit/conf/" + name + "/\n",
        # "cp predictions.jpg "+CURRENT_DIR+ "/toolkit/conf/" + name + "/"+name+"predictions.jpg\n",
        # "cd "+CURRENT_DIR+"\n"
    ]
    f.writelines(bash_content)
    f.close()

def generate_subprocess_check_py():
	f = open(current_directory_path + "/" + conf_directory_name + "/" + project_name + "/train.py", "w")
	train_check_content = [
		"import subprocess, shlex, os, signal\n",
		"\n",
		"def run_command(command):\n",
		"	process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)\n",
		"	print(\"Process PID is: \" + str(process.pid))\n",
		"	while True:\n",
		"		output = process.stdout.readline()\n",
		"		if output == '' and process.poll() is not None:\n",
		"			break\n",
		"		if output:\n",
		"			formatted_output = output.strip().decode(\"utf-8\")\n",
		"			if (\"avg loss\" in formatted_output) and (\"rate\" in formatted_output):\n",
		"				print(formatted_output)\n",
		"				iteration_times = int(formatted_output.split()[0][:-1])\n",
		"				avg_loss = float(formatted_output.split()[2])\n",
		"				# print(str(int(iteration_times)) + \",\" + str(float(formatted_output.split()[2])))\n",
		"				if avg_loss < 2.00: break\n",
		"	# process.terminate()\n",
		"	process.terminate()\n",
		"	try:\n",
		"		process.wait(timeout=0.2)\n",
		"		print('== subprocess exited with rc =', process.returncode)\n",
		"	except subprocess.TimeoutExpired:\n",
		"		print('subprocess did not terminate in time')\n",
		"	os.kill(int(process.pid)+1, signal.SIGKILL)\n",
		"\n",
		"try:\n",
		"	run_command(\"bash start-train.sh\")\n",
		"except KeyboardInterrupt:\n",
		"	print(\"Keyboard Interrupted.\")\n",
		"\n",
		"print(\"\"\"\n",
		"  ____                   _ \n",
		" |  _ \\  ___  _ __   ___| |\n",
		" | | | |/ _ \\| '_ \\ / _ \\ |\n",
		" | |_| | (_) | | | |  __/_|\n",
		" |____/ \\___/|_| |_|\\___(_)\n",
		"	\"\"\")\n"
	]
	f.writelines(train_check_content)
	f.close()


if __name__ == '__main__':
	# shenzhen_trash_classification_sign_dataset
	generate_cfg()
	generate_training_bash()
	generate_testing_bash()
	generate_subprocess_check_py()