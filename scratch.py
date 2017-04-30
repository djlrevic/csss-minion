cur.execute("SELECT user_id, exp, level FROM experience")
while True:
    result = cur.fetchone()
    if result == None:
        break
    else:
        list(result)
        # print(str(result[0]) + ', ' + str(userLevel(result[1])[0]))
        # cur.execute("INSERT INTO experience (level) WHERE user_id = (%s) VALUES (%s)", ((result[0], userLevel(result[1])[0]),) )
        level = userLevel(result[1])[0]
        cur.execute("UPDATE experience SET level = "+str(level)+" WHERE user_id = "+str(result[0])+";")
        
UPDATE experience SET level = userLevel((SELECT exp FROM experience)) WHERE level = None