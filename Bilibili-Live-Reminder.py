from time import sleep
from json import load, loads
from win10toast import ToastNotifier
from requests import get


#Init config (config.json)
config_file = open("config.json",encoding="UTF-8")
config = load(config_file)
config_file.close
flag = False

#Push
toaster = ToastNotifier()
def push(name:str, title="Live Reminder", time=0, icon=None):
        toaster.show_toast(title, name + " is live sreaming.", icon, time, True)

#Check
def check(id,flag):
    data = get("https://api.bilibili.com/x/space/acc/info?mid="+id,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"}).text
    live_status = loads(data)["data"]["live_room"]["liveStatus"]
    if live_status == 0:
        return False
    elif live_status == 1 and flag == False:
        return True, loads(data)["data"]["live_room"]["url"]
    else:
        return None

#Start the loop
print("Service is running, will check every %s seconds." % config["sleep_time"])
while True:
    status = check(config["uid"],flag)

    if status == None:
        pass
    elif status == False:
        flag = False
    elif status[0] == True:
        flag = True
        
        push(config["name"],icon=config["icon_path"])
        #TODO Jump to URL

    sleep(config["sleep_time"])
