from lxml import html
import requests
import os.path
import sys

page = []
tree = []
sunset_time = []
cron_rows = []

def getMonth(i):
    mon = ""
    if i == 1:
        mon = "January"
    elif i == 2:
        mon = "February"
    elif i == 3:
        mon = "March"
    elif i == 4:
        mon = "April"
    elif i == 5:
        mon = "May"
    elif i == 6:
        mon = "June"
    elif i == 7:
        mon = "July"
    elif i == 8:
        mon = "August"
    elif i == 9:
        mon = "September"
    elif i == 10:
        mon = "October"
    elif i == 11:
        mon = "November"
    elif i == 12:
        mon = "December"
    return mon

def fetch_data(num=2020):
    for i in range(1,13):
        print("Fetching sunset data for " + getMonth(i) + ", " + num + "...")
        page.append(requests.get('https://sunrise-sunset.org/search?location=90274&year=' + str(num) + '&month=' + str(i) + '#calendar'))
        tree = html.fromstring(page[i-1].content)
        #select td[3] for actual sunset time. Select td[4] for end of twilight
        sunset_time.append(tree.xpath('//table[@id="month"]//td[3]//text()'))
    #print(sunset_time[0])


def main():
    yr = 0
    for arg in sys.argv[1:]:
        yr = arg
    #print(yr)
    fetch_data(yr)
    print("Sunset data from " + str(yr) + " collected. Writing file...")
    sunset_file = open("sunset_data.txt", "w")
    n = 1
    for Month in sunset_time:
        k = 1
        for day in Month:
            #print(day)
            line = ""
            ss = day.split(":")
            ss_min = ss[1]
            ss_hour = ss[0]
            ss_sec = ss[2]
            ss_day = k
            ss_month = n
            ma = (ss_sec.split(" "))[1]
            if ma == "pm":
                ss_hour = 12 + int(ss_hour)
                ss_hour = str(ss_hour)
            file_name = str(yr) + "-" + str(ss_month) + "-" + str(ss_day) + "_" + ss_hour + "." + ss_min + ".jpg"
            cmd = "raspistill -vf -hf -o /home/pi/Projects/Sunset/Photos/" + file_name 
            #cmd = "ps aux  > /home/pi/Projects/Sunset/proc_sample.txt"
            line = ss_min + " " + ss_hour + " " + str(ss_day) + " " + str(ss_month) + " " + "* "
            line = line + cmd + "\n"
            sunset_file.write(line)
            k = k + 1
        #sunset_file.write("\n")
        n = n + 1

       
    print("Done.")

if __name__ == "__main__":
    main()
