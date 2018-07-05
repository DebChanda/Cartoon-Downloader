#! /usr/bin/env python3

import requests, gi, threading, ast, os
from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib, Gdk

"""
TO DO LIST 
1. add playlist feature
2. add folder button(implemented but under developement)
3. disabling and enabling butttons(done)
4. using list insted of dictionary
5. add about page(under maintainence)

"""

def video_finder(url, window , signal = False):

    options = Options()
    print("Started...")
    options.set_headless(headless=True)
    driver = wd.Firefox(firefox_options=options)
    # driver = wd.Firefox()
    name = os.path.join(main_path, "video", url.split("/")[-1])
    try:
        driver.get(url)
        video_name = driver.find_element_by_tag_name("h1").text
        iframes = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(iframes[2])
        video_url = driver.find_elements_by_tag_name("source")[0].get_attribute("src")
        driver.quit()
        print(video_url,video_name)
        window.if_checking = False
        window.findvalue = True
        window.dictionary[video_name] = video_url
        window.video_url = video_url
        window.video_name = video_name
        with open(name, "w") as f:
            f.write("{'"+video_name+"':'"+video_url+"'}")
            f.close()

    except Exception as e:
        driver.quit()
        window.video_url = e
        window.if_checking = False
        window.findvalue = False


def list_finder(url):
    dictionary = {}
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    div_list = soup.body.find_all("a", class_="sonra")
    for item in div_list:
        key = item.text
        link = item["href"]
        dictionary[key] = link
    return dictionary


def download(save_name, video_url, window):
    print(video_url)
    with open(save_name, "wb") as f:
        response = requests.get(video_url, stream=True)
        total = 1
        total = int(response.headers.get("content-length"))
        dl = 0
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            dl += len(data)
            done = round(float(dl / total),4)
            window.dload = done


    window.progressbar_1.hide()
    window.label_1.set_text("Download Complete")
    window.progressbar_1.set_fraction(0.0)
    window.download_incomplete = False

