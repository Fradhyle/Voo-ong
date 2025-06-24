DROP TABLE IF EXISTS `mlens`.`movies_genres_onehot`;

CREATE TABLE `mlens`.`movies_genres_onehot` (
    `movie_id` INT
  ,  `title` STRING
  ,  `action` INT
  ,  `adventure` INT
  ,  `animation` INT
  ,  `children` INT
  ,  `comedy` INT
  ,  `crime` INT
  ,  `documentary` INT
  ,  `drama` INT
  ,  `fantasy` INT
  ,  `film_noir` INT
  ,  `horror` INT
  ,  `imax` INT
  ,  `musical` INT
  ,  `mystery` INT
  ,  `romance` INT
  ,  `sci_fi` INT
  ,  `thriller` INT
  ,  `war` INT
  ,  `western` INT
);