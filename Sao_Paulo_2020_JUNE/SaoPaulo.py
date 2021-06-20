import pandas as pd 
from pandas_ods_reader import read_ods
import statsmodels.api as sm
import numpy as np

raw = read_ods('SaoPauloSP.ods', 1, headers=1)
df = pd.DataFrame()

df['Subprefeitura'] = raw['Subprefeitura']
df['Density'] = raw['Hab/km^2']
df['Income'] = raw['Renda Media (R$)']
df['Preto/Pardo'] = raw['Populacao negra']
df['Cases per 1k'] = raw['Casos por 1k']
df['Death Rate'] = raw['Taxa de Morte (por cem)']
df['HDI'] = raw['IDH']

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        if feature_name in ['Subprefeitura', 'Cases per 1k', 'Death Rate']:
            result[feature_name] = df[feature_name]
        else:
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

df = normalize(df)
X = df[['Preto/Pardo', 'HDI']]
Y1 = df['Cases per 1k']
# X = sm.add_constant(X) 
model = sm.OLS(Y1, X).fit()
predictions = model.predict(X) 

print_model = model.summary()
print(print_model)

Y2 = df['Death Rate']
model = sm.OLS(Y2, X).fit()
predictions = model.predict(X) 

print_model = model.summary()
print(print_model)