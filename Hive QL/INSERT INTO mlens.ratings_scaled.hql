DROP TABLE IF EXISTS `mlens`.`ratings_scaled`;


CREATE TABLE `mlens`.`ratings_scaled` (
      `user_id` INT
    , `movie_id` INT
    , `scaled_rating` DOUBLE
);