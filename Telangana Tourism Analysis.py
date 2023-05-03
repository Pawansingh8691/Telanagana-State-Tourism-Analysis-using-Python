#!/usr/bin/env python
# coding: utf-8

# In[45]:


import pandas as pd
import numpy as np
import plotly.express as px


# In[2]:


# merging all domestic visitors csv files in one pandas dataframe


# In[543]:


domestic_data = pd.concat(map(pd.read_csv,['c:/users/pawan singh/downloads/domestic_visitors/domestic_visitors_2016.csv',
                                          'c:/users/pawan singh/downloads/domestic_visitors/domestic_visitors_2017.csv',
                                         'c:/users/pawan singh/downloads/domestic_visitors/domestic_visitors_2018.csv',
                                         'c:/users/pawan singh/downloads/domestic_visitors/domestic_visitors_2019.csv']),
                          ignore_index = True)


# In[8]:


# Dropping null values from domestic_data


# In[ ]:


domestic_data = domestic_data.dropna(inplace = True)


# In[ ]:


domestic_data['visitors'] = pd.to_numeric(domestic_data['visitors'], errors = 'coerce')


# In[11]:


# merging all foreing visitors csv files in one pandas dataframe


# In[398]:


foreign_data = pd.concat(map(pd.read_csv,['c:/users/pawan singh/downloads/foreign_visitors/foreign_visitors_2016.csv',
                                          'c:/users/pawan singh/downloads/foreign_visitors/foreign_visitors_2017.csv',
                                         'c:/users/pawan singh/downloads/foreign_visitors/foreign_visitors_2018.csv',
                                         'c:/users/pawan singh/downloads/foreign_visitors/foreign_visitors_2019.csv']), ignore_index = True)


# In[17]:


# dropping null values from foreign_data


# In[399]:


foreign_data = foreign_data.dropna()


# In[400]:


foreign_data['visitors'] = pd.to_numeric(foreign_data['visitors'], errors = 'coerce')


# In[23]:


# Finding top10 districts with highest number of domestic visitors


# In[26]:


dv_sums = domestic_data[['district', 'visitors']]


# In[28]:


# float values only for domestic data


# In[30]:


floatvalues = pd.to_numeric(dv_sums['visitors'], errors = 'coerce')


# In[ ]:


dv_sums['visitorsnostd'] = floatvalues.values


# In[ ]:


# grouping domestic data distirct wise


# In[36]:


dv_sums = dv_sums.groupby(['district'])['visitorsnostd'].sum()


# In[38]:


dv_sums = pd.DataFrame({'district':dv_sums.index, 'visitorsno':dv_sums.values})


# In[41]:


top10_district = dv_sums.sort_values(by = 'visitorsno', ascending = False)


# In[51]:


top10_district = top10_district.head(10)


# In[44]:


# presenting top10 district on bar graph


# In[53]:


fig = px.funnel(top10_district, y = 'district', x = 'visitorsno', template = 'plotly_white',
                color = 'visitorsno').update_layout(font = dict(size = 25), showlegend = False)


# In[55]:


# top 3 district with highest annual growth


# In[56]:


# dometstic value


# In[57]:


annualg = domestic_data[['district', 'year', 'visitors']]


# In[ ]:


annualg['visitors'] = floatvalues.values


# In[61]:


annualg  = annualg.dropna()


# In[63]:


cagrbegval = annualg[annualg.year == 2016]


# In[65]:


cagrbegval = cagrbegval.groupby(['year', 'district'], as_index = False)['visitors'].sum()


# In[67]:


cagrbegval = pd.DataFrame({'year':cagrbegval['year'], 'district':cagrbegval['district'],'visitors':cagrbegval['visitors']})


# In[70]:


cagrbegval.set_index('district', inplace = True)


# In[80]:


cagrendval = annualg[annualg.year == 2019]


# In[81]:


cagrendval = cagrendval.groupby(['year', 'district'], as_index = False)['visitors'].sum()


# In[86]:


cagrendval = pd.DataFrame({'year':cagrendval['year'], 'district':cagrendval['district'], 'visitors':cagrendval['visitors']})


# In[88]:


cagrendval.set_index('district', inplace = True)


# In[93]:


cagrendval = cagrendval.drop(["Mulugu", "Narayanapet"])


# In[98]:


cagr = pow(cagrendval['visitors'] / cagrbegval['visitors'],1/3)-1


# In[100]:


cagr = cagr * 100.0


# In[114]:


cagrdf = pd.DataFrame({'district':cagr.index, 'CAGR':cagr.values})


# In[116]:


cagrdf = cagrdf.drop(index = [10, 23])


# In[118]:


