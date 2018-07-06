from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
import requests, os

def list_finder(playlist_url):

	url_list = []
	response = requests.get(playlist_url)
	soup = bs(response.content, "lxml")
	div_list = soup.body.find_all("a", class_="sonra")
	for item in div_list:
		link = item["href"]
		url_list.append(link)

	url_list = url_list[::-1]
	return url_list


def video_finder(url_list):

	options = Options()
	options.set_headless(headless=True)
	prefs = {'profile.managed_default_content_settings.images':2}
	options.add_experimental_option("prefs", prefs)
	driver = wd.Chrome(chrome_options=options)
	main_name = os.path.join(os.path.dirname(__file__), "..", "video")
	video_save_name_list = []

	for i in range(len(url_list)):

		url = url_list[i]
		try:
			video_save_name = url.split("/")[-1]
			video_save_name_list.append(video_save_name)
			print("[" + str(i+1) + "/" + str(len(url_list)) + "] Finding Download Link ...")

			if os.path.isfile(os.path.join(main_name, video_save_name)):
				print("[" + str(i+1) + "/" + str(len(url_list)) + "] Download Link found locally!")
			
			else:
				driver.get(url)
				video_name = driver.find_element_by_tag_name("h1").text
				iframes = driver.find_elements_by_tag_name("iframe")
				video_url=""
				for iframe in iframes:
					driver.switch_to.frame(iframe)
					try:
						video_url = driver.find_element_by_tag_name("source").get_attribute("src")
#						print(video_url)
						break
					except:
						pass
					driver.switch_to.parent_frame()

				name = os.path.join(main_name, video_save_name)
				with open(name, "w") as f:
					f.write(video_name + ',' + video_url)
					f.close()

				print("[" + str(i+1) + "/" + str(len(url_list)) + "] Download Link found !")
		
		except Exception as e :
			print(e)

	driver.quit()
	return video_save_name_list