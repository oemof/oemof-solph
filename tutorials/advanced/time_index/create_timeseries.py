import pandas as pd


def reshape_unevenly(df):

    def to_bucket(ts: pd.Timestamp) -> pd.Timestamp:
        h = ts.hour
        d = ts.normalize()
        if 6 <= h <= 21:
            return ts
        if h in (22, 23):
            return d + pd.Timedelta(hours=22)
        if h in (0, 1):
            return (d - pd.Timedelta(days=1)) + pd.Timedelta(hours=22)
        # h in (2, 3, 4, 5)
        return d + pd.Timedelta(hours=2)

    buckets = df.index.map(to_bucket)
    buckets = buckets.where(buckets >= df.index[0], df.index[0])

    df_mean = df.groupby(buckets).mean().sort_index()
    # df_sum = df.groupby(buckets).sum().sort_index()
    df_mean.index.name = 'timestamp'
    # df_sum.index.name = 'timestamp'

    return df_mean
