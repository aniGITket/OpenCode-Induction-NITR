import pandas as pd
import numpy as np 
import matplotlib.pyplot as mpl 

#Reading the data    #IMPORT YOUR OWN FILES HERE
data = pd.read_excel(r'//FILE LOCATION')
data["Stat Type"].replace({"A" : "Attack", "D" : "Defence"}, inplace = True)

#Function to attach value indicator above each plot
def textlabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
        xy=(rect.get_x() + rect.get_width() / 2, height),
        xytext=(0, 3),  # 3 points vertical offset
        textcoords="offset points",
        ha='center', va='bottom')
                       
#Plotting by Season and part of play i.e. Attack and Defence
for y in pd.unique(data["Season"]):
    for x in pd.unique(data["Stat Type"]):
            df0 = data[data["Stat Type"] == x] 
            df = df0[df0["Season"] == y]
            x1 = np.arange(len(df["Stats/90"]))            
            #Plotting
            fig, ax = mpl.subplots()
            r1 = ax.bar(x1, df["Aouar"], label = "Aouar", width = 0.25)
            r2 = ax.bar(x1 + 0.25, df["Partey"], label = "Partey", width = 0.25)
            r3 = ax.bar(x1 + 0.5, df["Xhaka"], label = "Xhaka", width = 0.25)
            ax.set_xlabel("STAT")
            ax.set_ylabel("Value")
            ax.set_xticks(x1 + 0.25)
            ax.set_xticklabels(df["Stats/90"])
            ax.set_title(x + " " + y)
            ax.legend()
            textlabel(r1)
            textlabel(r2)
            textlabel(r3)                        
            fig.tight_layout()
            mpl.show()

#Finding average stats over 2018/19 & 2019/20
df = pd.DataFrame()

for y in pd.unique(data['Season']):
    x = data[data["Season"] == y]
    x.reset_index( drop = True, inplace = True)
    df = pd.concat([df, x], axis = 1)

adf = pd.DataFrame({"AA" : df["Aouar"].mean(axis = 1 ).tolist()})
pdf = pd.DataFrame({"PA" : df["Partey"].mean(axis = 1 ).tolist()})
xdf = pd.DataFrame({"XA" : df["Xhaka"].mean(axis = 1 ).tolist()})

adf.reset_index(drop = True, inplace = True)
pdf.reset_index(drop = True, inplace = True)
xdf.reset_index(drop = True, inplace = True)

ds = data[data["Season"]=="2018/19"]
dst = ds["Stat Type"]
dst90 = ds["Stats/90"]
dst.reset_index(drop = True, inplace = True)
dst90.reset_index(drop = True, inplace = True)

avg_df = pd.concat([dst90,dst,adf,pdf,xdf], axis = 1)

avg_df["AA"] = avg_df["AA"].round(decimals = 2)
avg_df["PA"] = avg_df["PA"].round(decimals = 2)
avg_df["XA"] = avg_df["XA"].round(decimals = 2)

print(avg_df)
#Plotting the mean stats over 2018/19 & 2019/20  
for x in pd.unique(avg_df["Stat Type"]):
        df0 = avg_df[avg_df["Stat Type"] == x]
        x1 = np.arange(len(df0["Stats/90"]))            
        #Plotting
        fig, ax = mpl.subplots()
        r1 = ax.bar(x1, df0["AA"], label = "Aouar", width = 0.25)
        r2 = ax.bar(x1 + 0.25, df0["PA"], label = "Partey", width = 0.25)
        r3 = ax.bar(x1 + 0.5, df0["XA"], label = "Xhaka", width = 0.25)
        ax.set_xlabel("STAT")
        ax.set_ylabel("Value")
        ax.set_xticks(x1 + 0.25)
        ax.set_xticklabels(pd.unique(df0["Stats/90"]))
        ax.set_title(x + " 2018/19 & 2019/20" )
        ax.legend()
        textlabel(r1)
        textlabel(r2)
        textlabel(r3)                       
        fig.tight_layout()
        mpl.show()