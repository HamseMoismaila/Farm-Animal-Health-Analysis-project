# Here is all the data you need: "farm_animals_large.csv"


# Task 1 Load this data  into 

# Task 2 Explore the loaded data to understand its characteristics and identify potential issues.

# Task 3: Clean the data by handling inconsistencies and outliers.

# task 4: Analyze the cleaned data to gain insights into the relationships between different variables.

# Task 5: Visualize the key findings from the data analysis.

# Task 6: Summarize your insight and findings from the analysis.



# Task 1: Load this data into DataFrames


import pandas as pd

try:
    file_path =  'Farm_analysis/farm_animals_large.csv'
    df = pd.read_csv(file_path)
    print(df.head()) 
    print(df.shape)  #  number of row  and columns  but if add print(df.shape()) it willl give error saying tuples object has no attribute shape
    print(df.dtypes)
except FileNotFoundError:
    print("Error: 'farm_animals_large.csv' not found. please check the file path")
except pd.errors.ParserError:  # pd.errors.ParserError occurs when Pandas fails to correctly read a CSV file due to formatting issues, such as incorrect delimiters, missing/extra columns, or encoding problems.
    print("Error parsing CSV file. please check the file contents")
except Exception as e:
    print(f"An error occurred: {e}")



import pandas as pd

df = pd.read_csv('Farm_analysis/farm_animals_large.csv')

print(df.head())
print(df.shape)
print(df.dtypes)


# Task 2: Explore the loaded data to understand its characteristics and indentify potential issues

# Check for missing values 

print(df.isnull().sum())

# check for duplicates

print(df.duplicated().sum())

# check for unique values in each column(for categorical columns)

for col in df.columns:
    if df[col].dtype == 'object':
        print(f"\n unique value in {col} column: {df[col].value_counts()}")
        

# for col in ['Animal', 'Type', 'Healthy']:
#     print("\n unique value in and counts for column '{col}'")
#     print(df[col].value_counts())


# Decsriptive statitics for numberical columns 

print("\n Decriptive statistics for numerical columns:")

print(df[["Age", "Weight(kg)"]].describe())


# Task 3  Data cleaning by handling inconsistencies and outliers

df['Healthy'] = df["Healthy"].apply(lambda x: 'No' if x != 'Yes' else x) # replace all values in 'Healthy column that are not 'Yes' with 'No'


# handle outliers in weights(kg) Usinf IQR Methode

Q1_age = df['Age'].quantile(0.25)
Q3_age = df['Age'].quantile(0.75)
IQR_age = Q3_age - Q1_age
lower_bound_age = Q1_age - 1.5 * IQR_age
upper_bound_age = Q3_age + 1.5 * IQR_age

df['Age'] = df['Age'].clip(lower=lower_bound_age, upper=upper_bound_age)

# Handle outliers in weights(kg) using IQR  method
 
Q1_weight =  df['Weight(kg)'].quantile(0.25)

Q3_weight = df['Weight(kg)'].quantile(0.75)

IQR_weight = Q3_weight - Q1_weight

lower_bound_weight = Q1_weight - 1.5 * IQR_weight

upper_bound_weight = Q3_weight + 1.5 * IQR_weight

df['Weight(kg)'] =df['Weight(kg)'].clip(lower=lower_bound_weight, upper= upper_bound_weight)

print(df.dtypes)
print(df.head())


# Task 4 Analyze the cleaned data to gain insights into the relationships beteen different variables 

# Calculate the average weight of each animal type 


print("\n Average weight of each animal type:")

average_weight = df.groupby('Animal')['Weight(kg)'].mean() # calculates the average animal by types using groupby 
print(round(average_weight,2))

# group the data and calculate descriptive statitics

print("\n weight grouped descriptive statitics")

weight_stats =  df.groupby(['Animal', 'Type'])['Weight(kg)'].agg(['mean', 'median', 'std', 'min', 'max'])


print('\n Age grouped descriptive statitics ')

age_stats = df.groupby(['Animal', 'Type'])['Age'].agg(['mean', 'median', 'std', 'min', 'max'])


print(weight_stats)

print(age_stats)





# Explore the realtionship other variables


healthy_stats = df.groupby('Healthy')[["Weight(kg)", "Age"]].mean()

print(round (healthy_stats,3))



# Other ways to check the above  
# Works similarly to groupby() but can handle multiple aggregation functions.

healthy_stats = df.pivot_table(index='Healthy', values=['Weight(kg)', 'Age'], aggfunc='mean')
print(healthy_stats)



# calculate proposrtions of healthy/Unhealthy animal with in each categoruy 


health_propotions = df.groupby(['Animal', 'Type'])['Healthy'].value_counts(normalize=True).unstack


print(health_propotions)



#  Calculate the correlation coefficient between 'Weight(kg)' and 'Age' and prepare for a scatter plot visualization in a later step.

correlations = df['Weight(kg)'].corr(df["Age"])

print(f"Correlation between Weight(kg) and Age: {correlations}")



# Group the data by 'Type' and calculate correlations

correlations_by_type = df.groupby('Type')[['Weight(kg)', 'Age']].corr()

print("\n correlation by type: ")

print(correlations_by_type)




# Task 5: Visualize the key findings from the data analysis

import matplotlib.pyplot as plt 

import seaborn as sns 

# Histograms

plt.figure(figsize=(12, 5))
plt.subplot(1,2,1)
sns.histplot(df['Weight(kg)'], kde=True, color='skyblue')
plt.title("Distribustions of Weight(kg)")
plt.xlabel("Weight(kg)")
plt.ylabel("Frequency")


plt.subplot(1,2,2)
sns.histplot(df['Age'], kde=True, color='salmon')
plt.title("Distribution of Age")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()



# Box plot

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(x='Animal', y='Weight(kg)', hue='Type', data=df, palette="Set3")
plt.title('Weight(kg) by Animal and Type')
plt.xticks(rotation=45, ha='right')

plt.subplot(1, 2, 2)
sns.boxplot(x='Animal', y='Age', hue='Type', data=df, palette="Set3")
plt.title('Age by Animal and Type')
plt.xlabel('Animals(Kg)')
plt.ylabel("Weight")
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()



# scatter plot
plt.figure(figsize=(8,6))
sns.scatterplot(x='Weight(kg)', y='Age', hue='Healthy', data=df, palette=['red', 'green'])
plt.title('Weight(kg) vs Age, Colored by Healthy status')
plt.xlabel('Weight(kg)')
plt.ylabel("Age")
plt.show()


# Bar chart for healthy /unhealthy propotions
plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
mammal_data = df[df['Type'] == 'Mammal'].groupby('Animal')['Healthy'].value_counts(normalize= True).unstack()
mammal_data.plot(kind= 'bar', stacked=True, color=['skyblue', 'salmon'], ax=plt.gca() )
plt.title("Mammal Healthy Proportions")


plt.subplot(1,2,2)
bird_data =  df[df['Type'] == 'Bird'].groupby('Animal')['Healthy'].value_counts(normalize=True).unstack()
bird_data.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'], ax=plt.gca() )
plt.title('Birds Healthy proposions')


plt.tight_layout()
plt.show()



# Heatmap 

plt.figure(figsize=(13,6))
correlation = df.groupby('Type')[['Weight(kg)', 'Age']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation (weight(kg )& Age) b Type')
plt.show()

