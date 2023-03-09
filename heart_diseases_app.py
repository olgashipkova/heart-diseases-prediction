#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Пользовательское-приложение" data-toc-modified-id="Пользовательское-приложение-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Пользовательское приложение</a></span></li></ul></div>

# # Пользовательское приложение 

# In[ ]:


import streamlit as st
import pandas as pd
import pickle
from pickle import dump, load
import os

st.title('Рассчитайте вероятность риска развития сердечно-сосудистых заболеваний :broken_heart:')

st.subheader('Введите Ваши данные')
warning = 'Проверьте, пожалуйста, правильность введенных данных!'
#age = st.number_input('Возраст, лет', key='age') 
age = st.slider('Возраст, лет', 20, 100, 50, key='age')
height = st.slider('Рост (см)', 150, 210, 175, key='height')
if height >210:
    st.info(warning, icon="⚠️")
weight = st.slider('Вес (кг)', 47, 150, 85, key='weight')
#weight = st.number_input('Вес, кг', key='weight')
if weight >150:
    st.info(warning, icon="⚠️")
ap_hi = st.slider('Систолическое артериальное давление', 60, 250, 120, key='ap_hi')
ap_lo = st.slider('Диастолическое артериальное давление', 40, 150, 80, key='ap_lo')    
if (ap_lo >100) or (ap_hi >250) :
    st.info(warning, icon="⚠️")
if (ap_lo <40) or (ap_hi <60) :
    st.info(warning, icon="⚠️")    
if ap_hi == ap_lo:
    st.sidebar.warning('Систолическое давление не может быть равно диастолическому', icon="⚠️")
elif ap_hi < ap_lo:
    st.sidebar.warning('Диастолическое давление не может быть меньше систолического', icon="⚠️")    
gender = st.radio("Пол", options=("М", "Ж"), key='gender')
gluc = st.radio("Уровень сахара", options=("1", "2", "3"), key='gluc')
cholesterol = st.radio("Уровень холестерина", options=("1", "2", "3"), key='cholesterol')
smoke = st.radio("Курите ли Вы ?", options=("Да", "Нет"), key='smoke')
alco = st.radio("Злоупоребляете ли Вы алкоголем ?", options=("Да", "Нет"), key='alco')
active = st.radio("Ведете ли Вы активный образ жизни ?", options=("Да", "Нет"), key='active')

with open(os.path.dirname(__file__) + '/model.pkl', 'rb') as dataset: 
     model = pickle.load(dataset)
scaler = pickle.load(open(os.path.dirname(__file__) + '/scaler.pkl','rb'))        




age = age * 365
if gender == "М":
    gender_1 = 0
    gender_2 = 1
else:
    gender_1 = 1
    gender_2 = 0
 
  
if cholesterol == 1:
    cholesterol_1 = 1
    cholesterol_2 = 0
    cholesterol_3 = 0
elif cholesterol == 2:
    cholesterol_1 = 0
    cholesterol_2 = 1 
    cholesterol_3 = 0
else: 
    cholesterol_1 = 0
    cholesterol_2 = 0 
    cholesterol_3 = 1
    
if  gluc == 1:
    gluc_1 = 1
    gluc_2 = 0
    gluc_3 = 0
elif gluc == 2:
    gluc_1 = 0
    gluc_2 = 1 
    gluc_3 = 0
else: 
    gluc_1 = 0
    gluc_2 = 0 
    gluc_3 = 1     
    
if smoke == 'Да':
    smoke_0 = 0
    smoke_1 = 1
else: 
    smoke_0 = 1
    smoke_1 = 0    
    
if alco == 'Да':
    alco_0 = 0
    alco_1 = 1
else:
    alco_0 = 1
    alco_1 = 0
    
if active == 'Да':
    active_0 = 0
    active_1 = 1
else:
    active_0 = 1
    active_1 = 0
    
    
      
data = pd.DataFrame({'age': age,
                     'height': height,
                     'weight': weight,
                     'ap_hi': ap_hi,
                     'ap_lo': ap_lo,
                     'gender_1': gender_1,
                     'gender_2': gender_2,
                     'cholesterol_1': cholesterol_1,
                     'cholesterol_2': cholesterol_2,
                     'cholesterol_3': cholesterol_3,
                     'gluc_1': gluc_1,
                     'gluc_2': gluc_2,
                     'gluc_3': gluc_3,
                     'smoke_0': smoke_0,
                     'smoke_1': smoke_1,
                      'alco_0': alco_0,
                      'alco_1': alco_1,
                      'active_0': active_0,
                      'active_1': active_1
                       }, index=[0])                
    
if st.button("Рассчитать вероятность"):
    numeric = ['age', 'height', 'weight', 'ap_hi', 'ap_lo']
    data[numeric] = scaler.transform(data[numeric])
    prediction = model.predict_proba(data)[:,1]
    st.sidebar.header('Результаты',)
   
    prediction = round(float(prediction*100),2)
    if prediction >= 50:
        st.sidebar.warning('Вероятность риска развития сердечно-сосудистых заболеваний составляет: '+str(prediction)+'%')
       
        if ap_hi > 150:
            st.sidebar.warning('Ваше систолическое артериальное давление выше нормы !',  icon="⚠️")
        if ap_hi < 100:
            st.sidebar.warning('Ваше систолическое артериальное давление ниже нормы !',  icon="⚠️")    
        if (ap_lo > 90):
            st.sidebar.warning('Ваше диастолическое артериальное давление выше нормы !',  icon="⚠️")
        if (ap_lo < 50):
            st.sidebar.warning('Ваше диастолическое артериальное давление ниже нормы !',  icon="⚠️")    
        if (cholesterol_1 == 1) or (cholesterol_2 == 1):
            st.sidebar.warning('У Вас высокий уровень холестерина в крови!',  icon="⚠️")
        if (gluc_1 == 1) or (gluc_2 == 1):
            st.sidebar.warning('У Вас высокий уровень холестерина в крови!',  icon="⚠️") 
        if smoke_1 == 1 :
            st.sidebar.warning('Курение вредит Вашему здоровью !',  icon="⚠️") 
        if alco_1 == 1 :
            st.sidebar.warning('Злоупотребление алкоголем вредит Вашему здоровью !',  icon="⚠️") 
        if active_0 == 1 :
            st.sidebar.warning('Вам рекомендуется вести активный образ жизни!',  icon="⚠️")                 
    else:
        st.sidebar.write('Риск развития сердечно-сосудистого заболевания составляет: ' + str(prediction)+'%')
    
    

