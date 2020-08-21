from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from pyhive import hive
from sqlalchemy import create_engine
from tqdm import tqdm
import os
import numpy as np
import pandas as pd


def ratings_aggregator(func_args):
    user_id = func_args[0]
    movies_genres_onehot = func_args[1]
    ratings_df = func_args[2]
    # hive_cnx = hive.Connection(host='hd02.pdmnu.com', username='sweetbarrow', database='mlens', auth='NOSASL')
    # ratings_df = pd.read_sql(f'SELECT * FROM mlens.ratings_rescaled WHERE user_id = {user_id}', hive_cnx)
    # ratings_df.rename(
    #     columns={
    #         'ratings_rescaled.user_id': 'user_id'
    #         , 'ratings_rescaled.movie_id': 'movie_id'
    #         , 'ratings_rescaled.rating_rescaled': 'rating'
    #     }
    #     , inplace=True
    # )
    genres_columns = [
        'action', 'adventure', 'animation'
        , 'children', 'comedy', 'crime'
        , 'documentary', 'drama', 'fantasy'
        , 'film_noir', 'horror', 'imax'
        , 'musical', 'mystery', 'romance'
        , 'sci_fi', 'thriller', 'war', 'western'
    ]
    temp_df = pd.DataFrame(
        np.zeros((1, 20), dtype=int)
        , columns=[
            'user_id', 'action', 'adventure'
            , 'animation', 'children', 'comedy'
            , 'crime', 'documentary', 'drama'
            , 'fantasy', 'film_noir', 'horror'
            , 'imax', 'musical', 'mystery', 'romance'
            , 'sci_fi', 'thriller', 'war', 'western'
            ]
        )
    temp_df.at[0, 'user_id'] = user_id
    df_range = range(len(ratings_df))
    # t = tqdm(total=len(ratings_df), desc=f'PID {os.getpid()} Job Progress')
    for index in df_range:
        movie_id = ratings_df.at[index, 'movie_id']
        rating = ratings_df.at[index, 'rating']
        if rating == 1:
            for genre in genres_columns:
                temp_df.at[0, genre] += movies_genres_onehot[movies_genres_onehot['movie_id'] == movie_id][genre]
        elif rating == -1:
            for genre in genres_columns:
                temp_df.at[0, genre] -= movies_genres_onehot[movies_genres_onehot['movie_id'] == movie_id][genre]
        # t.update(1)
    # t.close()
    print(f'User {user_id} Aggregating Completed!')
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mysql_cnx = create_engine('mysql+pymysql://root:!panda8902@pc.pdmnu.com:3306/mlens?charset=utf8mb4', encoding='utf-8')
        temp_df.to_sql('ratings_genres', mysql_cnx, if_exists='append', index=False)
        return


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

        ratings_rescaled = pd.read_sql(f'SELECT * FROM mlens.ratings_rescaled', hive_cnx)
        ratings_rescaled.rename(
            columns={
                'ratings_rescaled.user_id': 'user_id'
                , 'ratings_rescaled.movie_id': 'movie_id'
                , 'ratings_rescaled.rating_rescaled': 'rating'
            }
            , inplace=True
        )

        mysql_cnx = create_engine('mysql+pymysql://root:!panda8902@pc.pdmnu.com:3306/mlens?charset=utf8mb4', encoding='utf-8')

        count_users = pd.read_sql('SELECT COUNT(DISTINCT user_id) FROM mlens.ratings_rescaled', hive_cnx)
        total_users = count_users.loc[0, '_c0']
        print('Total users count:', total_users)
        print()

        movies_genres_onehot = pd.read_sql('SELECT * FROM mlens.movies_genres_onehot', hive_cnx)
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
        movies_genres_onehot.sort_values('movie_id', inplace=True, ignore_index=True)
        movies_genres_onehot.drop('title', axis=1, inplace=True)
        print(movies_genres_onehot.head())
        print()

        total_tqdm = tqdm(total=total_users, desc='Total Progress')
        queue_tqdm = tqdm(total=total_users, desc='Job Submitting Progress')

        futures = []
        results = []
        func_args = ((user_id, movies_genres_onehot, ratings_rescaled[ratings_rescaled['user_id'] == user_id]) for user_id in range(1, total_users + 1))

        with ProcessPoolExecutor(32) as executor:
            for i in func_args:
                future = executor.submit(ratings_aggregator, i)
                futures.append(future)
                queue_tqdm.update(1)
            for i in as_completed(futures):
                # results.append(i.result())
                total_tqdm.update(1)

        queue_tqdm.close()
        total_tqdm.close()
        # result_df = pd.concat(results)
        # mysql_cnx = create_engine('mysql+pymysql://root:!panda8902@pc.pdmnu.com:3306/mlens?charset=utf8mb4', encoding='utf-8')
        # result_df.to_sql('ratings_genres', mysql_cnx, if_exists='append', index=False)

        print('All done! :)')
        exit()
    except KeyboardInterrupt:
        print(results)
        print('Keyboard interrupt detected. Unexpected program stop. :(')
    except OSError as ose:
        print(ose)
        print('OSError')
    except SystemExit:
        print('Bye! :)')
