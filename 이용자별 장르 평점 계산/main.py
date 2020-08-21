from concurrent.futures import ProcessPoolExecutor, as_completed
from pyhive import hive
from sqlalchemy import create_engine
from tqdm import tqdm
import os
import numpy as np
import pandas as pd

def ratings_aggregator(func_args):
    genres_columns = [
        'action', 'adventure', 'animation'
        , 'children', 'comedy', 'crime'
        , 'documentary', 'drama', 'fantasy'
        , 'film_noir', 'horror', 'imax'
        , 'musical', 'mystery', 'romance'
        , 'sci_fi', 'thriller', 'war', 'western'
        ]
    rating_df = func_args[0]
    movies_genres_onehot_new = func_args[1]
    index = func_args[2]
    temp_df = pd.DataFrame(np.zeros((1, 22), dtype=int)
    , columns=[
        'user_id', 'movie_id', 'rating_rescaled'
        , 'action', 'adventure', 'animation'
        , 'children', 'comedy', 'crime'
        , 'documentary', 'drama', 'fantasy'
        , 'film_noir', 'horror', 'imax'
        , 'musical', 'mystery', 'romance'
        , 'sci_fi', 'thriller', 'war', 'western'
        ])
    user_id = rating_df.at[index, 'user_id']
    movie_id = rating_df.at[index, 'movie_id']
    rating = rating_df.at[index, 'rating_rescaled']
    temp_df.at[0, 'user_id'] = user_id
    temp_df.at[0, 'movie_id'] = movie_id
    temp_df.at[0, 'rating_rescaled'] = rating
    if rating == 1:
        for genre in genres_columns:
            temp_df.at[0, genre] += movies_genres_onehot_new[movies_genres_onehot_new['movie_id'] == movie_id][genre]
    elif rating == -1:
        for genre in genres_columns:
            temp_df.at[0, genre] -= movies_genres_onehot_new[movies_genres_onehot_new['movie_id'] == movie_id][genre]
    return temp_df


