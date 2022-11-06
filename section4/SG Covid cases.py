
# coding: utf-8

# In[ ]:


import requests
import pandas as pd


# In[ ]:


response = requests.get("https://api.covid19api.com/country/singapore/status/confirmed?from=2020-03-01T00:00:00Z&to=2022-10-01T00:00:00Z")


# In[ ]:


result = response.json()


# In[ ]:


df = pd.DataFrame(result)


# In[ ]:


df['Daily_cases'] = df['Cases'].shift(periods = 1)
df['Daily_cases'][0]= 0
df['Daily_count'] = df['Cases'] - df['Daily_cases']


# In[ ]:


df.to_csv('SGCOVID.csv')

