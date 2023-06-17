import pandas as pd
import pickle
from surprise import SVD
from surprise import Dataset, Reader


df = pd.read_csv('./ml-latest-small/ratings.csv')

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

model = SVD(n_factors=50, biased=False)
model.fit(data.build_full_trainset())

with open('svd_model.pkl', 'wb') as f:
    pickle.dump(model, f)