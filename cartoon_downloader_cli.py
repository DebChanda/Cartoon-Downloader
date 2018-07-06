#! /usr/bin/env python3

import requests, os, time, sys
from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from pySmartDL import SmartDL
from progress import bar as Bars


site_data = {}
site_data["watchcartoononline"] = ["h1","iframe",2,"source","src","sonra"]
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"sites"))

def site_determiner(url):
	url_dummy = url.split(".")[1]
	print("Link of", url_dummy, "found! ") 

	return url_dummy

def onefunc(url_list, site):

	if site == "watchcartoononline":
		import watchcartoononline as sitename


	return sitename.video_finder(url_list)

def twofunc(playlist_url, site):

	if site == "watchcartoononline":
		import watchcartoononline as sitename
	elif site == "gogoanime":
		import gogoanime as sitename
	else:
		print("Unknown Site !")

	url_list = sitename.list_finder(playlist_url)
	return url_list


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
program_name = "Cartoon Downloader CLI 3.0"

print("Welcome to " + program_name)
k = input("Press ENTER to continue !")

for folder in folder_to_create:

    if not os.path.exists(os.path.join(main_path, folder)):
        os.makedirs(os.path.join(main_path, folder))
        print("Folder " + folder + " created!")
    else:
    	print("Folder " + folder + " found!")

loop = True
while loop:

	mode = str(input("Do you want to download from a playlist? (yes/no) "))

	if ( mode == 'y' or mode == 'yes' or mode == 'Y' or mode == 'Yes' or mode == 'YES'):
		loop = False
		print("You choose to download from a playlist!\n")
		playlist_url = str(input("Paste the url of the playlist :  "))
		site = site_determiner(playlist_url)

		url_list = twofunc(playlist_url,site)

		loop = True 
		while loop:
			
			check = input("Do you want to download all " + str(len(url_list)) + " videos ? (yes/no) ")
			if ( check == 'y' or check == 'yes' or check == 'Y' or check == 'Yes' or check == 'YES'):

				list_dl = []
				video_save_name = []

				for i in range(len(url_list)):
					list_dl.append(i)

				video_save_name_list = onefunc(url_list,site)

				for no in list_dl:
					download_video(video_save_name_list[no], no+1, len(url_list))

				loop = False

			elif ( check == 'N' or check == 'no' or check == 'n' or check == 'No' or check == 'NO'):

				list_dl = download_numbers()
				url_list_2 = []

				for no in list_dl:
					url_list_2.append(url_list[no])

				video_save_name_list =  onefunc(url_list_2,site)


				for no in range(len(list_dl)):
					download_video(video_save_name_list[no], no+1, len(list_dl))
					

				loop = False
				
			else:
				print("Wrong Choice !")


	elif ( mode == 'N' or mode == 'no' or mode == 'n' or mode == 'No' or mode == 'NO'):
		loop = False
		print("Downloading a single file!")
		url = str(input("Paste the url of the video :  "))
		site = site_determiner(url)
		url_list = []
		url_list.append(url)
		video_save_name_list =  onefunc(url_list, site)
		#print(video_save_name_list,"duplicate")
		download_video(video_save_name_list[0], 1, 1)

	else:
			print("Wrong Choice !")
