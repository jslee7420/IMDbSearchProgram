import pymysql
import time


def conv(attr):
    """
        convert '\\N' to null value
    """
    return None if attr == "\\N" else attr


def create_tables():
    """
        This function creates tables for IMDb database
    """

    commands = [
        ['create table movie completed', """create table movie(
            tconst varchar(20) primary key,
            titleType  varchar(20) not null,
            primaryTitle  varchar(2048) not null,
            originalTitle  varchar(2048) not null,
            isAdult boolean not null,
            startYear  int,
            endYear  int,
            runtimeMinutes  int
        )"""],
        ['create table review completed', """create table review(
            tconst varchar(20) primary key,
            averageRating float not null,
            numVotes int not null
        )"""],
        ['create table person completed', """create table person(
            nconst varchar(20) primary key,
            primaryName varchar(2048) not null,
            birthYear int,
            deathYear int
        )"""],
        ['create table localtitleinfo completed', """create table localtitleinfo(
            titleid varchar(20) not null,
            ordering int not null,
            title varchar(2048) not null,
            region varchar(30),
            language varchar(30),
            types varchar(200),
            attributes varchar(200),
            isOriginalTitle boolean,
            primary key(titleid, ordering),
            foreign key(titleid) references movie(tconst)
                on update cascade
                on delete cascade
        )"""],
        ['create table genre completed', """create table genre(
            tconst varchar(20) not null,
            genre varchar(60) not null,
            primary key(tconst, genre),
            foreign key(tconst) references movie(tconst)
                on update cascade
                on delete cascade
        )"""],
        ['create table knownfortitle completed', """create table knownfortitle(
            tconst varchar(20) not null,
            nconst varchar(20) not null,
            primary key(tconst, nconst),
            foreign key(tconst) references movie(tconst)
                on update cascade
                on delete cascade,
            foreign key(nconst) references person(nconst)
                on update cascade
                on delete cascade
        )"""],
        ['create table principal completed', """create table principal(
            tconst varchar(20) not null,
            ordering int not null,
            nconst varchar(20) not null,
            category varchar(30),
            job varchar(4096),
            characters varchar(2048),
            primary key(tconst, nconst)
        )"""],
        ['create table crew completed', """create table crew(
            tconst varchar(20) not null,
            nconst varchar(20) not null,
            job varchar(10) not null,
            primary key(tconst, nconst, job),
            foreign key(tconst) references movie(tconst)
                on update cascade
                on delete cascade,
            foreign key(nconst) references person(nconst)
                on update cascade
                on delete cascade
        )"""],
        ['create table primaryprofession completed', """create table primaryprofession(
            nconst varchar(20) not null,
            profession varchar(100) not null,
            primary key(nconst, profession),
            foreign key(nconst) references person(nconst)
                on update cascade
                on delete cascade
        )"""],
        ['create table episode completed', """create table episode(
            tconst varchar(20) not null,
            parentTconst varchar(20) not null,
            seasonNumber int,
            episodeNumber int,
            primary key(tconst, parentTconst),
            foreign key(tconst) references movie(tconst)
                on update cascade
                on delete cascade
        )"""]
    ]

    conn = pymysql.connect(host='localhost', user='db2021',
                           password='db2021', db='IMDb')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    for command in commands:
        cur.execute(command[1])
        conn.commit()
        print(command[0])

    cur.close()
    conn.close()


