# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import sem

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "data/mouse_drug_data.csv"
clinical_trial_data_to_load = "data/clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data
MouseData = pd.read_csv(mouse_drug_data_to_load)
TrialData = pd.read_csv(clinical_trial_data_to_load)

# Combine the data into a single dataset
CompleteDrugData = pd.merge(MouseData, TrialData, on='Mouse ID')

# Display the data table for preview
print(CompleteDrugData.head())



# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint
GroupByDF = CompleteDrugData.groupby(["Drug", "Timepoint"]).mean()['Tumor Volume (mm3)']

# Convert to DataFrame
MeanDataDF = pd.DataFrame(GroupByDF)

# Preview DataFrame
print(MeanDataDF.head())



# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
GroupByDF = CompleteDrugData.groupby(["Drug", "Timepoint"]).sem()['Tumor Volume (mm3)']

# Convert to DataFrame
SEMDataDF = pd.DataFrame(GroupByDF)

# Preview DataFrame
print(SEMDataDF.head())



# Minor Data Munging to Re-Format the Data Frames
MeanDataDF = MeanDataDF.pivot_table(values = "Tumor Volume (mm3)", columns = "Drug", index = "Timepoint")
SEMDataDF = SEMDataDF.pivot_table(values = "Tumor Volume (mm3)", columns = "Drug", index = "Timepoint")

# Preview that Reformatting worked
print(MeanDataDF)
print(SEMDataDF)



# Generate the Plot (with Error Bars)
markers = ['o:r','^:b','s:g','d:k']
fig = plt.figure()
ax = fig.add_subplot()
x = 0
GraphList = ['Capomulin','Infubinol','Ketapril','Placebo']
for drug in GraphList:
    ax.errorbar(MeanDataDF.index, MeanDataDF[drug], yerr=SEMDataDF[drug], fmt=markers[x], label=drug, alpha=0.8, lw=1)
    x += 1
    if x == 4:
        x = 0
plt.legend()
plt.title('Tumor Response to Treatment')
plt.xlabel('Time (Days)')
plt.ylabel('Tumor Volume (mm3)')

# Save the Figure
plt.savefig("Tumor Response to Treatment.png")

# Show the figure
plt.show()



# Store the Mean Met. Site Data Grouped by Drug and Timepoint
GroupByDF = CompleteDrugData.groupby(["Drug", "Timepoint"]).mean()["Metastatic Sites"]

# Convert to DataFrame
MetaDataDF = pd.DataFrame(GroupByDF)

# Preview DataFrame
print(MetaDataDF.head())



# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint 
GroupByDF = CompleteDrugData.groupby(["Drug", "Timepoint"]).sem()["Metastatic Sites"]

# Convert to DataFrame
SEMDataDF = pd.DataFrame(GroupByDF)

# Preview DataFrame
print(SEMDataDF.head())



# Minor Data Munging to Re-Format the Data Frames
MetaDataDF = MetaDataDF.pivot_table(values = "Metastatic Sites", columns = "Drug", index = "Timepoint")
SEMDataDF = SEMDataDF.pivot_table(values = "Metastatic Sites", columns = "Drug", index = "Timepoint")
# Preview that Reformatting worked
print(MetaDataDF)
print(SEMDataDF)



# Generate the Plot (with Error Bars)
fig = plt.figure()
ax = fig.add_subplot()
x = 0
GraphList = ['Capomulin','Infubinol','Ketapril','Placebo']
for drug in GraphList:
    ax.errorbar(MetaDataDF.index, MetaDataDF[drug], yerr=SEMDataDF[drug], fmt=markers[x], label=drug, alpha=0.8, lw=1)
    x += 1
    if x == 4:
        x = 0
plt.legend()
plt.title('Metastatic Spread During Treatment')
plt.xlabel('Treatment Duration (Days)')
plt.ylabel('Metastatic Sites')

# Save the Figure
plt.savefig("Metastatic Spread During Treatment")

# Show the Figure
plt.show()



# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
GroupByDF = CompleteDrugData.groupby(["Drug", "Timepoint"]).count()["Mouse ID"]

# Convert to DataFrame
MiceDF = pd.DataFrame(GroupByDF)
MiceDF = MiceDF.rename(columns = {'Mouse ID':'Mouse Count'})

# Preview DataFrame
print(MiceDF.head())



# Minor Data Munging to Re-Format the Data Frames
MiceDF = MiceDF.pivot_table(values = "Mouse Count", columns = "Drug", index = "Timepoint")

# Preview the Data Frame
print(MiceDF)



# Generate the Plot (Accounting for percentages)
fig = plt.figure()
ax = fig.add_subplot()
x = 0
GraphList = ['Capomulin','Infubinol','Ketapril','Placebo']
for drug in GraphList:
    ax.errorbar(MiceDF.index, MiceDF[drug]/MiceDF[drug].iloc[0]*100, fmt=markers[x], label=drug, alpha=0.8, lw=1)
    x += 1
    if x == 4:
        x = 0

#Format the graph
plt.legend()
plt.title('Survival During Treatment')
plt.xlabel('Time (Days)')
plt.ylabel('Survival Rate (%)')

# Save the Figure
plt.savefig("Survival During Treatment")

# Show the Figure
plt.show()



# Calculate the percent changes for each drug
PercentChanges = (MeanDataDF.iloc[-1] - MeanDataDF.iloc[0]) / MeanDataDF.iloc[0] * 100

# Display the data to confirm
print(PercentChanges)



#Initialize graph
fig = plt.figure()
ax = fig.add_subplot()
x = -0.15

#Plot data points
for drug in GraphList:
    #conditional formatting
    if PercentChanges[drug] > 0:
        barcolor = 'red'
        y = 5
    else:
        barcolor = 'green'
        y = -7
    #Plot data in bar chart
    ax.bar(drug, PercentChanges[drug], width=1, color=barcolor)
    #Label bar with percentage
    ax.text(x, y, "{:.0f}%".format(PercentChanges[drug]), color="white")
    x += 1

#Format graph
ax.grid()
ax.set_title("Tumor Change Over 45 Day Treatment")
ax.set_ylabel("% Tumor Volume Change")
ax.set_ylim(-30,70)
ax.set_xticks([0.5,1.5,2.5,3.5])
ax.set_xticklabels(GraphList)
yticks = [PercentChanges[drug] for drug in GraphList]

# Save the Figure
plt.savefig("Tumor Change Over 45 Day Treatment")

# Show the Figure
fig.show()