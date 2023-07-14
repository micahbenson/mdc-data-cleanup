import pandas as pd
import numpy as np
import normalize
import clean
import datetime

data = pd.read_excel('/Users/micahbenson/mdc/mdc_nikita.xlsx', sheet_name="mdc_nikita", dtype=str)

people, school, med = normalize.normalize_all(data)

med = med.reset_index()
med = med.dropna(subset="Individual Id")

med["Individual Id"] = med["Individual Id"].apply(lambda x: int(x) if pd.notna(x) else x)
med["Family Id"]= med["Family Id"].apply(lambda x: int(str.split(str(x), "family ")[1]) if "family " in str(x) else pd.NA)
#med = med.sort_values(["Individual Id", "Date"])
med = med.sort_values(["Date", "Individual Id"])

med = med.set_index(["Individual Id", "Date"])

new = pd.read_excel('/Users/micahbenson/mdc/Altered_Cols.xlsx')

new["Date"] = new["Date"].dt.date

new = new.set_index(["Individual Id", "Date"])

all_new = new.drop(["Lung", "Heart", "Abdomen"], axis="columns")
to_update = new.drop(["Blood Pressure 1", "Blood Pressure 2", "Blood Pressure 3", "Soda L/Wk"], axis="columns")

med = med.merge(all_new, on=["Individual Id", "Date"])
med.update(to_update)
print(med)
#Function to convert units
def convert_units(med, dates, col, conversion):
    for date in dates:
        df = med[med.index.get_level_values("Date")== date] 
        df.loc[:, col] = df.loc[:, col] * conversion 
        med[med.index.get_level_values("Date")== date] = df
    return med


#unit conversions: 
lbs_to_kg = 0.45359237
in_to_cm = 2.539999962
ft_to_cm = 30.48

#Dates to convert
lbs_to_kg_dates = [datetime.date(2021, 11, 1), datetime.date(2021, 5, 1)]
in_to_cm_dates = [datetime.date(2021, 5, 1)]
ft_to_cm_dates = [datetime.date(2021, 11, 1)]

#Do the conversions
med = convert_units(med, lbs_to_kg_dates, "Weight", lbs_to_kg)
med = convert_units(med, in_to_cm_dates, "Height", in_to_cm)
med = convert_units(med, ft_to_cm_dates, "Height", ft_to_cm)

#Calculate bmi
med["Bmi"] = med["Weight"] / (med["Height"]/100)**2

#Calc sugar grams per day
med["Soda Sugar g/day"] = med["Soda L/Wk"] * 108 / 7

#Clean glasses column 
med["Glasses"] = med["Glasses"].apply(lambda x: "yes" if "y" in str(x) else x)

#Clean Abdomen 
med["Abdomen"] = med["Abdomen"].apply(lambda x: "normal" if len(str(x)) <= 2 else x)

#Clean Risk 
med["Risk"] = med["Risk"].apply(lambda x: "yes" if str(x) == "risk" else x)

#Rootips 
med["Rootips"] = med["Rootips"].apply(lambda x: int(x) if pd.notna(x) else x)

to_drop = [
    "11/21 Blood Pressure", 
    "Reading Glasses",
    "Meds Despensed",
    "Meds Type And Dose",
    "Baby Cavities",
    "Adult Cavities",
    "Recent Dentist Visit",
    "Body",
    "Breathing", 
    "Blood Pressure", 
    "Su/Drinks/Day", 
    "Family Id"
    ]

med = med.drop(to_drop, axis="columns")

#order the df 
med = med[[
    "Height", 
    "Weight",
    "Bmi",
    "O2",
    "Pulse",
    "Heart",
    "Lung",
    "Abdomen",
    "Blood Pressure 1",
    "Blood Pressure 2",
    "Blood Pressure 3",	
    "Blood Sugar",
    "Medication",
    "Vaccine",
    "Lmp",
    "Follow Up",
    "Medical Notes",
    "Cavities",
    "Cavity Risk",
    "Oral Hygiene",
    "Dentation",
    "Missing",
    "Fractures",
    "Flouride",
    "Sdf",
    "Sealant",
    "Filling",
    "Extractions",
    "Rootips",
    "Dental Notes",
    "Glasses",
    "Letters",
    "Vision",
    "Vision Notes",
    "Soda L/Wk",
    "Soda Sugar g/day",
    "Exercise",
    "Fast",
    "Alcohol",
    "Smoke",
    "Safe",	
    "Risk",
]]

people = people[people["Individual Id"].isin(med.index.get_level_values("Individual Id").to_list())]
people = people.set_index("Individual Id")

people = people.drop(["Name", "Address", "Phone Number", "Is Child"], axis="columns")

#convert to date
#people["Birthday"] = people["Birthdate"].dt.date

with pd.ExcelWriter('~/mdc/mdc_clean.xlsx') as writer:  
    people.to_excel(writer, sheet_name='people')
    #school.to_excel(writer, sheet_name='school')
    med.to_excel(writer, sheet_name='med_fairs')