cagrdesc = cagrdf.sort_values(by = 'CAGR', ascending = False)


# In[125]:


cagrdesc = cagrdesc.head(3)


# In[127]:


cagrfig = px.bar(cagrdesc, x = 'district', y = 'CAGR')  


# In[129]:


# foreign value


# In[168]:


foreignannualg = foreign_data[['district', 'year', 'visitors']]


# In[169]:


cagrforthree = foreignannualg[foreignannualg.year == 2016]


# In[170]:


cagrforthree = cagrforthree.groupby(['year', 'district'], as_index = False)['visitors'].sum()


# In[ ]:


# finding begining year from forien visitors data


# In[172]:


cagrforbeg = pd.DataFrame({'year':cagrforthree.year, 'district':cagrforthree.district, 'visitors':cagrforthree.visitors})


# In[173]:


cagrforbeg.set_index('district', inplace = True)


# In[185]:


# finding end year from foreign visitors data


# In[174]:


cagrforend = foreignannualg[foreignannualg.year == 2019]


# In[177]:


cagrforend = cagrforend.groupby(['year', 'district'],as_index = False)['visitors'].sum()


# In[180]:


cagrforend = pd.DataFrame({'year':cagrforend.year,'district':cagrforend.district,'visitors':cagrforend.visitors})


# In[182]:


cagrforend.set_index('district', inplace = True)


# In[187]:


cagrfor = pow(cagrforend['visitors'] / cagrforbeg['visitors'], 1/3) - 1


# In[189]:


cagrfor = cagrfor * 100.0


# In[192]:


cagrfor = pd.DataFrame({'District':cagrfor.index, 'CAGR':cagrfor.values})


# In[194]:


cagrfor.replace([np.inf, -np.inf], np.nan, inplace = True)


# In[237]:


cagrfor.dropna(inplace = True)


# In[201]:


cagrfor = cagrfor.sort_values(by = 'CAGR', ascending = False)


# In[ ]:


# finding top 3 district attracting most foreing visitors.


# In[207]:


top3for_cagr = cagrfor.head(3)


# In[204]:


# visualising top 3 district with highest foreign cagr


# In[210]:


forcagrfig = px.bar(top3for_cagr, x = 'district', y = 'CAGR')


# In[212]:


# combinedvagr highest CAGR


# In[213]:


combinedcagr = [cagrdesc,top3for_cagr ]


# In[217]:


comcagr = pd.concat(combinedcagr)


# In[219]:


comcagr['type'] = ['Domestic', 'Domestic', 'Domestic', 'Foreign', 'Foreign', 'Foreign']


# In[223]:


comcagrfig = px.bar(comcagr, x = 'district', y = 'CAGR', color = 'type', 
                    template = 'plotly_white', text_auto = True
                   ).update_layout(font = dict(size = 25))


# In[225]:


# top 3 district with lowest domestic visitors cagr


# In[226]:


# domestic visitors


# In[229]:


leastcagr = cagrdf.sort_values(by = 'CAGR', ascending = True)


# In[262]:


top3_least_dom_cagr = leastcagr.head(3)


# In[234]:


# top 3 district with lowest foreign visitors cagr


# In[253]:


leastforcagr = cagrfor.sort_values(by = 'CAGR', ascending = True)


# In[254]:


top3_least_for_cagr = leastforcagr.head(3)


# In[256]:


# combined lowest cagr


# In[264]:


comleastcagr = [top3_dom_least_cagr, top3_least_for_cagr]


# In[265]:


comleastcagr = pd.concat(comleastcagr)


# In[267]:


comleastcagr['type'] = ['Domestic','Domestic','Domestic','Foreign','Foreign','Foreign']


# In[275]:


comleastcagr.sort_values(by = 'CAGR', inplace = True)


# In[276]:


top3_comleastcagr = comleastcagr.head(3)


# In[283]:


comleastcagr_fig = px.bar(top3_comleastcagr, x = ['District'], y = 'CAGR', color = 'type',
                         template = 'plotly_white', text_auto = True).update_layout(font = dict(size = 25))


# In[284]:


# peak and low season for Hyderabad district


# In[285]:


# domestic value


# In[369]:


hyderabaddata = domestic_data[['district', 'month', 'visitors']]


# In[370]:


hyderabaddata = hyderabaddata[hyderabaddata.district == 'Hyderabad']


# In[371]:


hyderabaddata = hyderabaddata.groupby(['district', 'month'], as_index = False)['visitors'].sum()


# In[372]:


hyderabaddata = hyderabaddata.sort_values(by = 'visitors', ascending = False)


# In[373]:


# hyderabad peak month