def load_data_from_file1():
    """
        insert data from file to table(movie, person, review, localTitleInfo, episode, principal)
    """
    commands = [
        {'fileName': 'title.basics.tsv/data.tsv',
         'sql': """insert into movie(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes)
            values(%s, %s, %s, %s, %s, %s, %s, %s)
        """, 'lastIndex': -1},
        {
            'fileName': 'name.basics.tsv/data.tsv',
            'sql': """insert into person(nconst, primaryName, birthYear, deathYear)
                values(%s, %s, %s, %s)
            """,
            'lastIndex': -2
        },
        {
            'fileName': 'title.ratings.tsv/data.tsv',
            'sql': """insert into review(tconst, averageRating, numVotes)
                values(%s, %s, %s)
            """,
            'lastIndex': None
        },
        {
            'fileName': 'title.akas.tsv/data.tsv',
            'sql': """insert ignore into localTitleInfo(titleId, ordering, title, region, language, types, attributes, isOriginalTitle)
            values(%s, %s, %s, %s, %s, %s, %s, %s)""",
            'lastIndex': None
        },
        {
            'fileName': 'title.episode.tsv/data.tsv',
            'sql': """insert ignore into episode(tconst, parentTconst, seasonNumber, episodeNumber)
            values(%s, %s, %s, %s)""",
            'lastIndex': None
        },
        {
            'fileName': 'title.principals.tsv/data.tsv',
            'sql': """insert ignore into principal(tconst, ordering, nconst, category, job, characters)
            values(%s, %s, %s, %s, %s, %s)""",
            'lastIndex': None
        }
    ]
    tableNames = ['movie', 'person', 'review',
                  'localtitleinfo', 'episode', 'principal']

    conn = pymysql.connect(host='localhost', user='db2021',
                           password='db2021', db='IMDb')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    for idx in range(len(commands)):
        f = open(commands[idx]['fileName'], 'rt', encoding='UTF8')
        oneline = f.readline()
        oneline = f.readline()[:-1]
        rows = []
        i = 0

        while oneline:
            attrs_list = oneline.split('\t')[:commands[idx]['lastIndex']]
            attrs = tuple([conv(attr) for attr in attrs_list])
            rows.append(attrs)
            i += 1
            if i % 20000 == 0:
                cur.executemany(commands[idx]['sql'], rows)
                conn.commit()
                rows = []
                print("%d rows" % i)
            oneline = f.readline()[:-1]

        if rows:
            cur.executemany(commands[idx]['sql'], rows)
            conn.commit()
            print("%d rows" % i)
        print('Insert data into ', tableNames[idx], ' completed!')

    f.close()
    cur.close()
    conn.close()


def nomalization():
    commands = [
        ['title.basics.tsv/data.tsv', """insert into genre(tconst, genre)
            values(%s, %s)"""],
        ['name.basics.tsv/data.tsv', """insert ignore into knownfortitle(tconst, nconst)
            values(%s, %s)"""],
        ['title.crew.tsv/data.tsv', """insert  ignore into crew(tconst, nconst, job)
            values(%s, %s, 'writer')"""],
        ['name.basics.tsv/data.tsv', """insert  ignore into primaryprofession(nconst, profession)
            values(%s, %s)"""],
        ['title.crew.tsv/data.tsv', """insert  ignore into crew(tconst, nconst, job)
            values(%s, %s, 'director')"""]
    ]
    tableNames = ['genre', 'knownfortitle', 'crew writer',
                  'primaryprofession', 'crew director']

    conn = pymysql.connect(host='localhost', user='db2021',
                           password='db2021', db='IMDb')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    for idx in range(len(commands)):
        filename = commands[idx][0]
        insert_sql = commands[idx][1]
        f = open(filename, 'rt', encoding='UTF8')

        oneline = f.readline()
        oneline = f.readline()[:-1]
        rows = []
        i = 0
        if idx <= 2:
            flag = -1  # genre, knownfortitle,crew writer
        else:
            flag = -2  # primaryprofession, crew director
        while oneline:
            attrs_list = oneline.split('\t')
            if attrs_list[flag] != '//N':
                for data in attrs_list[flag].split(','):
                    attrs = [attrs_list[0], data]
                    rows.append(attrs)
                    i += 1
                    if i % 20000 == 0:
                        cur.executemany(insert_sql, rows)
                        conn.commit()
                        rows = []
                        print("%d rows" % i)

            oneline = f.readline()[:-1]
        if rows:
            cur.executemany(insert_sql, rows)
            conn.commit()
            print("%d rows" % i)

        f.close()
        print('Insert data into ', tableNames[idx], ' completed!')

    cur.close()
    conn.close()


if __name__ == '__main__':
    create_tables()
    load_data_from_file1()
    nomalization()
