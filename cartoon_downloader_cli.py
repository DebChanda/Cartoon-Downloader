#! /usr/bin/env python3

import requests, os, time, sys
from pySmartDL import SmartDL
from progress import bar as Bars

sys.path.insert(0, os.path.join(os.path.dirname(__file__),"sites"))

class tc:
    VIOLET = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALICS = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERT = '\033[7m'
    STRIKE = '\033[9m'

    EVIOLET = '\033[0m\033[95m'
    EBLUE = '\033[0m\033[94m'
    EGREEN = '\033[0m\033[92m'
    EYELLOW = '\033[0m\033[93m'
    ERED = '\033[0m\033[91m'

    EBOLD = '\033[0m\033[1m'
    EDIM = '\033[0m\033[2m'
    EITALICS = '\033[0m\033[3m'
    EUNDERLINE = '\033[0m\033[4m'
    EBLINK = '\033[0m\033[5m'
    EINVERT = '\033[0m\033[7m'
    ESTRIKE = '\033[0m\033[9m'


def site_determiner(url):
	url_dummy = url.split(".")[1]
	print(tc.ENDC + "\nLink of", tc.EBOLD + tc.YELLOW, url_dummy, tc.ENDC + "was given.\n") 

	return url_dummy

def url_validity(url):
	print(tc.EYELLOW + "\nChecking URL..." + tc.ENDC)
	r = requests.get(url)
	if r.status_code == 404:
		return False
	else:
		return True


def masterfunc(something, site, type):

	if site == "watchcartoononline":
		import watchcartoononline as sitename

	elif site == "gogoanime":
		import gogoanime as sitename

	elif site == "kiss-anime":
		import kiss_anime as sitename

	else:
		print("Unknown Site !")


	if type == "list":
		return sitename.list_finder(something)

	elif type == "video":
		return sitename.video_finder(something)

	else:
		print("Wrong Type !")



def download_video(video_save_name, no, total):

	with open(os.path.join(main_path, "video",video_save_name), "r") as f:

		video_data = f.read().split(",")
		video_name = video_data[0]
		video_url = video_data[1]

	print("[" + str(no) + "/" + str(total) + "] Staring download...")
	video_save_name = video_save_name + ".mp4"
	save_path = os.path.join(main_path, "download",video_save_name)
	
	obj = SmartDL(video_url, save_path, progress_bar=False)
	obj.start(blocking=False)

	bar = Bars.FillingSquaresBar("[" + str(no) + "/" + str(total) + "] Downloading " + str(no) + "/" + str(total), max = 100, suffix = "0.00%% " + obj.get_speed(human = True) + " " + str(obj.get_dl_size(human = True)))
	p = 0.0
	while not obj.isFinished():

		bar.next(obj.get_progress()*100 - p )

		p = obj.get_progress()*100
		bar.suffix = "%.2f" %p + "%% " + obj.get_speed(human = True) + " " + str(obj.get_dl_size(human = True))
		time.sleep(0.5)
	bar.suffix = "100.00%% " + obj.get_speed(human = True) + " " + str(obj.get_dl_size(human = True))
	bar.next(100)
	bar.finish()
       

def download_numbers(go=1):
	list1 = []
	list2 = []
	list3 = []

	if go != 1:
		print("Some error occured, please input again carefully !")


	download_no = input("Enter no. of videos to be downloaded (e.g., 1 2 3 or/and 1-3)\n==> ")
	list1 = download_no.split(" ")
	for item in list1:
		try:
			x_int = int(item)
			if x_int > 0:
				list2.append(x_int-1)
			else:
				print("Negative number ",x_int," not included!")
		
		except:

			try:
				list3 = item.split("-")
				for i in range(int(list3[0]),int(list3[1])+1):
					list2.append(i-1)

			except ValueError as e:
				print(e)
				list2 = download_numbers(2)

	list2 = list(set(list2))
	return list2


os.system("clear")
main_path = os.path.dirname(__file__)
folder_to_create = ["video","download"]
program_name = "Cartoon Downloader CLI 3.2"

print(tc.YELLOW + "Welcome to " + tc.VIOLET + tc.BOLD + program_name + tc.ENDC)
k = input("\nPress" + tc.BLINK + tc.BOLD + tc.YELLOW + " ENTER" + tc.ENDC + " to continue!\n")

for folder in folder_to_create:

    if not os.path.exists(os.path.join(main_path, folder)):
        os.makedirs(os.path.join(main_path, folder))
        print(tc.EGREEN + "Folder " + tc.BOLD +  folder + tc.EGREEN + " created!" + tc.ENDC)
    else:
    	print(tc.EYELLOW + "Folder " + tc.BOLD +  folder + tc.EYELLOW + " found!" + tc.ENDC)

loop = True
while loop:

	mode = str(input(tc.BOLD + "\nDo you want to download from a playlist? " + tc.ERED +"(yes/no) " + tc.EBLUE))

	if ( mode == 'y' or mode == 'yes' or mode == 'Y' or mode == 'Yes' or mode == 'YES'):
		loop = False
		print(tc.EGREEN + "\nYou choose to download from a" + tc.BOLD + " playlist" + tc.EGREEN + "!\n" + tc.ENDC)
		playlist_url = str(input(tc.BOLD + "Paste the URL of the playlist :  " + tc.ENDC))

		if url_validity(playlist_url):
			print(tc.EGREEN + tc.BOLD + "URL valid!")
		else:
			print(tc.ERED + tc.BOLD + "URL not valid!")
			quit()
			
		site = site_determiner(playlist_url)

		url_list = masterfunc(playlist_url, site, "list")

		loop = True 
		while loop:
			
			check = input("Do you want to download all " + str(len(url_list)) + " videos ? (yes/no) ")
			if ( check == 'y' or check == 'yes' or check == 'Y' or check == 'Yes' or check == 'YES'):

				list_dl = []
				video_save_name = []

				for i in range(len(url_list)):
					list_dl.append(i)

				video_save_name_list = masterfunc(url_list, site, "video")

				for no in list_dl:
					download_video(video_save_name_list[no], no+1, len(url_list))

				loop = False

			elif ( check == 'N' or check == 'no' or check == 'n' or check == 'No' or check == 'NO'):

				list_dl = download_numbers()
				url_list_2 = []

				for no in list_dl:
					url_list_2.append(url_list[no])

				video_save_name_list =  masterfunc(url_list_2,site,"video")


				for no in range(len(list_dl)):
					download_video(video_save_name_list[no], no+1, len(list_dl))
					

				loop = False
				
			else:
				print(tc.ERED + tc.BOLD + "\nWrong Choice!" + tc.ENDC)


	elif ( mode == 'N' or mode == 'no' or mode == 'n' or mode == 'No' or mode == 'NO'):
		loop = False
		print(tc.EGREEN + "\nYou choose to download a" + tc.BOLD + " single episode" + tc.EGREEN + "!\n" + tc.ENDC)
		url = str(input(tc.BOLD + "Paste the URL of the video :  " + tc.ENDC))

		if url_validity(url):
			print(tc.EGREEN + tc.BOLD + "URL valid!")
		else:
			print(tc.ERED + tc.BOLD + "URL not valid!")
			quit()

		site = site_determiner(url)
		url_list = []
		url_list.append(url)
		video_save_name_list =  masterfunc(url_list, site, "video")
		download_video(video_save_name_list[0], 1, 1)

	else:
			print(tc.ERED + tc.BOLD + "\nWrong Choice!" + tc.ENDC)
