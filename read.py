import csv
import numpy as np
import matplotlib.pyplot as plt
ssvname = "playdrone_cset.ssv"
market_name = "Google play store"

#figure 
fig_dpi=300
fig_l = 1200
fig_h = 768


#Labels :
category_label = "app category"
detection_label = "# of detections"
downloads_label = "# of download"



def virus_in_app(app, criteria=detection_label):
    """takes an element of the dataset and check if the app is infected"""
    # Another criteria could be used to limit false positives: setting a threshold (ex 10% of antiviruses find a virus)
    return(int(app[criteria]) > 0)
        
def plot_virus_categories(data):
    #virus_categories will contain a pair (non infected apps, infected apps) per category
    virus_categories = {}
    for e in data:
        categ = e[category_label]
        if categ[:4] == "GAME":
            print(categ)
            categ = "GAMES"
        if categ not in virus_categories.keys():
            virus_categories[categ] = [0,0]
        if virus_in_app(e):
            virus_categories[categ][1] += 1
        else:
            virus_categories[categ][0] += 1
    y_virus = []
    y_non_virus = []
    y_ratios = []
    list_categories = []
    for k in virus_categories:
        y_non_virus.append(virus_categories[k][0])
        y_virus.append(virus_categories[k][1])
        y_ratios.append(virus_categories[k][1]/(virus_categories[k][0]+virus_categories[k][1]))
        list_categories += [k]
    #Drawing
    fig = plt.figure("Infected apps figure")
    bar = plt.bar(range(len(virus_categories)), y_virus, align='center', color='red')
    bar2 = plt.bar(range(len(virus_categories)), y_non_virus, align='center', color='blue', bottom=y_virus)
    plt.legend((bar[0], bar2[0]), ('infected apps', 'non-infected apps'))
    for i in range(len(y_ratios)):
        height = y_virus[i]+y_non_virus[i]
        x = i
        plt.text(x, height, '%i%%' % int(y_ratios[i]*100), ha='center', va='bottom')
    
    #plot and tilt the xticks
    plt.xticks(range(len(virus_categories)), list_categories)
    ax = fig.axes[0]
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.ylabel("Number of applications")
    plt.title("Infected applications per category on " + market_name)
    #resizing to fullscreen to get a proper picture
    mng = plt.get_current_fig_manager()
    mng.resize(mng.window.maxsize()[0]/0.9,mng.window.maxsize()[1]/0.9)
    plt.show()
    fig.savefig("./images/" + market_name +"_infected_cat.png")

def plot_downloads_categories(data):
    down_categories = {}
    for e in data:
        # if int(e['# of detections'])>0:
            # print(e['file name'], " : ", e[detection_label], "/", e["# of AVs that scan the file"])
        categ = e[category_label]
        if categ[:4] == "GAME":
            print(categ)
            categ = "GAMES"
        if categ not in down_categories.keys():
            down_categories[categ] = 0
            e_down = e[downloads_label]
            e_down = e_down.replace(",","")
            if e_down.isdigit():
                D=int(e_down)
            elif e_down[-1]=="K":
                D = int(float(e_down[:-1])*1000)
            elif e_down[-1]=="M":
                D = int(float(e_down[:-1])*1000000)
            else:
                print(e[downloads_label])
        down_categories[categ] += D
    list_categories = []
    y_downloads = []
    for k in down_categories:
        list_categories.append(k)
        y_downloads.append(down_categories[k])
    #Drawing
    fig = plt.figure("Downloads figure")
    bar = plt.bar(range(len(down_categories)), y_downloads, align='center', color='0.7')
    plt.xticks(range(len(down_categories)), list_categories)
    ax = fig.axes[0]
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.ylabel("Number of downloads")
    plt.title("Downloaded applications per category on " + market_name)
    #resizing to fullscreen to get a proper picture
    mng = plt.get_current_fig_manager()
    mng.resize(mng.window.maxsize()[0]/0.9,mng.window.maxsize()[1]/0.9)
    plt.show()
    fig.savefig("./images/" + market_name +"_down_cat.png",)




def read_ssv_dataset(ssvname):
    with open(ssvname,'r') as ssvfile: 
        dataset = list(csv.reader(ssvfile, delimiter='\n'))
        #table is a list which contains each row (=application)
        # each element of table is a list which contains one string
        # this string is a semicolon separated value table
        # in eoemarket.ssv dataset[0] is the header
        headers = dataset[0][0].split(";")
        #data will contain the list of elements properly formatted in python dictionaries
        data = []
        #el_dict is the dictionary that will contain the element information with headers
        for el in dataset[1:]:
            el_dict = {}
            #get the string and split it as a list
            el = el[0].split(";")
            #assemble the dict
            for i in range(len(el)):
                el_dict[headers[i]] = el[i]
            data += [el_dict]
        return(data, headers)

if __name__ == "__main__":
    data, headers = read_ssv_dataset(ssvname)
    plot_virus_categories(data)
    plot_downloads_categories(data)