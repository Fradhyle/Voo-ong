DROP DATABASE IF EXISTS `mlens` CASCADE;

CREATE DATABASE `mlens`;

CREATE TABLE `mlens`.`genome_scores` (
      `movieId` INT
    , `tagId` INT
    , `relevance` DOUBLE
);

CREATE TABLE `mlens`.`genome_tags` (
      `tagId` INT
    , `tag` STRING
);

CREATE TABLE `mlens`.`genres` (
      `genre_id` INT
    , `genre_name` STRING
);

CREATE TABLE `mlens`.`links` (
      `movieId` INT
    , `imdbId` INT
    , `tmdbId` INT
);

-- `mlens`.`movies`의 CREATE TABLE 문은 INSERT INTO 쿼리 파일과 합쳤음

CREATE TABLE `mlens`.`ratings` (
      `userId` INT
    , `movieId` INT
    , `rating` FLOAT
    , `timestamp` INT
);

CREATE TABLE `mlens`.`tags` (
      `userId` INT
    , `movieId` INT
    , `tag` STRING
    , `timestamp` INT
);