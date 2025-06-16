DROP DATABASE IF EXISTS `naver_movie` CASCADE;

CREATE DATABASE `naver_movie`;

CREATE TABLE `naver_movie`.`genres` (
      `genre_id` INT
    , `genre_name` STRING
);

CREATE TABLE `naver_movie`.`main_actors` (
      `mi_code` INT
    , `pi_code` INT
    , `name_ko` STRING
    , `name_en` STRING
    , `main_role` INT
    , `role_name` STRING
);

CREATE TABLE `naver_movie`.`movie_basic` (
      `mi_code` INT
    , `title_ko` STRING
    , `title_i18n` STRING
    , `release_year` INT
    , `genres` STRING
    , `nation` STRING
);

CREATE TABLE `naver_movie`.`movie_staffs` (
      `mi_code` INT
    , `pi_code` INT
    , `name_ko` STRING
    , `name_en` STRING
    , `professions` STRING
);

CREATE TABLE `naver_movie`.`persons` (
      `pi_code` INT
    , `name_ko` STRING
    , `name_en` STRING
    , `name_i18n` STRING
    , `birth_date` STRING
    , `death_date` STRING
    , `birth_nation` STRING
    , `represent_movie` STRING
    , `aliases` STRING
);

-- `naver_movie`.`professions`의 CREATE TABLE 문은 INSERT INTO 쿼리 파일과 합쳤음

CREATE TABLE `naver_movie`.`sub_actors` (
      `mi_code` INT
    , `pi_code` INT
    , `actor_name` STRING
    , `role_name` STRING
);