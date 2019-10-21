import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.stats

ssv_names = ["eoemarket.ssv", "liqucn.ssv", "mumayi.ssv", "playdrone_cset.ssv", "gp09.ssv", "freewarelovers.ssv"]
market_names = ["eoemarket (CHN)", "liqucn (CHN)", "mumayi (CHN)", "Google play store", "gp09 (JPN)", "freewarelovers"]
downloads_label = "# of download"
category_label = "app category"
detection_label = "# of detections"
# eoemarket : "Game"
# liqucn.ssv: all are games return 100%
# mumayi : Game-...
# playdrone : "GAME SPORTS"
# freewarelovers : Games
# gp09: Game-



def virus_in_app(app,criteria):
    """takes an element of the dataset and check if the app is infected"""
    # Another criteria could be used to limit false positives: setting a threshold (ex 10% of antiviruses find a virus)
    return(int(app[criteria]) > 0)

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

def malware_percentage(filename):
    """return percentage of malware in dataset contained in filename"""
    data, headers = read_ssv_dataset(filename)

    n_malwares = 0
    for e in data:
        if virus_in_app(e, detection_label):
            n_malwares +=1
    return(n_malwares/len(data))


def games_percentage(filename):
    """return percentage of games in dataset contained in filename"""
    # liqucn contains only games
    if filename == "liqucn.ssv":
        return 1
    data, headers = read_ssv_dataset(filename)

    n_category = 0
    for e in data:
        categ = e[category_label].lower()
        if categ[:4] == "game":
            n_category += 1
    return(n_category/len(data))

def list_categories(filename):
    data, headers = read_ssv_dataset(filename)
    cats = []
    for e in data:
        categ = e[category_label].lower()
        if categ not in cats:
            cats.append(categ)
            print(categ)

def figure_categories_malwares(x_ticks, y_mal, y_down, print_r=False, print_rho=False):
    
    indices = np.argsort(-y_mal)
    y_mal = [y_mal[i] for i in indices]
    y_down = [y_down[i] for i in indices]
    x_ticks = [x_ticks[i] for i in indices]

    x = np.arange(len(x_ticks))
    fig, ax1 = plt.subplots()
    color = [0.85,0,0]
    ax1.set_ylabel("Malware proportion", color=color)
    ax1.plot(x,y_mal, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = [0,0,0.9]
    ax2.plot(x,y_down, color=color)
    ax2.set_ylabel("Downloads", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.xticks(x, x_ticks)
    plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
    fig.tight_layout()
    plt.title(market_name + ": malware proportion and downloads per category")

    #correlation:
    if print_r or print_rho:
        legend = "Correlation :"
        if print_r:
            corr_r = scipy.stats.pearsonr(y_mal,y_down)[0]
            legend += "\n" + r"$r$={0:0.4f}".format(corr_r)
        if print_rho:
            corr_rho = scipy.stats.spearmanr(y_mal,y_down)[0]
            legend += "\n" + r"$\rho$={0:0.4f}".format(corr_rho)
        plt.plot([], [], ' ', label=legend)
        plt.legend()
    #resizing to fullscreen to get a proper picture
    mng = plt.get_current_fig_manager()
    mng.resize(mng.window.maxsize()[0]/0.9,mng.window.maxsize()[1]/0.9)
    plt.show()
    fig.savefig("./images/"+market_name +"_down&mal.png")




def corr_categories_malware(filename, market_name, print_r=False, print_rho=False):
    data, headers = read_ssv_dataset(filename)
    categories_list = {}
    for e in data:
        categ = e[category_label].lower()
        if categ[:4] == "game":
            categ = "game"
        if categ not in categories_list:
            categories_list[categ] = [0,0]
        if virus_in_app(e,detection_label):
            categories_list[categ][1] += 1
        e_down = e[downloads_label].replace(",","")
        if e_down == "":
            D = 0
        elif e_down.isdigit():
            D=int(e_down)
        elif e_down[-1]=="K":
            D = int(float(e_down[:-1])*1000)
        elif e_down[-1]=="M":
            D = int(float(e_down[:-1])*1000000)
        else:
            print(e[downloads_label])
        categories_list[categ][0] += D
    
    x_ticks = []
    y_down = []
    y_mal = []
    for c in categories_list:
        x_ticks.append(c)
        y_down.append(categories_list[c][0])
        y_mal.append(categories_list[c][1])
    y_mal = np.array(y_mal) / sum(y_mal)
    figure_categories_malwares(x_ticks,y_mal,y_down, print_r, print_rho)
    





def plot_markets_games(y_game,y_malware,market_names):
    x = np.arange(len(market_names))
    fig = plt.figure()
    plt.plot(x,y_game, label="Games proportion", color=[0,0.7,0])
    plt.plot(x,y_malware, label="Malwares proportion", color=[0.7,0,0])
    plt.xticks(x, market_names)
    ax = fig.axes[0]
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.legend()
    corr_r = scipy.stats.pearsonr(y_malware,y_game)[0]
    corr_rho = scipy.stats.spearmanr(y_malware,y_game)[0]
    plt.figtext(0.8,0.5,r"$r$={0:0.4f}".format(corr_r) + "\n" + r"$\rho$={0:0.4f}".format(corr_rho), ha="center", fontsize=10)
    plt.title("Malwares and games proportion per market")
    mng = plt.get_current_fig_manager()
    mng.resize(mng.window.maxsize()[0]/0.9,mng.window.maxsize()[1]/0.9)
    plt.show()
    fig.savefig("./images/markets.png")


if __name__ == "__main__":
    y_game = []
    y_malware = []
    x_ticks = []
    for i in range(len(ssv_names)):
        filename = ssv_names[i]
        market_name = market_names[i]
        f_game = games_percentage(filename)
        f_malware = malware_percentage(filename)
        print(market_name + ": games {0:0.3f}, malwares {1:0.3f}".format(f_game, f_malware))
        y_game.append(f_game)
        y_malware.append(f_malware)
        # list_categories(filename)
        if market_name != "freewarelovers":
            # freewarelovers has no download data
            corr_categories_malware(filename, market_names[i], print_r=True, print_rho=True)
    plot_markets_games(y_game,y_malware,market_names)

    
    