if __name__ == '__main__':
    try:
        hive_cnx = hive.Connection(
            host='hd02.pdmnu.com'
            , username='sweetbarrow'
            , database='mlens'
            , auth='NOSASL'
        )
        print(hive_cnx)
        print()

        mysql_cnx = create_engine('mysql+pymysql://root:!panda8902@pc.pdmnu.com:3306/mlens', echo=True)
        print(mysql_cnx)
        print()

        ratings_rescaled = pd.read_sql('SELECT * FROM mlens.ratings_rescaled', hive_cnx)
        ratings_rescaled.rename(
            columns={
                'ratings_rescaled.user_id': 'user_id'
                , 'ratings_rescaled.movie_id': 'movie_id'
                , 'ratings_rescaled.rating_rescaled': 'rating_rescaled'
            }
            , inplace=True
        )
        print(ratings_rescaled.head())
        print()    

        movies_genres_onehot = pd.read_sql('SELECT * FROM mlens.movies_genres_onehot', hive_cnx)
        print(movies_genres_onehot.head())
        print()

        new_columns = {
            'movies_genres_onehot.movie_id': 'movie_id'
            , 'movies_genres_onehot.title': 'title'
            , 'movies_genres_onehot.action': 'action'
            , 'movies_genres_onehot.adventure': 'adventure'
            , 'movies_genres_onehot.animation': 'animation'
            , 'movies_genres_onehot.children': 'children'
            , 'movies_genres_onehot.comedy': 'comedy'
            , 'movies_genres_onehot.crime': 'crime'
            , 'movies_genres_onehot.documentary': 'documentary'
            , 'movies_genres_onehot.drama': 'drama'
            , 'movies_genres_onehot.fantasy': 'fantasy'
            , 'movies_genres_onehot.film_noir': 'film_noir'
            , 'movies_genres_onehot.horror': 'horror'
            , 'movies_genres_onehot.imax': 'imax'
            , 'movies_genres_onehot.musical': 'musical'
            , 'movies_genres_onehot.mystery': 'mystery'
            , 'movies_genres_onehot.romance': 'romance'
            , 'movies_genres_onehot.sci_fi': 'sci_fi'
            , 'movies_genres_onehot.thriller': 'thriller'
            , 'movies_genres_onehot.war': 'war'
            , 'movies_genres_onehot.western': 'western'
        }

        movies_genres_onehot.rename(columns=new_columns, inplace=True)
        print(movies_genres_onehot.head())
        print()

        movies_genres_onehot.sort_values('movie_id', inplace=True, ignore_index=True)
        print(movies_genres_onehot.head())
        print()

        movies_genres_onehot_new = movies_genres_onehot.drop('title', axis=1)
        print(movies_genres_onehot_new.head())
        print()

        genres_columns = []
        for _ in movies_genres_onehot_new.columns:
            if _ == 'movie_id':
                pass
            else:
                genres_columns.append(_)
        print(genres_columns)
        print()

        genres_columns_df = pd.DataFrame(columns=genres_columns)
        print(genres_columns_df.head())
        print()

        genres_ratings_df = pd.DataFrame(ratings_rescaled)
        print(genres_ratings_df.head())
        print()

        genres_ratings_df = pd.merge(genres_ratings_df, genres_columns_df, how='left', left_index=True, right_index=True)
        genres_ratings_df.fillna(0, inplace=True)
        print(genres_ratings_df.head())
        print()        

        df_length = len(ratings_rescaled)
        
        result_df = pd.DataFrame(columns=genres_ratings_df.columns)
        results = []

        start_point = 0
        finish_point = 10000
        tqdm_length = len(range(start_point, finish_point))
        total_tqdm = tqdm(total=df_length, desc='Total Progress')
        t_obj = tqdm(total=tqdm_length, desc='Job Scheduling Progress')
        tqdm_obj = tqdm(total=tqdm_length, desc='Aggregating Progress')

        while True:
            futures = []
            func_args = ((ratings_rescaled.loc[[index]], movies_genres_onehot_new, index) for index in range(start_point, finish_point))
            with ProcessPoolExecutor(61) as executor:                          
                for i in func_args:
                    future = executor.submit(ratings_aggregator, i)
                    futures.append(future)
                    t_obj.update(1)
                for i in as_completed(futures):
                    results.append(i.result()) 
                    tqdm_obj.update(1)
                    total_tqdm.update(1)
            if finish_point < df_length:
                start_point += finish_point
                finish_point += 10000
                if finish_point > df_length:
                    finish_point = df_length + 1
                    tqdm_length = len(range(start_point, finish_point))
                    t_obj.reset(total=tqdm_length)
                    tqdm_obj.reset(total=tqdm_length)
                    continue
                else:
                    tqdm_length = len(range(start_point, finish_point))
                    t_obj.reset(total=tqdm_length)
                    tqdm_obj.reset(total=tqdm_length)
                    continue
                continue
            elif finish_point > df_length:
                t_obj.close()
                tqdm_obj.close()
                total_tqdm.close()
                break

        result_df = pd.concat(results, ignore_index=True)
                
        result_df.drop('movie_id', axis=1, inplace=True)
        result_df.drop('rating_rescaled', axis=1, inplace=True)
        result_df.sort_values('user_id', inplace=True, ignore_index=True)
        result_df = result_df.groupby('user_id').sum()

        print(result_df.head())
        print()

        input('Press any key to continue. MySQL INSERT is waiting')
        result_df.to_sql('ratings_genres', mysql_cnx, if_exists='append')
    except KeyboardInterrupt:
        result_df = pd.concat(results, ignore_index=True)
                
        result_df.drop('movie_id', axis=1, inplace=True)
        result_df.drop('rating_rescaled', axis=1, inplace=True)
        result_df.sort_values('user_id', inplace=True, ignore_index=True)
        result_df = result_df.groupby('user_id').sum()

        print(result_df.head())
        print()

        input('Press any key to continue. MySQL INSERT is waiting')
        result_df.to_sql('ratings_genres', mysql_cnx, if_exists='append')
