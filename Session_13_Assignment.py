# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:28:56 2018

@author: Ravikiran Bailkeri
"""


import sys, os
import pandas as pd
import pysqldf
from pandasql import sqldf

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', sep=',', header=None, names=['age','workclass','fnlwgt','education','education_num','marital_status','occupation','relationship','race','sex','capital_gain','capital_loss','hours_per_week','native_country','class'])
print (df)
df_obj = df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())


pysqldf = lambda q: sqldf(q, globals())
#Create a sql db from adult dataset and name it sqladb
sqLadb = pysqldf("SELECT * FROM df;")

#1. Select 10 records from the adult sqladb

print ("sqLadb::\n",sqLadb)

print ("# 1 Question Output ::: \n",pysqldf('select * from sqLadb limit 10;'))

#2. Show me the average hours per week of all men who are working in private sector
print ("@ 2 Output:: \n",pysqldf('SELECT avg(hours_per_week) FROM sqLadb WHERE workclass="Private" And Sex="Male";'))

#3. Show me the frequency table for education, occupation and relationship, separately
print ("#3.1 Sub question:::\n",pysqldf(""" SELECT education,count(education) AS frequency FROM sqLadb GROUP by education """))
print ("#3.2 Sub question::: \n",pysqldf(""" SELECT occupation, count(occupation) as frequency from sqLadb group by occupation """))
print ("3.3 Sub question ::: \n",pysqldf(""" SELECT relationship, count(relationship) as frequency from sqLadb group by relationship """))


#4. Are there any people who are married, working in private sector and having a masters degree

print ("#4 Output::: \n", pysqldf("""select count(1) from sqLadb where (marital_status='Married-civ-spouse' or marital_status='Married-AF-spouse' or marital_status='Married-spouse-absent') And education = 'Masters' And workclass = 'Private' """))

       
# 5. What is the average, minimum and maximum age group for people working in different sectors
print ("# 5 Output ::\n",pysqldf('select workclass, avg(age), min(age), max(age) from sqLadb group by workclass order by 2 desc;'))


# 6. Calculate age distribution by country

print ("#6 Outut \n", pysqldf('select native_country, avg(age), min(age), max(age) from sqLadb group by native_country order by 2 desc;'))

#7. Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and 'capital-loss'
print ("# 7 Output- as last column:: \n", pysqldf('select *, (capital_gain - capital_loss) As net_capital_gain from sqLadb'))