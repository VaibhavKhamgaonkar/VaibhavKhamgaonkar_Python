#importing the Std packages

import numpy as np 
import pandas as pd
import os, time


path = os.path.dirname(os.path.abspath('__file__')) + '/' 
#importing the files
eDay = pd.read_csv(path + 'Expected_EndOfDay_Positions.txt')
stDay = pd.read_csv (path + 'Input_StartOfDay_Positions.txt')
transactions = pd.read_json(path + '1537277231233_Input_Transactions.txt')

'''
Processing the Data: 
Arranging the Data of transaction table to more readable form using groupby method
'''

transData = transactions.groupby(['TransactionType','Instrument']).sum()
#Reseting the index to get normal Dataframe without Multiindex
transData.reset_index(inplace=True)
#showing the DataFrame for reference
print(transData)

#--------------------------------------------
#creating a custom function for core logic for updating the Quantities
def getTransactionQuantity(instrument,transType):
    instData = transData[transData['Instrument'] == instrument]
    sell = instData[instData['TransactionType'] == 'S']['TransactionQuantity'] 
    buy = instData[instData['TransactionType'] == 'B']['TransactionQuantity']

    #Verifying if the quantity if is is zero
    if sell.shape[0] <= 0:
        sell = 0        
    if buy.shape[0] <= 0:
        buy = 0
        
    if transType == 'E':
        delta = float(buy) - float(sell)
    elif transType == 'I':
        delta = float(sell) - float(buy)
    else:
        return('Transaction type is inavlid')
    return delta

#--------------------------------------------
'''
Calculating the delta and updating the records to position table as per the Rule mentioned.

If Transaction Type =B , For AccountType=E, Quantity=Quantity + TransactionQuantity
                        For AccountType=I, Quantity=Quantity - TransactionQuantity

If Transaction Type =S , For AccountType=E, Quantity=Quantity - TransactionQuantity
                        For AccountType=I, Quantity=Quantity + TransactionQuantity
'''


#using apply method with lambda function to call the mehtod for getting delta value of quantity
stDay['Delta'] = stDay[['Instrument','AccountType']].apply(lambda x : getTransactionQuantity(*x),axis=1)
stDay['Quantity'] = stDay['Quantity'] + stDay['Delta']


#Verifying the Data after update
print(stDay)

#verifying it with Endo of Position file
print(eDay)


