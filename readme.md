# IMDB 검색 응용프로그램

- **기술스택**: MySQL, Python3
- tsv(tab-separated-values) dataset을 파이썬 응용프로그램으로 파싱하여 DB 구축
- 개념 데이터 모델링(E/R 모델 설계), 논리 데이터 모델링(RDB 테이블 설계)수행
- 검색 응용 프로그램 구현
- 인덱스 생성을 통해 쿼리성능 평균 200배 향상

## 파일구성

- make_db.py : 파일로 부터 db 구성
- IMDbSearch.py: 검색 응용프로그램

## 주요 코드 설명

### 함수

- def conv(attr):’\\N’로 표시된 값을 None값으로 변경
- def create_tables():테이블 생성
- def load_data_from_file1():정규화가 필요없는 테이블에 데이터 삽입
- def nomalization():정규화가 필요한 테이블에 데이터 삽입

### def nomalization()

```python
if idx <= 2:
            flag = -1  # genre, knownfortitle,crew writer
        else:
            flag = -2  # primaryprofession, crew director
        while oneline:
            attrs_list = oneline.split('\t')
            if attrs_list[flag] != '//N':
                for data in attrs_list[flag].split(','):
                    attrs = [attrs_list[0], data]
                    rows.append(attrs)
                    i += 1
                    if i % 20000 == 0:
                        cur.executemany(insert_sql, rows)
                        conn.commit()
                        rows = []
                        print("%d rows" % i)
            oneline = f.readline()[:-1]

```

## 주요 SQL

- 영화 제목을 입력하여, 이에 매칭되는 영화를 검색:

```sql
select * from movie where primaryTitle = ‘%s’;
```

- 특정 배우가 등장하는 영화를 별점이 높은 순으로 검색:

```sql
select m.primarytitle, r.averageRating from movie m, review r, person p, principal pp where m.tconst=pp.tconst and m.tconst=r.tconst and p.nconst = pp.nconst and p.primaryName=%s' order by  r.averageRating desc;
```

- 특정 감독이 제작한 영화를 개봉연도순으로 검색:

```sql
select m.primarytitle, m.startYear from movie m, crew c, person p where m.tconst=c.tconst and c.nconst = p.nconst and c.job="director" and p.primaryName=“%s" order by m.startYear;
```

- Drama 장르의 영화를 리뷰가 많은 순 또는 별점이 높은 순으로 검색:

```sql
select m.primaryTitle, g.genre, r.averageRating, r.numVotes from movie m, genre g, review r where m.tconst = g.tconst and m.tconst=r.tconst and g.genre='Drama' order by r.numVotes desc limit 30;
select m.primaryTitle, g.genre, r.averageRating from movie m, genre g, review r where m.tconst = g.tconst and m.tconst=r.tconst and g.genre='Drama' order by r.averageRating desc limit 30;
```

- 특정 영화의 지역별 이름을 검색:

```sql
select l.region, l.title from movie m, localtitleinfo l where m.tconst = l.titleid and m.primarytitle=‘%s';
```

## 인덱스 생성

- SQL문의 WHERE 절을 참고하여 인덱스 지정

```sql
create index idx_primaryTitle on movie(primaryTitle)
create index idx_primaryName on person(primaryName)
create index idx_nconst_principal on principal(nconst)
create index idx_tconst_crew on crew(tconst)
create index idx_titleId on localtitlinfo(titleId)
```

=> 쿼리 성능 평균 200배 향상
