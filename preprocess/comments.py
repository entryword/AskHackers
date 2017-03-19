import sys
import MySQLdb
import json

def getcomments():
    text_file = open("errorComment.txt", "w")
    for i in range(17, 20):
        url = '/Users/ycymio/Downloads/comments_0000000000' + str(i)
        with open(url) as json_data:
            for myJson in json_data:
                d = json.loads(myJson)
                if d.get("id") == None or d.get("by") == None \
                        or d.get("parent") == None:
                    continue
                id = int((d["id"]).decode("utf-8"))
                by = (d["by"]).decode("utf-8")
                author = d.get("author", by)
                time = d.get("time", "")
                time_ts = d.get("time_ts", "")
                text = d.get("text", "")
                parent = d["parent"].decode("utf-8")
                ranking = 0
                if d.get("ranking") != None:
                    ranking = d["ranking"]

                conn = MySQLdb.connect(host="localhost", user="ycy", passwd="123456", db="sharing", charset="utf8")
                cursor = conn.cursor()
                sql = 'insert into comments(id, byauthor, author, timec, time_ts, text, parent, ranking) ' \
                      'values(%s, %s, %s, %s, %s, %s, %s, %s)'
                param = (id, by, author, time, time_ts, text, parent, ranking)
                try:
                    cursor.execute(sql, param)
                    # break
                except Exception as e:
                    print(d)
                    print str(e)
                    text_file.write(str(d))
                    text_file.write("\n")
                    text_file.write(str(e))
                    text_file.write("\n")

                # cursor.execute(sql, param)
                cursor.close()
                conn.commit()
                conn.close()
    text_file.close()
