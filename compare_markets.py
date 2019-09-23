import numpy as np
import matplotlib.pyplot as plt
import csv

ssv_names = ["eoemarket.ssv", "liqucn.ssv", "mumayi.ssv", "playdrone_cset.ssv", "freewarelovers.ssv", "gp09.ssv"]
market_names = ["eoemarket (CHN)", "liqucn (CHN)", "mumayi (CHN)", "Google play store", "freewarelovers", "gp09 (JPN)"]
detection_labels = ["# of detections", "# of detections", "# of detections", "# of detections", "# of detections", "# of detections"]
downloads_labels = ["# of download","# of download","# of download","# of download","","# of download"]



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

        
def virus_in_app(app, criteria):
    """takes an element of the dataset and check if the app is infected"""
    # Another criteria could be used to limit false positives: setting a threshold (ex 10% of antiviruses find a virus)
    return(int(app[criteria]) > 0)

def plot_virus_market(normalized=False):
    # dict with names as keys and list [number of viruses, number of non virus]
    market_virus = {}
    for name in market_names:
        market_virus[name] = [0,0]
    for index, ssvfile in enumerate(ssv_names):
        market_name = market_names[index]
        data, headers = read_ssv_dataset(ssvfile)
        detection_header = detection_labels[index]
        for e in data:
            if virus_in_app(e, detection_header):
                market_virus[market_name][0] += 1
            else:
                market_virus[market_name][1] += 1
    y_virus = []
    y_non_virus = []
    y_ratios = []
    for n in market_names:
        y_virus.append(market_virus[n][0])
        y_non_virus.append(market_virus[n][1])
        y_ratios.append(market_virus[n][0]/(market_virus[n][0]+market_virus[n][1]))
    #Drawing
    fig = plt.figure("Infected apps figure")
    ax = plt.gca()
    if normalized == False:
        bar = plt.bar(range(len(market_virus)), y_virus, align='center', color='red')
        bar2 = plt.bar(range(len(market_virus)), y_non_virus, align='center', color='blue', bottom=y_virus)
        plt.legend((bar[0], bar2[0]), ('infected apps', 'non-infected apps'))
        plt.ylabel("Number of applications")
        figname = "market_ratios.png"
        for i in range(len(y_ratios)):
            height = y_virus[i]+y_non_virus[i]
            x = i
            plt.text(x, height, '%i%%' % int(y_ratios[i]*100), ha='center', va='bottom')
    else:
        bar = plt.bar(range(len(market_virus)), np.array(y_ratios)*100, align='center', color=[0.8,0,0])
        plt.ylabel("Proportion of infected applications (%)")
        ax.set_ylim([0,100])
        figname = "market_ratios_norm.png"
        for i in range(len(y_ratios)):
            height = y_ratios[i]*100 +1
            x = i
            plt.text(x, height, '%i%%' % int(y_ratios[i]*100), ha='center', va='bottom')
    for i in range(len(y_ratios)):
        height = y_virus[i]+y_non_virus[i]
        x = i
        plt.text(x, height, '%i%%' % int(y_ratios[i]*100), ha='center', va='bottom')
    #plot and tilt the xticks
    plt.xticks(range(len(market_virus)), market_names)    
    plt.title("Percentage of infected applications on different Android stores")
    #resizing to fullscreen to get a proper picture
    mng = plt.get_current_fig_manager()
    mng.resize(mng.window.maxsize()[0]/0.9,mng.window.maxsize()[1]/0.9)
    plt.show()
    fig.savefig("./images/" + figname)


def plot_downloads_market(normalized=False):
    # dict with names as keys and list [number of viruses, number of non virus]
    market_down = {}
    for index,name in enumerate(market_names):
        download_header = downloads_labels[index]
        #check if downloads data in the dataset
        if download_header != "":
            market_down[name] = [0,0]
    for index, ssvfile in enumerate(ssv_names):
        if market_names[index] in market_down: 
            market_name = market_names[index] 
            data, headers = read_ssv_dataset(ssvfile)
            for e in data:
                e_down = e[download_header]
                e_down = e_down.replace(",","")
                if e_down == "":
                    pass
                elif e_down.isdigit():
                    D=int(e_down)
                elif e_down[-1]=="K":
                    D = int(float(e_down[:-1])*1000)
                elif e_down[-1]=="M":
                    D = int(float(e_down[:-1])*1000000)
                else:
                    # print("Not recognized: ", e_down, " market: ", market_name)
                    pass

                if virus_in_app(e, detection_labels[index]):
                    market_down[market_name][0] += D
                else:
                    market_down[market_name][1] += D
    y_virus = []
    y_non_virus = []
    y_ratios = []
    x_ticks = []
    for n in market_down:
        y_virus.append(market_down[n][0])
        y_non_virus.append(market_down[n][1])
        y_ratios.append(market_down[n][0]/(market_down[n][0]+market_down[n][1]))
        x_ticks.append(n)
    #Drawing
    fig = plt.figure("Downloaded apps figure")
    if normalized == False:
        bar = plt.bar(range(len(market_down)), y_virus, align='center', color='red')
        bar2 = plt.bar(range(len(market_down)), y_non_virus, align='center', color='blue', bottom=y_virus)
        plt.legend((bar[0], bar2[0]), ('infected apps', 'non-infected apps'))
        plt.ylabel("Number of downloads")
        figname = "market_down.png"
        for i in range(len(y_ratios)):
            height = y_virus[i]+y_non_virus[i]
            x = i
            plt.text(x, height, '%i%%' % int(y_ratios[i]*100), ha='center', va='bottom')
    else:
        bar = plt.bar(range(len(market_down)), np.array(y_ratios)*100, align='center', color=[0.8,0,0])
        plt.ylabel("Proportion of infected downloadss (%)")
        figname = "market_down_norm.png"
        for i in range(len(y_ratios)):
            height = y_ratios[i]*100
            x = i
            plt.text(x, height, '%i%%' % int(y_ratios[i]*100), ha='center', va='bottom')
    #plot and tilt the xticks
    plt.xticks(range(len(market_down)), x_ticks)    
    plt.title("Percentage of infected downloads on different Android stores")
    #resizing to fullscreen to get a proper picture
    mng = plt.get_current_fig_manager()
    mng.resize(mng.window.maxsize()[0]/0.9,mng.window.maxsize()[1]/0.9)
    plt.show()
    fig.savefig("./images/" + figname)


if __name__ == "__main__":
    plot_virus_market(normalized=False)
    plot_downloads_market(normalized=False)
    plot_virus_market(normalized=True)
    plot_downloads_market(normalized=True)