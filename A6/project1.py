import json
import sys
import matplotlib.pyplot as plt
import datetime
import csv
import time

def parse_tweet(val):
    body = ''
    date = ''
    sentiment = ''

    date = val['created_at']['$date']
    date = datetime.datetime.fromtimestamp(int(date)/1000.0).strftime('%Y-%m-%d %H:%M:%S') #2013-01-29 10:25:26
    body_text = val['body'].encode("ascii", "ignore").lower()
    for ch in body_text:
        if ch.isalnum() or ch==' ':
            body+=ch

    if val['entities'].get('sentiment', None) != None:
        sentiment =  val['entities']['sentiment'].get('basic','Unknown')
    else :
        sentiment = 'Unknown'


    return [date, body, sentiment]


def read_stocktwits():
    allTweets = json.load(open('BAC.json'))
    extractList = [ parse_tweet(val) for val in allTweets]
    f = open("BAC.csv", "w")
    for line in extractList:
        f.write(','.join(line)+"\n")
    f.close()
    return


def sentiment_analysis():
    positive_list=[]
    negative_list=[]
    #read positive list
    positive_file=  open('positive_words.txt', 'rb')
    p_reader = csv.reader(positive_file)
    for row in p_reader:
        positive_list.append(row[0])
    positive_file.close()

    negative_file=  open('negative_words.txt', 'rb')
    n_reader = csv.reader(negative_file)
    for row in n_reader:
        negative_list.append(row[0])
    negative_file.close()

    csvfile=  open('BAC.csv', 'rb')
    outfile=  open('BAC2.csv', 'w')
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        p_count=0
        n_count=0
        sentiment=row[2]
        if row[2]=='Unknown':
            body = row[1]
            for word in body.split():
                if word in positive_list:p_count+=1
                elif word in negative_list: n_count+=1

            if(p_count>n_count): sentiment='Bullish'
            elif(p_count<n_count):sentiment='Bearish'
            else: sentiment='Neutral'


        outfile.write(','.join([row[0], sentiment])+"\n")

    outfile.close()
    csvfile.close()
    return


def get_sentiment_dates(start_date, end_date):
    # datetime.datetime(*time.strptime("1988-02-12 5:30:23", "%Y-%m-%d %H:%M:%S")[0:3]).strftime("%d/%m/%Y")
    start= datetime.date(*time.strptime(start_date, "%Y-%m-%d")[0:3])
    end= datetime.date(*time.strptime(end_date, "%Y-%m-%d")[0:3])
    positive_dict = {}
    negative_dict = {}
    neutral_dict = {}
    csvfile=  open('BAC2.csv', 'rb')
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        row_date = datetime.date(*time.strptime(row[0].split()[0], "%Y-%m-%d")[0:3])
        date=row_date
        # date=str(row_date)
        if start<=row_date and row_date<=end:
            if(row[1]=='Bullish'):
                count = positive_dict.get(date,0)+1
                positive_dict[date]=count
            elif(row[1]=='Bearish'):
                count = negative_dict.get(date,0)+1
                negative_dict[date]=count
            else:
                count = neutral_dict.get(date,0)+1
                neutral_dict[date]=count
    csvfile.close()
    return [positive_dict, negative_dict, neutral_dict]


def drawing_pie(start_date, end_date):
    p_count=0
    n_count=0
    neu_count=0
    sentiment = get_sentiment_dates(start_date,end_date)
    for semt in sentiment[0].values():
        p_count+=semt
    for semt in sentiment[1].values():
        n_count+=semt
    for semt in sentiment[2].values():
        neu_count+=semt

    print p_count
    print n_count
    print neu_count
    labels = 'Positive','Negative','Neutral'
    sizes = [p_count,n_count,neu_count]
    colors = ['green', 'red', 'yellow']
    explode = (0, 0.1, 0) # only "explode" the 2nd slice

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('Sentiment is Positive')

    plt.show()
    return


def drawing_lines(start_date, end_date):
    sentiment = get_sentiment_dates(start_date,end_date)
    date_ol = sorted(sentiment[0])
    p_list =[]
    n_list=[]
    nu_list=[]
    for key in date_ol:
        p_list.append(sentiment[0].get(key))
        n_list.append(sentiment[1].get(key))
        nu_list.append(sentiment[2].get(key))

    data_list=[p_list,n_list,nu_list]
    fig, ax = plt.subplots()
    # ax.plot(data_list,('date', 'p', 'n', 'nu'), subplots=False)
    ax.plot(date_ol,p_list, 'o-')
    ax.plot(date_ol,n_list, 'o-')
    ax.plot(date_ol,nu_list, 'o-')
    # ax.plot([1, 2, 3])
    ax.legend(['Positive', 'Negative', 'Neutral'])
    plt.title('Sentiment between 2013-01-02 and 2013-01-31')


    fig.autofmt_xdate()
    plt.show()
    return


def main():
    read_stocktwits()  # output: BAC.csv
    sentiment_analysis() # output BAC2.csv
    print get_sentiment_dates('2013-01-02', '2013-01-31')#As you can see in the output, I used datetime.date objects as keys of a dictionary. You can also do this, you can use date strings as keys.
    drawing_pie('2013-01-02', '2013-01-31') #output: pie_sentiment.png - you can see a graph in a pop-up window. you don't need to save the graph
    drawing_lines('2013-01-02', '2013-01-31') # output: lines_sentiment.png
    return


if __name__ == '__main__':
    main()
