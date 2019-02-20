import pandas as pd


def scaler(data):
    numerator = data - data.min(axis=0)
    denominator = data.max(axis=0) - data.min(axis=0)
    return numerator / (denominator + 1e-7)