# In[ ]:


hyderabaddata[:1]


# In[ ]:


# Hyderabad lowest peak month


# In[ ]:


hyderabaddata[-1:]


# In[377]:


hyderabaddata = hyderabaddata.groupby('month')['visitors'].mean()


# In[378]:


hyderabaddata = pd.DataFrame({'Month':hyderabaddata.index, 'Visitors':hyderabaddata.values})


# In[380]:


hyderabaddata = hyderabaddata.sort_values(by = ['Month'])


# In[382]:


hyderabaddata['Monthdate'] = pd.to_datetime(hyderabaddata['Month'],format = '%B', errors = 'coerce')


# In[383]:


hyderabaddata = hyderabaddata.sort_values(by = ['Monthdate'], ascending = True)


# In[385]:


hyderabaddata['Monthdate'] = hyderabaddata['Monthdate'].dt.month


# In[422]:


hyddomesticgraph = px.line(hyderabaddata, x = 'Month', y = 'Visitors', title = 'Hyderabad Doemstic Visitors Monthwise Graph')


# In[390]:


# foreign value


# In[402]:


hyderabad_data = foreign_data[foreign_data['district'] == 'Hyderabad']


# In[404]:


hyderabad_data = hyderabad_data.groupby(['district', 'month'], as_index = False)['visitors'].sum()


# In[408]:


hyderabad_data['monthdate'] = pd.to_datetime(hyderabad_data['month'], format = '%B', errors = 'coerce')


# In[411]:


hyderabad_data['monthdate'] = hyderabad_data['monthdate'].dt.month


# In[416]:


hyderabad_data = hyderabad_data.sort_values(by = 'monthdate')


# In[430]:


hyderbad_data = hyderabad_data[['month', 'visitors', 'monthdate']]


# In[424]:


# combined value for q4


# In[458]:


hydcombined = [hyderabaddata, hyderabad_data]


# In[459]:


hydcombined = pd.concat(hydcombined)


# In[460]:


hydcombined['type'] = ['Domestic', 'Domestic', 'Domestic','Domestic', 'Domestic', 'Domestic',
                       'Domestic', 'Domestic', 'Domestic','Domestic', 'Domestic', 'Domestic',
                      'Foreign', 'Foreign', 'Foreign','Foreign', 'Foreign', 'Foreign',
                       'Foreign', 'Foreign', 'Foreign','Foreign', 'Foreign', 'Foreign']


# In[468]:


fig = px.line(hydcombined, x = 'month', y = 'visitors', color = 'type')


# In[470]:


# top 3 and bottom 3 district with highest domestic to foreign visitors ratio


# In[471]:


domesticvisitors = domestic_data[['district', 'visitors']]


# In[472]:


foreignvisitors = foreign_data[['district', 'visitors']]


# In[ ]:


domesticvisitors.rename(columns = {'visitors':'domesticvisitors'}, inplace = True)


# In[ ]:


foreignvisitors.rename(columns = {'visitors':'foreignvisitors'}, inplace = True)


# In[482]:


domesticvisitors = domesticvisitors.groupby(['district'])['domesticvisitors'].sum()


# In[484]:


foreignvisitors = foreignvisitors.groupby(['district'])['foreignvisitors'].sum()


# In[ ]:


dtofratio = domesticvisitors.values / foreignvisitors.values


# In[491]:


dtofratio = pd.DataFrame({'district':domesticvisitors.index, 'dtofratio':dtofratio})


# In[493]:


dtofratio.replace([np.inf, -np.inf], np.nan, inplace = True)


# In[497]:


dtofratio.dropna(inplace = True)


# In[500]:


dtofratio['dtofratio'] = dtofratio['dtofratio'].round(decimals = 2)


# In[503]:


dtofratio = dtofratio.sort_values(by = 'dtofratio', ascending = False)


# In[506]:


top3_dtofratio = dtofratio.head(3)


# In[511]:


bottom3_dtofratio = dtofratio.tail(3)


# In[ ]:


# creating pie chart of top 3 district with domestic to foreign visitors ratio


# In[527]:


top3_dtoffig = px.pie(top3_dtofratio, values = 'dtofratio', names = 'district', hole = .2,
                color_discrete_sequence = px.colors.sequential.Darkmint).update_layout(font = dict(size = 25))


# In[ ]:


# creating pie chart of bottom 3 district with domestic to foreign visitors ratio


# In[541]:


bottom3_dtoffig = px.pie(bottom3_dtofratio, values = 'dtofratio', names = 'district', hole = .2,
                color_discrete_sequence = px.colors.sequential.Darkmint).update_layout(font = dict(size = 25))


# In[ ]:




