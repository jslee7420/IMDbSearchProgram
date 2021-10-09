import os
import pymysql
import time
# John Belushi


class Search:
    """
    검색 클래스
    각 메뉴를 메소드로 구현
    """

    def __init__(self):  # 생성자
        self.conn = pymysql.connect(  # 커넥션 생성
            host='localhost', user='db2021', password='db2021', db='IMDb')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)  # 커서 생성
        pass

    def __del__(self):  # 소멸자
        self.curs.close()  # 커서 닫기
        self.conn.close()  # 커넥션 닫기
        pass

    def menu1(self):
        """
        메뉴1: 제목으로 영화 검색
        """
        os.system('cls')
        print('---------------제목으로 영화 검색---------------')
        self.title = input('\n영화 제목을 입력해주세요: ')
        self.start_time = time.time()
        # 제목이 일치하는 영화 정보 출력
        self.sql = f'SELECT * FROM movie WHERE primaryTitle="{self.title}"'
        self.curs.execute(self.sql)
        self.elapsed_time = time.time() - self.start_time
        self.row = self.curs.fetchone()
        while self.row:
            print(self.row)
            self.row = self.curs.fetchone()

        print(self.elapsed_time, 'seconds')
        input('계속하려면 아무키나 눌러주세요')

    def menu2(self):
        """
        메뉴2: 배우로 영화 검색
        """
        os.system('cls')
        print('---------------배우로 영화 검색---------------')
        self.actor = input('\n배우 이름을 입력해주세요: ')
        self.start_time = time.time()
        self.sql = f'select m.primarytitle, r.averageRating from movie m, review r, person p, principal pp where m.tconst=pp.tconst and m.tconst=r.tconst and p.nconst = pp.nconst and p.primaryName="{self.actor}" order by  r.averageRating desc'
        self.curs.execute(self.sql)
        self.elapsed_time = time.time() - self.start_time
        self.row = self.curs.fetchone()
        while self.row:
            print(self.row)
            self.row = self.curs.fetchone()
        print(self.elapsed_time, 'seconds')
        input('계속하려면 아무키나 눌러주세요')

    def menu3(self):
        """
        메뉴3: 감독으로 영화 검색
        """
        os.system('cls')
        print('---------------감독으로 영화 검색---------------')
        self.director = input('\n감독 이름을 입력해주세요: ')
        self.start_time = time.time()

        self.sql = f'select m.primarytitle, m.startYear from movie m, crew c, person p where m.tconst=c.tconst and c.nconst = p.nconst and c.job="director" and p.primaryName="{self.director}" order by m.startYear'
        self.curs.execute(self.sql)
        self.elapsed_time = time.time() - self.start_time
        self.row = self.curs.fetchone()
        while self.row:
            print(self.row)
            self.row = self.curs.fetchone()
        print(self.elapsed_time, 'seconds')
        input('계속하려면 아무키나 눌러주세요')

    def menu4(self):
        """
        메뉴4: Drama 장르 영화 검색
        """
        os.system('cls')
        print('---------------Drama 장르 영화 검색---------------')
        print('1. 리뷰가 많은 순')
        print('2. 별점이 높은 순')
        self.choice = input('선택해주세요:')
        if self.choice == '1':
            self.sql = f'select m.primaryTitle, g.genre, r.averageRating, r.numVotes from movie m, genre g, review r where m.tconst = g.tconst and m.tconst=r.tconst and g.genre="Drama" order by r.numVotes desc limit 30;'
        elif self.choice == '2':
            self.sql = f'select m.primaryTitle, g.genre, r.averageRating from movie m, genre g, review r where m.tconst = g.tconst and m.tconst=r.tconst and g.genre="Drama" order by r.averageRating desc limit 30;'

        self.start_time = time.time()
        self.curs.execute(self.sql)
        self.elapsed_time = time.time() - self.start_time
        self.row = self.curs.fetchone()
        while self.row:
            print(self.row)
            self.row = self.curs.fetchone()
        print(self.elapsed_time, 'seconds')
        input('계속하려면 아무키나 눌러주세요')

    def menu5(self):
        """
        메뉴5: 과목 삭제
        """
        os.system('cls')
        print('---------------특정 영화의 지역별 이름 검색---------------')
        self.title = input('\n영화 제목을 입력해주세요: ')
        self.start_time = time.time()
        # 제목이 일치하는 영화 정보 출력
        self.sql = f'select l.region, l.title from movie m, localtitleinfo l where m.tconst = l.titleid and m.primarytitle="{self.title}"'
        self.curs.execute(self.sql)
        self.elapsed_time = time.time() - self.start_time
        self.row = self.curs.fetchone()
        while self.row:
            print(self.row)
            self.row = self.curs.fetchone()

        print(self.elapsed_time, 'seconds')
        input('계속하려면 아무키나 눌러주세요')


search = Search()  # 수강신청 클래스 인스턴스 생성

while True:  # 반복하여 기능 사용
    os.system('cls')
    print('------------IMDB 검색----------------')
    print('1. 제목으로 영화 검색')
    print('2. 배우로 영화 검색')
    print('3. 감독으로 영화 검색')
    print('4. Drama 장르 영화 검색')
    print('5. 특정 영화의 지역별 이름 검색')
    print()

    try:  # 예외처리
        menuInput = int(input('메뉴를 선택해주세요: '))  # 메뉴 번호 선택 저장
        if menuInput == 1:
            search.menu1()
        elif menuInput == 2:
            search.menu2()
        elif menuInput == 3:
            search.menu3()
        elif menuInput == 4:
            search.menu4()
        elif menuInput == 5:
            search.menu5()

    except Exception as e:  # 예외상황에 대한 메세지 출력
        print('잘못된 입력입니다.', e)
        input('계속하려면 아무키나 눌러주세요')
