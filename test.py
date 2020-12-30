import MySQLdb

db =  MySQLdb.connect("nlp-dev2.sai.corp","root","root","azero_recommender_system",port = 3306,charset='utf8')

cursor = db.cursor()

file = "data/title"

reader = open(file,'r',encoding="utf-8")

song_comment_map = {}

for line in reader:

    data = line.strip.split("\t")

    song = data[0]

    comment_num = data[1]

    if song not in song_comment_map:

        song_comment_map[song] = comment_num

sql = "select id,name,author_name,is_original,url,comment_number,version from music_song"

cursor.execute(sql)

#获取所有记录列表

results = cursor.fetchall()

print(len(results))

song_map = {}

flag = True

for row in results:

    id = row[0]

    song_name = row[1]

    artist_name = row[2]

    is_original = row[3]

    url = row[4]

    version = row[5]

    if artist_name is None:

        artist_name = ""

    if is_original == 1 and url is not None:

        key = song_name+"\t"+artist_name

        if key not in song_map:

            song_map[key] = id

        else:

            if version == ""or version is None:
                song_map[key] = id

    song_mutli_is_original = {}

    has_checked_song = {}

    for key,value in song_map.items():

        song_name = key.split("\t")[0]

        artist_name = key.split("\t")[1]

        song_id = value

        if song_name in song_comment_map:

            comment_num = song_comment_map[song_name]

            check_key = song_name + ":" +comment_num

            if check_key not in has_checked_song:

                has_checked_song[check_key] = artist_name + "+" +str(song_id)

            else:
                if check_key in song_mutli_is_original:

                    song_mutli_is_original[check_key].append(artist_name+"+"+str(song_id))

                else:

                    song_mutli_is_original[check_key] = [artist_name+"+"+str(song_id)]

                    song_mutli_is_original[check_key].append(has_checked_song[check_key])



    for key,value in song_map.items():

        song_name = key.split("\t")[0]

        artist_name = key.split("\t")[1]

        song_id = value

        if song_name in song_comment_map:

            comment_num = song_comment_map[song_name]

            check_key = song_name + ":" + comment_num

            if ckeck_key not in song_mutli_is_original:

                sql = "update music_song set comment_number = '%s' where id = '%s'" %(comment_num,song_id)

                cursor.execute(sql)

                db.commit()

                print(sql)


    file = "data/multi_song"

    writer = open(file,'w',encoding="utf-8")

    for key,value in song_mutli_is_original.items():

        writer.writer(key+"\t")

        for item in value:

            writer.write(item+"\t")

        writer.write("\n")

    print(song_mutli_is_original)

    print(len(song_mutli_is_original))
