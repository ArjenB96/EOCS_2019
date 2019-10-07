import numpy as np
import matplotlib.pyplot as plt
import csv

google_play_ssv = "playdrone_cset.ssv"

name_header = "title"
download_header = "# of download"
currency_header = "currency"
price_header = "price"
detection_header = "# of detections"
total_antivirus_header = "# of AVs that scan the file"
analysis_header = "result of scans(csv)"

exchange_rate = {"USD":1, "EUR":1.0979, "CAD":0.7512 , "KRW":0.000838, "PLN":0.254, "GBP":1.2335, "HKD":0.1275, "JPY":0.009351, "AUD":0.6771, "CHF":1.00429, "SGD":0.725272, "ILS":0.287467, "NOK": 0.109956, "SEK":0.101618, "DKK": 0.147018, "NZD":0.631691, "MXN":0.0512438, "CZK":0.0426725}

def is_malware(app):
    return(int(app[detection_header]) > 0)

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

def get_downloads_app(app):
    app_down = app[download_header]
    app_down = app_down.replace(",","")
    if app_down == "":
        pass
    elif app_down.isdigit():
        D=int(app_down)
    elif app_down[-1]=="K":
        D = int(float(app_down[:-1])*1000)
    elif app_down[-1]=="M":
        D = int(float(app_down[:-1])*1000000)
    else:
        # print("Not recognized: ", e_down, " market: ", market_name)
        pass
    return(D)

def get_price_app(app):
    cur = app[currency_header]
    price = app[price_header]
    if price == "Free":
        price = 0
    else: 
        price = float(price)
    usd_price = exchange_rate[cur]*price
    return(usd_price)

def count_downloads_market(data):
    # dict with names as keys and list [number of viruses, number of non virus]
    total_D = 0
    total_D_malwares = 0
    n_malware = 0
    for app in data:
        D = get_downloads_app(app)
        total_D += D
        if is_malware(app):
            total_D_malwares += D
            n_malware += 1
    print("Total downloads malwares = ",total_D_malwares, " Total number of malwares = ", n_malware)
    return(total_D, total_D_malwares)


def price_of_malwares (data):
    total_malware_price = 0
    total_price = 0
    n_malware = 0
    for app in data:
        usd_price = get_price_app(app)
        total_price += usd_price
        if is_malware(app):
            total_malware_price += usd_price
            n_malware += 1
    return(total_malware_price, n_malware)




def get_analysis(app):
    antivirus_dict = {}
    string_csv = app[analysis_header]
    list_csv = string_csv.split(", ")
    for a in list_csv:
        try:
            antivirus, result = a.split(":")
            antivirus_dict[antivirus] = result
        except:
            pass
    return(antivirus_dict)
        
def antivirus_analysis(data, antivirus_name):
    """Compute the number of malwares detected by McAfee and another antivirus"""
    correctly_detected = 0
    false_negative = 0
    false_positive = 0
    for app in data:
        if is_malware(app):
            analysis = get_analysis(app)
            #check if antivirus detected the app
            if antivirus_name in analysis:
                threshold = int(app[total_antivirus_header])/10
                #to stay with the definition malware = detected by one antivirus, uncomment the following line
                # threshold = 3
                if int(app[detection_header]) > threshold:
                    if analysis[antivirus_name] != "None":
                        correctly_detected += 1
                    else:
                        false_negative +=1
                else:
                    if analysis[antivirus_name] != "None":
                        false_positive += 1
    if false_negative > 0 or correctly_detected > 0:
        ratioFN = false_negative / (correctly_detected+false_negative)
        safe_apps = len(data) - correctly_detected - false_negative
        ratioFP = false_positive / safe_apps
        return(ratioFN, ratioFP)
    else:
        return(0,0) 

def print_antivirus_perf(antivirus_name, data):
    (ratioFN, ratioFP) = antivirus_analysis(data, antivirus_name)
    if (ratioFN, ratioFP) != (0,0):
        print("{0}: false positive ratio : {1:.2f}%, false negative ratio : {2}".format(antivirus_name, ratioFP *100, ratioFN *100))
    else:
        print("{0} did not detect any malware".format(antivirus_name))

if __name__ == "__main__":
    data, headers = read_ssv_dataset(google_play_ssv)
    total_D, total_D_malware = count_downloads_market(data)
    print(total_D, total_D_malware)
    malware_price, malware_number = price_of_malwares(data)
    # print("Total price {0:.2f} for {1} malwares. Average : {2:.2f}".format(malware_price, malware_number, malware_price/malware_number))
    list_antivirus = ["Zillya","Zoner","MicroWorld-eScan","Emsisoft","SUPERAntiSpyware","Fortinet","K7AntiVirus","Tencent","ViRobot","AVG","AVware","Panda","TrendMicro","Cyren","VIPRE","Avast","NANO-Antivirus","McAfee-GW-Edition","Qihoo-360","Antiy-AVL","Microsoft","F-Prot","DrWeb","AhnLab-V3","Kaspersky","Bkav","Jiangmin","VBA32","Kingsoft","Ikarus","ClamAV","ALYac","Comodo","Baidu","Sophos","K7GW","BitDefender","CMC","nProtect","Symantec","Alibaba","Ad-Aware","TotalDefense","Malwarebytes","AegisLab","CAT-QuickHeal","Avira","TheHacker","TrendMicro-HouseCall","GData","ESET-NOD32","Baidu-International","Arcabit","Yandex","F-Secure","McAfee"]
    # for antivirus_name in list_antivirus:
        # print_antivirus_perf(antivirus_name,data)
    print_antivirus_perf("McAfee",data)
    