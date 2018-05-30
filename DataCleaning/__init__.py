#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 08:39:55 2018

@author: communitysoftwaregroup
"""


import pandas as pd

class Liheap:
    # changing data type
    def typeToString(self,dataFrame,itemsList,changeTo):
        print(itemsList)
        for i in range(len(itemsList)):
            dataFrame[itemsList[i]]=dataFrame[itemsList[i]].astype(changeTo[i])
    
    # Convert the date
    def convertToDate(self,dataFrame,dateList):
        for k in range(len(dateList)):
            dataFrame[dateList[k]]=pd.to_datetime(dataFrame[dateList[k]])
            dataFrame[dateList[k]]=dataFrame[dateList[k]].dt.date
            dataFrame[dateList[k]]=pd.to_datetime(dataFrame[dateList[k]])
            
    def createCustomKeys(self,LiheapDF1):
        rearrangedColumns=list(LiheapDF1)                                 
        
        ##Adding Person Key and Householdkey
        LiheapDF1["PersonKey"]=LiheapDF1['FiscalYear'].map(str)+LiheapDF1['AgencyID'].map(str)+LiheapDF1['App Number'].map(str)+LiheapDF1['Person #'].map(str)
        LiheapDF1["HouseholdKey"]=LiheapDF1['FiscalYear'].map(str)+LiheapDF1['AgencyID'].map(str)+LiheapDF1['App Number'].map(str)
        #Sorting Dataframes                              
        
        ## Rearranging Columns
        rearrangedColumns.insert(4,"PersonKey")
        rearrangedColumns.insert(5,"HouseholdKey")
        LiheapDF1=LiheapDF1[rearrangedColumns]
        LiheapDF1=LiheapDF1.sort_values(by=['HouseholdKey','PersonKey'])
        
        return LiheapDF1

    def replaceNullWithNU(self,LiheapDF1):
        
        return LiheapDF1

        
    def flattenSourceName(self,df):
        df=df['App Number','Person #', 'IncomeSourceName','Amount']
        


LiheapObject=Liheap()
inputFile=pd.read_csv("/home/communitysoftwaregroup/Documents/LiheapMergedData/dum1.csv", sep='_')
LiheapDF1=pd.DataFrame(inputFile)
# delete input
del inputFile

#### ELEMENTS TO BE DROPPED
#elementsToBeDropped=['Amount','IncomeSourceName','Vendor Number', 'P/S', 'Vendor Code', 'Vendor name','SourceNumber','IncomeSource']
elementsToBeDropped=['Primary Name', 'SourceNumber','Secondary Name','Application Type','Zip Code','LanguageCode','Primary Code', 'Secondary Code', 'FamilyType','LastYearEligible','PersonEthnicity', 'PersonRace','Vendor Number', 'IncomeSource','DivBillYN','SeuYN', 'IncomeSourceName', 'Amount','Vendor name','FundId','LanguageSpoken','TransactionNumber','PaymentNumber','VendorCode','UserName','CheckNumber','CheckDate','AccountNumberPaid','FeeCode','Income String','PaidBill','CheckId','Commitment']
LiheapDF1=LiheapDF1.drop(elementsToBeDropped,axis=1)

                   
## Type Conversion =====================================
itemsList=['AgencyID','App Number','Person #']
changeTo=["object","object","object"]
LiheapObject.typeToString(LiheapDF1,itemsList,changeTo)

### Time and date
dateList=['TransactionDateTime','DeliveryDate','BillingDate']
LiheapObject.convertToDate(LiheapDF1,dateList)
### =========================


##  Create Keys===========================================================
LiheapDF1=LiheapObject.createCustomKeys(LiheapDF1)

### Drop Duplicates from the main dataframe
LiheapDF1=LiheapDF1.drop_duplicates()

####Creating 2 separate dataframes
df2elements=['PersonKey','HouseholdKey','TransactionNumber', 'TransactionDateTime', 'VoucherNumber', 'PaymentNumber', 'VendorCode', 'FuelType', 'DeliveryDate', 'BillingDate', 'RetailPrice', 'Gallons', 'MORPrice', 'FeeAmount', 'FeeCode', 'TotalPaid', 'Balance', 'UserName', 'CheckDate', 'CheckNumber', 'AccountNumberPaid', 'Deleted', 'OriginalGallons', 'SecondaryPay', 'OriginalFee', 'PaidBill', 'ForceRetailPayment', 'PriceBeingPaid', 'DivideBill', 'Adjustment', 'CheckId', 'AdjustsVoucherNumber', 'AdjustsPaymentNumber', 'AdjustsAppNumber', 'Commitment']
LiheapDF2=LiheapDF1[df2elements].copy()
LiheapDF1=LiheapDF1.drop(df2elements,axis=1)
LiheapDF1=LiheapDF1.drop_duplicates()































####Write types to file

# Writing Datatype to a file
file = open("/home/communitysoftwaregroup/Documents/LiheapMergedData/types.txt","w") 
a=['FiscalYear', 'AgencyID', 'App Number', 'Person #', 'BenefitLevel', 'TotalBenefitPaid', 'Remaining', 'City/Town', 'Total Income', 'Primary Heat Source',   'Number in Household', 'FamilyTypeDescription',  'ConsTotalBilled', 'LangSpeakUnderstandEng', 'ConsGallonsConsumed', 'Age', 'Sex', 'Handicap',  'Income', 'Educ', 'Insurance',  'RaceDescription',  'Benefit Level', 'HeatingSystemNeedRepair', 'HomeNeedWAP', 'Dwelling weatherized', 'Divide Bill',  'SEU',   'P/S', 'Vendor Code',  'BillingNotInHousehold', 'TransactionDateTime', 'VoucherNumber',   'FuelType', 'DeliveryDate', 'BillingDate', 'RetailPrice', 'Gallons', 'MORPrice', 'FeeAmount',  'TotalPaid', 'Balance', 'Deleted', 'OriginalGallons', 'SecondaryPay', 'OriginalFee',  'ForceRetailPayment', 'PriceBeingPaid', 'DivideBill', 'Adjustment',  'AdjustsVoucherNumber', 'AdjustsPaymentNumber', 'AdjustsAppNumber']
   
for i in range(len(a)):
    print(a[i]," : ",LiheapDF1[a[i]].dtype)
    x=LiheapDF1[a[i]].dtype
    sk=a[i]+" : "+str(x)+"\n"
    file.write(str(sk))
file.close()