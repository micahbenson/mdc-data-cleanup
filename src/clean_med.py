import pandas as pd
import numpy as np
import normalize
import clean
import datetime

data = pd.read_excel('../mdc/mdc_nikita.xlsx', sheet_name="mdc_nikita", dtype=str)

people, school, med = normalize.normalize_all(data)

med = med.reset_index()
med = med.dropna(subset="Individual Id")

med["Individual Id"] = med["Individual Id"].apply(lambda x: int(x) if pd.notna(x) else x)
med["Family Id"]= med["Family Id"].apply(lambda x: int(str.split(str(x), "family ")[1]) if "family " in str(x) else pd.NA)
#med = med.sort_values(["Individual Id", "Date"])
med = med.sort_values(["Date", "Individual Id"])

med = med.set_index(["Individual Id", "Date"])

new = pd.read_excel('../mdc/Altered_Cols.xlsx')

new["Date"] = new["Date"].dt.date

new = new.set_index(["Individual Id", "Date"])

all_new = new.drop(["Lung", "Heart", "Abdomen", "Pulse"], axis="columns")
to_update = new.drop(["Blood Pressure Accurate", "Soda"], axis="columns")

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
med["Glasses"] = med["Glasses"].apply(lambda x: True if "y" in str(x) else True if str(x).isnumeric() else False)

#Clean Abdomen 
med["Abdomen"] = med["Abdomen"].apply(lambda x: "healthy" if str(x) == "0" else x)

#Clean Risk 
#med["Risk"] = med["Risk"].apply(lambda x: "yes" if str(x) == "risk" else x)

#Clean Rootips 
med["Rootips"] = med["Rootips"].apply(lambda x: int(x) if pd.notna(x) else x)

#Clean Safe Risk Smoke Alcohol Fast
med[["Safe", "Risk", "Smoke", "Alcohol", "Fast"]] = med[["Safe", "Risk", "Smoke", "Alcohol", "Fast"]].applymap(lambda x: pd.NA if pd.isna(x) else False if "no" in str(x) else True)

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
    "Blood Pressure Accurate",	
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
#people["Family Role"] = people["Family Role"].apply(lambda x: pd.NA if pd.isna(x) else str(x).split(" ")[0])

people["Highest Education Level"] = people["Highest Education Level"].apply(
    lambda x: 
    "kindergarten" if "kinder" in str(x) else \
    "primary" if "prim" in str(x) in str(x) else \
    "secondary" if "sec" in str(x) else \
    "university" if "uni" in str(x) else \
    "preporatory" if "prep" in str(x) else \
    "none" if "no" in str(x) else \
    "other" if pd.notna(x) else x
    )

people["Relationship To Primary"] = people["Relationship To Primary"].apply(
    lambda x: 
    "child" if "hijo" in str(x) or "hija" in str(x) else \
    "parent" if "padre" in str(x) or "madre" in str(x) else \
    "sibling" if "hermano" in str(x) or "hermana" in str(x) else \
    "grandparent" if "abuelo" in str(x) or "abuela" in str(x) else \
    "grandchild" if "nieto" in str(x) or "nieta" in str(x) else \
    "primary" if "primary" in str(x) else \
    "spouse" if str(x) == "esposo" or str(x) == "esposa" else \
    "nephew/niece" if "sobrino" in str(x) or "sobrina" in str(x) or "nice" in str(x) or "nephew" in str(x) else \
    "other" if pd.notna(x) else x
)

people[["Feed A Family", "Super Saturday", "Education Program"]] = people[["Feed A Family", "Super Saturday", "Education Program"]].applymap(lambda x: True if str(x) == "true" else False if str(x) == "false" else x)

#people["Is Child"] = np.where(people["Is Child"] == "yes", True, False)

combined = med.reset_index().set_index("Individual Id").merge(people, on="Individual Id")
combined = combined.drop("Age", axis="columns")

def age_combined(date, birth):
    return date.year - birth.year - ((date.month, date.day) < (birth.month, birth.day))

dates = combined[["Date", "Birthdate"]]

combined["Age At Fair"] = dates.apply(lambda x: age_combined(x["Date"], x["Birthdate"]), axis=1)

combined = combined.reset_index().set_index(["Individual Id", "Date"]).sort_values(["Date", "Individual Id"])

people = people.drop([
    #"Name", 
   # "Address", 
   # "Phone Number", 
    "Is Child", 
    #"Birthdate",
    #"Family Role",
    #"Super Saturday", 
    #"Feed A Family", 
    #"Education Program",
    ], 
    axis="columns")
combined = combined.drop([
    #"Name", 
    #"Address", 
    #"Phone Number", 
    "Is Child", 
    #"Birthdate", 
    #"Family Role",
    #"Super Saturday", 
    #"Feed A Family", 
    #"Education Program",
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