"""
dictionary = list_finder("https://www.watchcartoononline.com/anime/pokemon-sun-moon")
video_list = {}
for key  in dictionary:
    print(key, dictionary[key])
    video_url = video_finder(dictionary[key])
    video_list[key]=video_url
"""

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=program_name)
        self.set_icon_from_file("icon.png")
        self.set_resizable(False)
        self.set_border_width(15)
        self.set_default_size(200, 50)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.main_area = Gtk.Stack()
        self.main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_area.set_transition_duration(200)

        # items that goes inside main area

        # for url only
        self.box_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_area.add_titled(self.box_1, "box for url type", "Video")
        self.url_entry = Gtk.Entry(valign  = Gtk.Align.CENTER)
        self.url_entry.set_text("Video link here!")
        self.box_1.pack_start(self.url_entry, True, True, 0)

        self.button1 = Gtk.Button(label="Search", valign = Gtk.Align.CENTER)
        self.button1.connect("clicked", self.find)
        self.box_1.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="Download", valign = Gtk.Align.CENTER)
        self.button2.connect("clicked", self.on_file_clicked)
        self.box_1.pack_start(self.button2, True, True, 0)

        self.button3 = Gtk.Button(label=" Cancel & Exit ", halign=Gtk.Align.CENTER)
        self.button3.connect("clicked", Gtk.main_quit)
        self.box_1.pack_start(self.button3, True, True, 0)

        self.progressbar_1 = Gtk.ProgressBar()
        self.box_1.pack_start(self.progressbar_1, True, True, 0)

        self.label_1 = Gtk.Label("Paste the URL and click Search", halign=Gtk.Align.CENTER)
        self.label_1.set_justify(Gtk.Justification.LEFT)
        self.label_1.set_line_wrap(True)

        self.box_1.pack_start(self.label_1, True, True, 0)
        self.dictionary = {}

        # for playlist only
        self.box_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_area.add_titled(self.box_2, "box for playlist", "Playlist")
        self.label_2 = Gtk.Label("Coming Soon.")
        self.box_2.pack_start(self.label_2, True, True, 0)

        # for settings page
        self.box_3 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,spacing = 10)
        self.main_area.add_titled(self.box_3, "box for Settings", "Settings")

        self.hbox1 = Gtk.Box(spacing = 10, orientation = Gtk.Orientation.HORIZONTAL)
        self.box_3.pack_start(self.hbox1,True,True,0)

        self.check_button = Gtk.CheckButton("Change video location",halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
        self.check_button.connect("toggled",self.video_dir_change)
        self.hbox1.pack_start(self.check_button,True,True,0)

        self.change_dir = Gtk.FileChooserButton(title = "Select folder", action = Gtk.FileChooserAction.SELECT_FOLDER,
                                                halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)
        self.hbox1.pack_start(self.change_dir,True,True,0)

        self.label_3 = Gtk.Label("Don't use under construction")
        self.box_3.pack_start(self.label_3,True, True,0)

        self.button4 = Gtk.Button(" About ",halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
        self.button4.connect("clicked",self.show_about)
        self.box_3.pack_end(self.button4,True, True, 0)



        # Adding stacks and switchers
        self.stack_switcher = Gtk.StackSwitcher(halign=Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
        self.stack_switcher.set_stack(self.main_area)

        self.box.pack_start(self.stack_switcher, True, True, 0)
        self.box.pack_start(self.main_area, True, True, 0)

        # self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)
        self.findvalue = False

    def show_about(self,widget):

        self.about = Gtk.AboutDialog()
        self.about.run()

    def find(self, widget):
        self.progressbar_1.show()
        self.progressbar_1.set_fraction(0.0)
        self.progressbar_1.pulse()
        self.url = self.url_entry.get_text()
        self.button2.hide()
        self.video_url = ""
        self.video_name = ""
        self.button1.set_sensitive(False)
        self.button3.show()
        self.name = os.path.join(main_path,"video",self.url.split("/")[-1])
        try:
            self.file = open(self.name,"r")
            self.dictionary = ast.literal_eval(self.file.read())
            self.video_name = next(iter(self.dictionary))
            self.video_url = self.dictionary[self.video_name]

            self.label_1.set_text("Video URL found locally.")
            self.button2.show()
            self.progressbar_1.hide()
            self.progressbar_1.set_fraction(0.0)
            self.file.close()
            self.if_checking =True
            self.findvalue = True
            self.button1.set_sensitive(True)
            self.button3.hide()

        except:

            self.if_checking =True
            self.label_1.set_text("Finding video URL...")
            self.findvalue = False
            thread = threading.Thread(target=video_finder, name="Thread 1", args=(self.url, self))
            thread.daemon = True
            thread.start()
            GLib.timeout_add(100, self.check_if_found)


    def download_monitor(self):

        if self.download_incomplete:
            self.label_1.set_text("Downloading {0:.2f} %".format(self.dload*100))
            self.progressbar_1.set_fraction(self.dload)
        else:
            self.button3.hide()
            self.button1.set_sensitive(True)
            self.button2.set_sensitive(True)

        return self.download_incomplete


    def video_dir_change(self,widget):

        if self.check_button.get_active():
            self.change_dir.set_sensitive(True)
        else:
            self.change_dir.set_sensitive(False)

    def check_if_found(self):

        if not self.if_checking:
            if self.findvalue:
                self.label_1.set_text("Video URL found.")
                self.button2.show()
                self.progressbar_1.hide()
                self.progressbar_1.set_fraction(0.0)

            else:
                self.label_1.set_text("Error " + str(self.video_url))
                self.progressbar_1.hide()
                self.progressbar_1.set_fraction(0.0)

            self.button1.set_sensitive(True)
            self.button3.hide()
        else:
            self.progressbar_1.pulse()

        self.trial = not self.findvalue and self.if_checking
        return self.trial

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Save As", self, Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_current_name(self.video_name + ".flv")
        response = dialog.run()
        self.button3.show()
        self.button1.set_sensitive(False)
        self.button2.set_sensitive(False)


        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.OK:
            self.save_name = dialog.get_filename()
            self.progressbar_1.set_fraction(0.0)
            self.progressbar_1.show()
            thread_2 = threading.Thread(target=download,args=(self.save_name,self.video_url,self))
            thread_2.daemon = True
            thread_2.start()
            self.download_incomplete = True
            self.dload = 0.0
            GLib.timeout_add(250,self.download_monitor)

        dialog.destroy()

# main program launches
Gdk.threads_init()
main_path = os.path.dirname(__file__)
folder_to_create = ["video","playlist"]
program_name = "Cartoon Downloader 2.8"

for folder in folder_to_create:

    if not os.path.exists(os.path.join(main_path, folder)):
        os.makedirs(os.path.join(main_path, folder))


win = Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
win.progressbar_1.hide()
win.button2.hide()
win.button3.hide()
win.change_dir.set_sensitive(False)
Gtk.main()

