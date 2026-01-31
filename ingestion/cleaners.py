def deduplicate(df, key_columns):
    return df.drop_duplicates(subset = key_columns)