import plotly.express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import plotly.graph_objects as go
import streamlit as st
df = pd.read_csv('data/average_dose.csv')

st.title('Dose Response Curve')

name1 = st.selectbox('Choose Drug 1', set(df['Name1']))

data1 = df[df['Name1'] == name1]
name2 = st.selectbox('Choose Drug 2', set(data1['Name2']))
st.write('Drug1 you selected is:', name1)
st.write('Drug2 you selected is:', name2)
#
#
#name1 = 'Lenalidomide_1'
#name2 = 'EPZ-5676_2'
data2 = data1[data1['Name2'] == name2]

#experiment = 'MOM14_ASSAY_ID_8872'
experiment = st.selectbox('Choose Experiment', set(data2['Experiment']))

st.write('Experiment you selected is:', experiment)
df1 =data2[data2['Experiment'] == experiment]

#dose response plot
drug1_min = df1[df1['Name'] == name1].Drug.min()
drug1_max = df1[df1['Name'] == name1].Drug.max()
glm_model1 = smf.glm('Average ~ Drug', df1[df1['Name'] == name1], family=sm.families.Binomial()).fit()

X1 = np.linspace(drug1_min,drug1_max,100)
Y1 = glm_model1.predict(exog=dict(Drug=X1))


drug2_min = df1[df1['Name'] == name2].Drug.min()
drug2_max = df1[df1['Name'] == name2].Drug.max()
glm_model2 = smf.glm('Average ~ Drug', df1[df1['Name'] == name2], family=sm.families.Binomial()).fit()

X2 = np.linspace(drug2_min,drug2_max,100)
Y2 = glm_model2.predict(exog=dict(Drug=X2))

from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols = 2)
fig.add_trace(go.Scatter(x=df1[df1['Name'] == name1]['Drug'], y = df1[df1['Name'] == name1]['Average'], mode = 'markers', marker_color='red'), row=1, col=1)
fig.add_trace(go.Scatter(x=X1, y=Y1, marker_color='red',name=name2), row=1, col=1)
fig.add_trace(go.Scatter(x=df1[df1['Name'] == name2]['Drug'], y = df1[df1['Name'] == name2]['Average'], mode = 'markers', marker_color='blue'), row=1, col=2)
fig.add_trace(go.Scatter(x=X2, y=Y2, marker_color='blue', name=name1), row=1, col=2)
fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
