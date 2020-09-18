import pandas as pd
import numpy as np 
import matplotlib.pyplot as mpl 
from scipy.stats import chi2_contingency

#Importing data                 #IMPORT YOUR OWN FILES HERE
RA = pd.read_excel(r'//INSERT RURAL AWARENESS FILE LOCATION')
RC = pd.read_excel(r'//INSERT RURAL CLINICAL DATA FILE LOCATION')
UA = pd.read_excel(r'//INSERT URBAN AWARENESS FILE LOCATION')
UC = pd.read_excel(r'//INSERT URBAN CLINICAL DATA FILE LOCATION')
Awareness_Key = pd.read_excel(r'//INSERT KEY FOR THE AWARENESS FINDINGS')
Clinical_Key = pd.read_excel(r'//INSERT KEY FOR THE CLINICAL DATA FINDINGS')

#CHECK FOR DATA CONSISTENCY AND CLEAN DATA HERE (drop, replace etc.) //INSERT YOUR OWN CODE HERE 

#Calculating number and percentage of patients in each category for each parameter in the Urban and Rural Populations  
def perdfs(df):
    df_cut = df.drop(columns = ["PATIENT NO."]).select_dtypes(include = ['object']).dropna()    #CLEAN DATA AS REQUIRED
    per_df = pd.DataFrame(columns=["Column Name", "Category", "Percentage", "No. of Patients"])
    for col in df_cut:
        percentage = 0
        for x in sorted(pd.unique(df_cut[col])):
            if(pd.isna(x)):
                continue
            else:
                percentage = round( (sum(df_cut[col] == x))/(len(df_cut))*100 , 3)
                per_df = per_df.append({"Column Name": col, "Category": x, "Percentage": percentage, "No. of Patients" : sum(df_cut[col] == x) }, ignore_index=True)
    return(per_df)

#Dataframes to store percentage and number of patients in each category 
RA_per_df = perdfs(RA)
UA_per_df = perdfs(UA)
RC_per_df = perdfs(RC)
UC_per_df = perdfs(UC)    

#Function to attach value indicator above each bar in the plot
def textlabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
        xy=(rect.get_x() + rect.get_width() / 2, height),
        xytext=(0, 3),  # 3 points vertical offset
        textcoords="offset points",
        ha='center', va='bottom')

#Function for bar plotting the percentage of patients in each category for every parameter between the Urban and Rural populations
def plotdata(udf,rdf,tag, keydf):
    for col in pd.unique(udf["Column Name"]):
        U_tempdf = udf[udf["Column Name"] == col]
        R_tempdf = rdf[rdf["Column Name"] == col]    
    
        fig, (ax1,ax2) = mpl.subplots(1,2)
        fig.suptitle(col)
        r1 = ax1.bar(U_tempdf["Category"],U_tempdf["Percentage"], width = 0.25, label = ("URBAN " + tag ))
        ax1.set_xlabel("Category")
        ax1.set_ylabel("Percentage of Patients")
        ax1.legend(loc = "upper right")
        textlabel(r1,ax1)   

        r2 = ax2.bar(R_tempdf["Category"],R_tempdf["Percentage"], width = 0.25, label = ("RURAL " + tag))
        ax2.set_xlabel("Category")
        ax2.set_ylabel("Percentage of Patients")
        ax2.legend(loc = "upper right")
        textlabel(r2,ax2)
        print(keydf[col].dropna())
        mpl.show()

#Plotting the data
plotdata(UA_per_df, RA_per_df, "AWARENESS", Awareness_Key)
plotdata(UC_per_df, RC_per_df, "CLINICAL", Clinical_Key)

#CHI SQUARE TEST with threshold p-value 0.05 on Parameters in question and Patient type aka Urban or Rural
#NULL HYPOTHESIS H0: THERE IS NO DIFFERNCE BETWEEN OCCURENCE OF PARAMETER BETWEEN URBAN AND RURAL GROUPS
#i.e. OCCURENCE OF PARAMTER IS INDEPENDENT OF WETHER PATIENT IS URBAN OR RURAL  
#ALTERNATE HYPOTHESIS: THERE IS A DIFFERNCE BETWEEN OCCURENCE OF PARAMETER BETWEEN URBAN AND RURAL GROUPS
#i.e. OCCURENCE OF PARAMETER IS DEPENDENT ON WETHER PATIENT IS URBAN OR RURAL
def pval(df):
    stat, p, dof, expected = chi2_contingency(df)
    print(p)    
    if p <= 0.05:
	    print('Dependent (reject H0)')
    else:
	    print('Independent (fail to reject H0)')

def dependency(df1,df2):
    for x in pd.unique(df1["Column Name"]):
        udf = df1[df1["Column Name"]==x]
        rdf = df2[df2["Column Name"]==x]
        l1 = pd.unique(udf["Category"])
        l2 = pd.unique(rdf["Category"])

        if set(l1) == set(l2):
            df = [[udf["No. of Patients"]], [rdf["No. of Patients"]]]
            print(x)
            pval(df)

dependency(UA_per_df, RA_per_df)
dependency(UC_per_df, RC_per_df)