DROP TABLE IF EXISTS `voo_ong`.`genres`;

CREATE TABLE `voo_ong`.`genres` (
      `genre_id` INT
    , `imdb_genre_id` INT
    , `mlens_genre_id` INT
    , `naver_genre_id` INT
    , `genre_name_ko` STRING
    , `genre_name_en` STRING
);

INSERT INTO `voo_ong`.`genres`
VALUES
  (0, 0, 0, 0, NULL, NULL)
, (1, 1, 1, 19, '액션', 'Action')
, (2, 2, NULL, 21, '성인', 'Adult')
, (3, 3, 2, 6, '모험', 'Adventure')
, (4, 4, 3, 15, '애니메이션', 'Animation')
, (5, 5, NULL, NULL, '전기 영화', 'Biography')
, (6, 6, 5, 11, '코미디', 'Comedy')
, (7, 7, 6, 16, '범죄', 'Crime')
, (8, 8, 7, 10, '다큐멘터리', 'Documentary')
, (9, 9, 8, 1, '드라마', 'Drama')
, (10, 10, NULL, 12, '가족', 'Family')
, (11, 11, 9, 2, '판타지', 'Fantasy')
, (12, 12, 10, 8, '느와르', 'Film Noir')
, (13, 13, NULL, NULL, '게임쇼', 'Game Show')
, (14, 14, NULL, NULL, '역사', 'History')
, (15, 15, 11, 4, '공포', 'Horror')
, (16, 16, NULL, NULL, '음악', 'Music')
, (17, 17, 13, 17, '뮤지컬', 'Musical')
, (18, 18, 14, 13, '미스터리', 'Mystery')
, (19, 19, NULL, NULL, '뉴스', 'News')
, (20, 20, NULL, NULL, '리얼리티 TV', 'Reality TV')
, (21, 21, 15, 5, '로맨스', 'Romance')
, (22, 22, 16, 18, '공상과학', 'Sci-Fi')
, (23, 23, NULL, NULL, '단편', 'Short')
, (24, 24, NULL, NULL, '스포츠', 'Sport')
, (25, 25, NULL, NULL, '토크 쇼', 'Talk Show')
, (26, 26, 17, 7, '스릴러', 'Thriller')
, (27, 27, 18, 14, '전쟁', 'War')
, (28, 28, 19, 3, '서부', 'Western')
, (29, NULL, 4, NULL, '아동', 'Children')
, (30, NULL, 12, NULL, 'IMAX', 'IMAX')
, (31, NULL, NULL, 9, '컬트', 'Cult')
, (32, NULL, NULL, 20, '무협', 'Martial Arts')
, (33, NULL, NULL, 22, '서스펜스', 'Suspense')
, (34, NULL, NULL, 23, '서사 영화', 'Epic Film')
, (35, NULL, NULL, 24, '블랙 코미디', 'Black Comedy')
, (36, NULL, NULL, 25, '실험', 'Experimental Film')
, (37, NULL, NULL, 29, '공연실황', 'Live Performance')
;