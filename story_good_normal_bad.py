import argparse
from google.cloud import language
import MySQLdb

def print_result(id, parent, annotations):
    # print("print_result")
    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude

    # for index, sentence in enumerate(annotations.sentences):
    #     sentence_sentiment = sentence.sentiment.score
    #     print('Sentence {} has a sentiment score of {}'.format(
    #         index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))

    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="sharing", charset="utf8")
    cursor = db.cursor()
    sql = 'insert into UsefulScore(id, parent, score) values(%s, %s, %s)'
    # param = (int(id), float(score))
    param = (id, parent, score)
    # print id
    # print type(id)
    # print type(score)
    cursor.execute(sql, param)
    db.commit()
    cursor.close()
    # print score
    db.close()
    return 0

def openDB():
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="sharing", charset="utf8")
    cursor = db.cursor()
    cursor.execute("select id, parent, score from UsefulScore")
    data = cursor.fetchall()
    # data = cursor.fetchone()
    # print "Database version : %s " % data
    db.close()
    return data

def computeScore(_id, data):
    global good
    global normal
    global bad
    for item in data:        
        if(item[1]==_id):
            if item[2] > 0.1:
                good = good+1
            elif item[2] < -0.1:
                bad = bad+1
            else:
                normal = normal+1
    all = float(good+normal+bad)
    print(float(good)/all)
    print(float(normal)/all)
    print(float(bad)/all)

def computeSameId(data):
    _id = 85840
    computeScore(_id, data)


if __name__ == '__main__':
    good = 0
    normal = 0
    bad = 0
    data = openDB()
    computeSameId(data)
    


