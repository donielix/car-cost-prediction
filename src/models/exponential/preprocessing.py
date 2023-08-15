from typing import List

import pandas as pd
from sklearn.base import TransformerMixin


class ColumnDropperTransformer(TransformerMixin):
    def __init__(self, columns: List[str]):
        self.columns = columns

    def transform(self, X: pd.DataFrame, y=None):
        return X.drop(columns=self.columns, errors="ignore")

    def fit(self, X: pd.DataFrame, y=None):
        return self
