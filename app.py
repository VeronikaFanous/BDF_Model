
import streamlit as st
import pickle
import pandas as pd
import numpy as np

#import dataset (not normalized)
products = pd.read_csv("export_products_notNorm.csv",low_memory=False, encoding='utf-8')

# loading the trained model
RF_model = pickle.load(open('RF_model.pkl', 'rb'))
DTR_model = pickle.load(open('DTR_model.pkl', 'rb'))
ET_model = pickle.load(open(r'ET_model.pkl', 'rb'))

 
#@st.cache()  
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:teal;padding:10px"> 
    <h1 style ="color:black;text-align:center;">Forecast of quantity sold</h1> 
    </div> 
    """
      
    # Display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
    activities=['Decision Tree','Extra Trees','Random Forest']
    option=st.sidebar.selectbox('Which model would you like to use?',activities)
    st.subheader(option)
    
    #Product, Channel, Month: 
    product_name = ['TXQ0T', 'TXQQX', 'TXQT7', 'TXQTZ', 'TXX00', 'TXX06' ,'TXX5Q' ,'TXXX0', 'TXZ06','TZQAQ']
    channel_name = ['A', 'B', 'C', 'D', 'E', 'F']
    month_name = ["January", "February", "March", "April", "May", "June","July","August", "September", "October", 
                  "November", "December"]
    isPromoPeriod_name = ['Yes', 'No']
    
    # following lines create boxes in which user can enter data required to make prediction 
    product = st.selectbox('Which Product would like to choose?', product_name)
    channel = st.selectbox('Please select the distribution channel',channel_name) 
    month = st.selectbox('Please select a month', month_name)
    isPromoPeriod = st.radio('Is Promo Week?', isPromoPeriod_name)
    TV = st.number_input('Please specify the amount of investment in TV advertising.')
    online = st.number_input('Please specify the amount of investment in Online advertising.')
    StoresAvailability = st.number_input('Please specify the percentage of stores in which the product is available in the range of [0.00, 1.00].')
    price = st.number_input('Please specify the price of the Product.')
    
    
    p = np.zeros(len(product_name)-1)
    c = np.zeros(len(channel_name)-1)
    m = np.zeros(len(month_name)-1)
    
    for i in range(len(p)):
        if product == product_name[i+1]:
            p[i]=1
            
    for i in range(len(c)):
        if channel == channel_name[i+1]:
            c[i] = 1
    
    for i in range(len(m)):
        if month == month_name[i+1]:
            m[i] = 1
    
    p2, p3, p4, p5, p6, p7, p8, p9, p10 = p
    
    c2, c3,c4,c5, c6 = c
    
    m2,m3,m4,m5,m6,m7,m8,m9,m10,m11, m12 = m
    
    
    # Pre-processing user input    
    if option == "Random Forest":
        model = RF_model
    
    elif option == "Extra Trees": 
        model = ET_model
    else:
        model = DTR_model
    
    #IsPromoWeek
    if isPromoPeriod == "Yes":
        promo = True
    else:
        promo = False 
    
    #normalisation of input:
    price = (price - products['Price'].min())/(products['Price'].max()-products['Price'].min())
    online = (online - products['Online'].min())/(products['Online'].max()-products['Online'].min())
    TV = (TV - products['TV'].min())/(products['TV'].max()-products['TV'].min())
    StoresAvailability = (StoresAvailability - products['StoresAvailability'].min())/(products['StoresAvailability'].max()-products['StoresAvailability'].min())
    #isPromoPeriod = (isPromoPeriod - products['isPromoPeriod'])
    
    inputs = [[price, promo, TV, online, StoresAvailability, p2, p3, p4, p5, p6, p7, p8, p9, p10,
               c2, c3,c4,c5, c6, m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12]]
        
    # when 'Forecast' is clicked, make the prediction and store it 
    if st.button("Forecast"): 
        result = model.predict(inputs)
        st.success('The quantity sold is {}'.format(result))

    
if __name__=='__main__': 
    main()
