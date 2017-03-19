import MySQLdb

class Node(object) :
    id = 0
    timec = 0.0
    score = 0.0
    count = 0.0
    x = 0.0
    pos = 0

def OWAB(w = [], a = []) :
    sum = 0.0
    for i in range(1, m) :
        sum = sum + w[i] * a[i]
    return sum

def Input():
    cursor = conn.cursor()
    sql = "select a.id as id, a.timec as timec, a.score as score , b.count as authorcount, c.count as titlecount from stories_text as a, author_count_story as b, title_count_comment as c where a.id in (select DISTINCT parent from UsefulScore) and a.byauthor = b.author and a.id = c.id;"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for item in result:
        data.append([item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])])
    return data

def OWA():
    global conn
    global m
    alpha = 0.2
    beta = 0.5
    w = [0,]
    m = 4
    b = [0 for i in range(m+1)]

    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="sharing", charset="utf8")
    cursor = conn.cursor()
    sql = "select count(*) from stories_text where id in (select DISTINCT parent from UsefulScore)"
    cursor.execute(sql)
    result = cursor.fetchone()
    n = result[0]
    
    z = [Node() for i in range(n+1)]

    a = Input() # n * m : double a[][5]
#    print a

    for i in range(1, m) :
        maxn = 0.0
        for j in range(1, n) :
            maxn = max(maxn, a[j][i])
        for j in range(1, n) :
            a[j][i] = a[j][i] / maxn;

    w.append((1 - (alpha + beta)) / m + alpha)

    for j in range(2, m - 1) :
        w.append((1 - (alpha + beta)) / m)
    w.append((1 - (alpha + beta)) / m + beta)
    
    for i in range(1, n) :
        for j in range(0, m) :
            b[j] = a[i][j]
        b.sort(reverse = True);

        z[i].x = OWAB(w, b)
        z[i].id = int(b[0])
        z[i].timec = b[1]
        z[i].score = b[2]
        z[i].acount = b[3]
        z[i].ccount = b[4]
        z[i].pos = i
    z[1:].sort(key = lambda x: x.x, reverse = True)
#    print z
    data = []
    for i in range(1, n):
        data.append(z[i].id)
    return data

if __name__ == '__main__':
    OWA()