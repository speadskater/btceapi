import urllib.request
import datetime
import time
import timeit

def importing():
    html = urllib.request.urlopen("https://btc-e.com/api/2/btc_usd/depth")
    htmlSource = html.read()
    html.close()
    chop = str(htmlSource)
    chop = chop[2:]
    return chop

def depthpull():
    depth = importing()
    depth = str(depth)
    depth = depth[1:len(depth)-1]
    count = 0
    for i in depth:
        if i == ':':
            hold1 = count+1
            break
        count+=1
    ask = depth[hold1:]
    count = 0
    for i in ask:
        if i == ':':
            hold2= count+1
            break
        count+=1
    count=0
    for i in ask:
        if i == '"':
            hold1 = count-1
            break
        count+=1
    bid = ask[hold2+1:-1]
    ask = ask[1:hold1-1]
    for i in ask:
        ask=ask.replace('[','')
        ask=ask.replace(']','')
    for i in bid:
        bid=bid.replace('[','')
        bid=bid.replace(']','')

    return ask , bid

def depthlist():
    ask , bid = depthpull()
    asklist = []
    bidlist = []
    hold = ''
    count=0
    length=0
    for i in ask:
        if i == ',':
            asklist+= [hold]
            hold = ''
            count+= length+2
            length = 0
        else:
            hold += i
            length+=1
    hold = ''
    count=0
    length=0
    for i in bid:
        if i == ',':
            bidlist+= [hold]
            hold = ''
            count+= length+2
            length = 0
        else:
            hold += i
            length+=1
    return asklist , bidlist

def depthparse():
    asklist , bidlist = depthlist()
    askprice=[]
    askquantity=[]
    bidprice=[]
    bidquantity=[]
    count=0
    for i in asklist:
        if count%2==0:
            askprice += [i]
        else:
            askquantity += [i]
        count+=1
    count=0
    for i in bidlist:
        if count%2==0:
            bidprice += [i]
        else:
            bidquantity += [i]
        count+=1
    return askprice , askquantity , bidprice , bidquantity

def value():
    askprice , askquantity , bidprice , bidquantity = depthparse()
    askvalue = []
    bidvalue = []
    for i,j in list(zip(askprice,askquantity)):
        askvalue += [round(float(i)*float(j),8)]
    for i,j in list(zip(bidprice,bidquantity)):
        bidvalue += [round(float(i)*float(j),8)]
    return askvalue, bidvalue


def main():
    aps = []
    aqs = []
    bps = []
    bqs = []
    avs = []
    bvs = []
    while True:
        start = timeit.default_timer()
        today = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        askprice , askquantity , bidprice , bidquantity = depthparse()
        askvalue, bidvalue = value()
        aps += [askprice]
        aqs += [askquantity]
        bps += [bidprice]
        bqs += [bidquantity]
        avs += [askvalue]
        bvs += [bidvalue]
        if len(aps)>100:
            aps = aps[0:99]
            aqs = aqs[0:99]
            bps = bps[0:99]
            bqs = bqs[0:99]
            avs = avs[0:99]
            bvs = bvs[0:99]
        print("At ", today)
        print("Buy at", askprice[0]," Dollars", ", You can buy up to", askvalue[0], " BTC")
        print("Sell at", bidprice[0], " Dollars",", You can sell up to", bidvalue[0], " BTC")
        stop = timeit.default_timer()
        if 5-(stop-start)>0:
            time.sleep(5-(stop-start))

main()
