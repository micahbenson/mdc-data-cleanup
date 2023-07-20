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

all_new = new.drop(["Lung", "Heart", "Abdomen", "Pulse"], axis="columns")
to_update = new.drop(["Blood Pressure 1", "Blood Pressure 2", "Blood Pressure 3", "Soda"], axis="columns")

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

#Make pd.NA where should be
med = med.where(med != "?", pd.NA)
med = med.where(med != "not taken", pd.NA)

#Calculate bmi
med["Bmi"] = med["Weight"] / (med["Height"]/100)**2

#Calc sugar grams per day
med["Soda Sugar"] = med["Soda"] * 108 / 7

#Clean glasses column 
med["Glasses"] = med["Glasses"].apply(lambda x: "yes" if "y" in str(x) else "yes" if str(x).isnumeric() else "no")

#Clean Abdomen 
med["Abdomen"] = med["Abdomen"].apply(lambda x: "healthy" if str(x) == "0" else x)

#Clean Risk 
med["Risk"] = med["Risk"].apply(lambda x: "yes" if str(x) == "risk" else x)

#Clean Rootips 
med["Rootips"] = med["Rootips"].apply(lambda x: int(x) if pd.notna(x) else x)

#Clean Safe Risk Smoke Alcohol Fast
med[["Safe", "Risk", "Smoke", "Alcohol", "Fast"]] = med[["Safe", "Risk", "Smoke", "Alcohol", "Fast"]].applymap(lambda x: pd.NA if pd.isna(x) else "no" if "no" in str(x) else "yes")

#Clean cavity risk
med["Cavity Risk"] = med["Cavity Risk"].apply(lambda x: "medium" if "m" in str(x) else "medium" if "fair" in str(x) else x)

#Clean oral hygiene 
med["Oral Hygiene"] = med["Oral Hygiene"].apply(lambda x: "fair" if str(x) == "fair/good" else x)

#Clean Vaccine
med["Vaccine"] = med["Vaccine"].apply(lambda x: "yes all" if "yes" in str(x) and "all" in str(x) else "some past two years" if "2" in str(x) else x)

#Replace 0s with "none"
med[["Sealant", "Filling", "Extractions"]] = med[["Sealant", "Filling", "Extractions"]].where(med[["Sealant", "Filling", "Extractions"]] != "0", "none")

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
    "Family Id", 
    "Letters", 
    "Sealant",
    "Abdomen"
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
    "Blood Pressure 1",
    "Blood Pressure 2",
    "Blood Pressure 3",	
    "Blood Sugar",
    "Medication",
    "Vaccine",
    "Lmp",
    "Medical Notes",
    "Cavities",
    "Cavity Risk",
    "Oral Hygiene",
    "Dentation",
    "Missing",
    "Fractures",
    "Flouride",
    "Sdf",
    "Filling",
    "Extractions",
    "Rootips",
    "Dental Notes",
    "Glasses",
    "Vision",
    "Vision Notes",
    "Soda",
    "Soda Sugar",
    "Exercise",
    "Fast",
    "Alcohol",
    "Smoke",
    "Safe",	
    "Risk",
]]

people = people[people["Individual Id"].isin(med.index.get_level_values("Individual Id").to_list())]
people = people.set_index("Individual Id")

def age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

#convert to date
people["Birthdate"] = pd.to_datetime(people["Birthdate"]).dt.date

people["Age"] = people["Birthdate"].apply(age)

#Remove numbers from children in family role
people["Family Role"] = people["Family Role"].apply(lambda x: pd.NA if pd.isna(x) else str(x).split(" ")[0])

#people["Is Child"] = np.where(people["Is Child"] == "yes", True, False)

combined = med.reset_index().set_index("Individual Id").merge(people, on="Individual Id")
combined = combined.drop("Age", axis="columns")

def age_combined(date, birth):
    return date.year - birth.year - ((date.month, date.day) < (birth.month, birth.day))

dates = combined[["Date", "Birthdate"]]

combined["Age At Fair"] = dates.apply(lambda x: age_combined(x["Date"], x["Birthdate"]), axis=1)

combined = combined.reset_index().set_index(["Individual Id", "Date"]).sort_values(["Date", "Individual Id"])

people = people.drop([
    "Name", 
    "Address", 
    "Phone Number", 
    "Is Child", 
    "Birthdate"
    ], 
    axis="columns")
combined = combined.drop([
    "Name", 
    "Address", 
    "Phone Number", 
    "Is Child", 
    "Birthdate"
    ], 
    axis="columns")

with pd.ExcelWriter('~/mdc/mdc_clean.xlsx') as writer:  
    people.to_excel(writer, sheet_name='people')
    #school.to_excel(writer, sheet_name='school')
    med.to_excel(writer, sheet_name='med_fairs')
    combined.to_excel(writer, sheet_name='combined')

med.to_csv('./data/med.csv')
people.to_csv('./data/people.csv')
combined.to_csv('./data/combined.csv')




