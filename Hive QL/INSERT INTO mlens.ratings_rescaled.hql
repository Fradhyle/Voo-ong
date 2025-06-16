DROP TABLE IF EXISTS `mlens`.`ratings_rescaled`;

CREATE TABLE `mlens`.`ratings_rescaled` (
      `user_id` INT
    , `movie_id` INT
    , `rescaled_rating` INT
);