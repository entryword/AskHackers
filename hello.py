from flask import Flask,render_template,url_for,request
import MySQLdb
#import story_good_normal_bad

app = Flask(__name__)
global conn

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/index')
def showindex():
    cursor = conn.cursor()
    sql = "select a.id as id, a.byauthor as byauthor, a.score as score, a.title as title, a.time_ts as time_ts, b.good as good, b.normal as normal, b.bad as bad from stories_text as a, article_score as b where a.id = b.id order by timec desc LIMIT 0, 10 " # LIMIT 5,10
    cursor.execute(sql)
    content = cursor.fetchall()
    # TODO: score
    
    entry = []
    for item in content:
        entry.append({"id": item[0], "byauthor": item[1], "score": item[2], "title": item[3]})
    return render_template('index.html',entries=entry)

@app.route('/index/<id>')
def showindexnumber(id):
    if id == 1:
        return showindex()
#    conn = MySQLdb.connect(host="localhost", user="ycy", passwd="123456", db="sharing", charset="utf8")
    cursor = conn.cursor()
    start = (int(id) - 1) * 10
    sql = "select a.id as id, a.byauthor as byauthor, a.score as score, a.title as title, a.time_ts as time_ts, b.good as good, b.normal as normal, b.bad as bad from stories_text as a, article_score as b where a.id = b.id order by timec desc LIMIT " + str(start) +", 10"
    cursor.execute(sql)
    content = cursor.fetchall()
    # TODO: score
    entry = []
    hidden = ""
    i = 0
    for item in content:
        entry.append({"id": item[0], "byauthor": item[1], "score": item[2], "title": item[3], "time_ts": item[4], "num": i})
        i = i + 1
        hidden += str(int(item[5]*100)) + ";" + str(int(item[6]*100)) + ";" + str(int(item[7]*100)) + ";"
    print hidden
    return render_template('index.html',entries=entry, hidden=hidden)

@app.route('/content/<id>')
def showcontentone(id):
    return showcontent(id, 1)


@app.route('/content/<id>/<commentid>')
def showcontent(id, commentid):
    cursor = conn.cursor()
    sql = "select title, text, byauthor, time_ts, url from stories_text where id = " + id
    cursor.execute(sql)
    stories = cursor.fetchone()
    entry = []
    entry.append({"title": stories[0], "text": stories[1], "byauthor": stories[2], "time": stories[3], "url": stories[4], "id": id})
    content = getcomment(id, commentid)
#    print commentid
    i = 1
    for item in content:
        ## TODO: rank?
        entry.append({"commentauthor": item[0], "commenttext": item[1], "numid": i})
        i = i + 1
    #    print entry
#    return ""
    return render_template('content.html', entry=entry)
#    start = (int(commentid)) * 5
#    cursor.close()

#def getrating(author):
#    cursor = conn.cursor()

def getcomment(id, commentid):
    start = (int(commentid) - 1 ) * 5
    cursor = conn.cursor()
    sql = "select byauthor, text from comments_first where parent = " + str(id) + " order by ranking desc limit " + str(start) + ", 5"
    cursor.execute(sql)
    content = cursor.fetchall()
#    print content
    return content

if __name__ == '__main__':
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="sharing", charset="utf8")
    app.run(debug=True)
    conn.close()