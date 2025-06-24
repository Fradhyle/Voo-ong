DROP DATABASE IF EXISTS `movielens` CASCADE;

CREATE DATABASE `movielens`;

-- MovieLens에서 제공하는 데이터셋을 저장하는 테이블 생성

-- ratings.csv
-- 평점은 0.5점부터 0.5점 단위로 만점은 5.0점
-- 타임스탬프는 1970년 1월 1일 00:00:00 UTC부터의 초 단위로 저장
CREATE TABLE `movielens`.`ratings` (
      `userId` INT
    , `movieId` INT
    , `rating` FLOAT
    , `timestamp` INT
);

-- tags.csv
-- 태그는 사용자가 영화에 대해 작성한 텍스트
-- 타임스탬프는 1970년 1월 1일 00:00:00 UTC부터의 초 단위로 저장
CREATE TABLE `movielens`.`tags` (
      `userId` INT
    , `movieId` INT
    , `tag` STRING
    , `timestamp` INT
);

-- movies.csv
-- The Movie Database에서 제공하는 영화 제목과 장르 이름을 가진다.
CREATE TABLE `movielens`.`movies` (
      `movieId` INT
    , `title` STRING
    , `genres` STRING
);

-- links.csv
-- movies.csv의 movieId를 기준으로 IMDb의 데이터와 The Movie Database의 데이터를 연결한다.
CREATE TABLE `movielens`.`links` (
      `movieId` INT
    , `imdbId` INT
    , `tmdbId` INT
);

-- Tag Genome
-- genome-scores.csv, genome-tags.csv
-- tag genome은 영화에 대한 태그의 관련성을 포함하는 데이터 구조이다.
-- 이 구조는 밀집행렬 구조로 각 영화는 모든 태그에 대한 게놈 값을 가진다.
-- http://files.grouplens.org/papers/tag_genome.pdf
CREATE TABLE `movielens`.`genome_scores` (
      `movieId` INT
    , `tagId` INT
    , `relevance` DOUBLE
);
CREATE TABLE `movielens`.`genome_tags` (
      `tagId` INT
    , `tag` STRING
);