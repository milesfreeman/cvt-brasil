import pandas as pd 
import numpy as np 
import statsmodels.api as sm
from scipy import stats

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        if feature_name in ['Casos (por 1k)', 'obitos percapita', 'Município']:
            result[feature_name] = df[feature_name]
        else:
            # max_value = df[feature_name].max()
            # min_value = df[feature_name].min()
            # result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
            result[feature_name] = (df[feature_name] - df[feature_name].mean())/df[feature_name].std(ddof=0)
    return result

# --------------------------------------------------------------------------------------------------------------------------------------------------
# 1. Demografics per municipality

with open('Minas_Gerais.csv', 'r') as f:
    demografics = pd.read_csv(f)

demografics = demografics[['Município', 'Population Estimate -  [2020]', 'Densidade – hab/km^2 [2010]', 'MHDI (Municipal human development index) [2010]',
                    'GDP Per Capita - R$ (*1000) [2017]']]


# 2. Covid cases 11 Nov

with open('Minas_Gerais_boletim.txt', 'r') as f:
    lines = f.readlines()
covid = pd.DataFrame(columns=['Município', 'Casos', 'Obitos'])
for line in lines:
    x = line.split()
    x = ['0' if y == '-' else y for y in x]
    if x[0] =='#' : break 
    
    i = 0
    while i < len(x) - 2:
        nome = []
        while ord(x[i][0]) not in range(0x30, 0x3a):
            nome.append(x[i])
            i += 1
        cdd  = " ".join(nome)
        casos = int(x[i])
        mortes = int(x[i+1])
        dados = {'Município': cdd, 'Casos': casos, 'Obitos': mortes}
        covid = covid.append(dados, ignore_index=1)
        i += 2

joint = covid.merge(demografics, on='Município', how='left')
# joint = joint.loc[(joint=='-').any(axis=1)]

joint['Casos (por 1k)'] = 1000* joint['Casos'] / joint['Population Estimate -  [2020]']
joint['obitos percapita'] = 1000* joint['Obitos'] / joint['Population Estimate -  [2020]']

# --------------------------------------------------------------------------------------------------------------------------------------------------

joint = joint.drop(853, axis=0).dropna()
# indices = joint['Município' in ['Araporã', 'Extrema']].indices
joint = joint[joint.Município != 'Araporã']
joint = joint[joint.Município != 'Extrema']
joint = joint[joint.Município != 'Olímpio Noronha']
joint = joint[joint.Município != 'Uberaba']
joint = joint[joint.Município != 'Itaverava']
joint = joint[joint.Município != 'Virgínia']

n_joint = normalize(joint)
n_joint.rename(inplace=1, columns= {'Densidade – hab/km^2 [2010]' : 'Densidade (hab/km^2)', 'MHDI (Municipal human development index) [2010]' :'IDH (2010)', 'GDP Per Capita - R$ (*1000) [2017]' : 'GDP per capita R$'})
joint.rename(inplace=1, columns= {'Densidade – hab/km^2 [2010]' : 'Densidade (hab/km^2)', 'MHDI (Municipal human development index) [2010]' :'IDH (2010)', 'GDP Per Capita - R$ (*1000) [2017]' : 'GDP per capita R$'})
X = joint[['Densidade (hab/km^2)', 'IDH (2010)']]
print(n_joint)
Y = joint['Casos (por 1k)']

# for i, y in enumerate(Y):
#     if y > 60 : 
#         print(joint['Município'][i])
# for i, x in enumerate(X['GDP per capita R$']):
#     if x > 0.8 : 
#         print(joint['Município'][i])

# --------------------------------------------------------------------------------------------------------------------------------------------------

X = sm.add_constant(X) 
model = sm.GLS(Y.astype(float), X.astype(float)).fit()
predictions = model.predict(X) 

print_model = model.summary()
print(print_model)

import matplotlib.pyplot as plt
fig = plt.figure()
plotX = np.asarray(joint['IDH (2010)'].iloc[1:])
plotY = np.asarray(Y.iloc[1:])
plt.scatter(plotX, plotY, s=40, c=joint['Densidade (hab/km^2)'][1:], cmap='viridis')
plt.colorbar(label='Densidade (hab/km^2)')
plt.xlabel('IDH (2010)')
plt.ylabel('Casos confirmados por 1k')
for i, name in enumerate(joint['Município']):
    if name in ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora']:
        plt.text(plotX[i], plotY[i], name, c='r')
plt.plot([0.4757, 0.85], [0, 21.273864], c='r')
plt.title("Minas Gerais: casos vs. IDH")
plt.show()