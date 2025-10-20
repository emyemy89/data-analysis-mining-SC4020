import pandas as pd

df = pd.read_csv("../raw/dataset.csv")
print('Head')
print(df.head())
print('Info')
print(df.info())
print('Is null')
print(df.isnull().sum())
print('Duplicated')
print(df.duplicated().sum())

# remove duplicates
df = df.drop_duplicates()

#normalize symptom names
symptom_num = [f'Symptom_{i}' for i in range(1, 18)]
for col in symptom_num:
    df[col] = df[col].str.lower().str.strip()

#convert each row to transactions
# just to ignore NaN
transactions = []
for _, row in df.iterrows():
    symptoms = [row[col] for col in symptom_num if pd.notnull(row[col])]
    transactions.append(symptoms)

# consider synonyms
synonyms = {'pyrexia': 'fever', 'skin_rash': 'rash'}
for col in symptom_num:
    df[col] = df[col].replace(synonyms)

# should return true for no NaNs
print('are there no NaNs?'+ str(all(pd.notnull(item) for t in transactions for item in t)))

# should return true for no duplicates
print('are there no duplicates?'+str(all(len(t) == len(set(t)) for t in transactions)))

print(transactions[:5])


# Now save the clean thing to a new csv file
df_cleaned = pd.DataFrame({
    'Disease': df['Disease'],
    'Symptoms': [';'.join(t) for t in transactions]
})

# Save to CSV in the same directory
df_cleaned.to_csv('./dataset_cleaned.csv', index=False)

print("Cleaned dataset saved to data/cleaned/dataset_cleaned.csv")

