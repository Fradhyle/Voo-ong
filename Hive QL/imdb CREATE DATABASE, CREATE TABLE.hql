DROP DATABASE IF EXISTS `imdb` CASCADE;

CREATE DATABASE `imdb`;

CREATE TABLE `imdb`.`genres` (
      `genre_id` INT
    , `genre_name` STRING
);

CREATE TABLE `imdb`.`name_basics` (
      `nconst` STRING
    , `primaryName` STRING
    , `birthYear` INT
    , `deathYear` INT
    , `primaryProfession` STRING
    , `knownForTitles` STRING
    , `nconst_int` INT
);

CREATE TABLE `imdb`.`professions` (
      `prof_id` INT
    , `prof_name` STRING
);

CREATE TABLE `imdb`.`title_akas` (
      `titleId` STRING
    , `ordering` INT
    , `title` STRING
    , `region` STRING
    , `language` STRING
    , `types` STRING
    , `attributes` STRING
    , `isOriginalTitle` INT
    , `titleId_int` INT
);

CREATE TABLE `imdb`.`title_basics` (
      `tconst` STRING
    , `titleType` STRING
    , `primaryTitle` STRING
    , `originalTitle` STRING
    , `isAdult` INT
    , `startYear` INT
    , `endYear` INT
    , `runtimeMinutes` INT
    , `genres` STRING
    , `tconst_int` INT
);

CREATE TABLE `imdb`.`title_crew` (
      `tconst` STRING
    , `directors` STRING
    , `writers` STRING
    , `tconst_int` INT
);

CREATE TABLE `imdb`.`title_episode` (
      `tconst` STRING
    , `parentTconst` STRING
    , `seasonNumber` INT
    , `episodeNumber` INT
    , `tconst_int` INT
);