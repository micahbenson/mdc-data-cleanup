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
med = med.sort_values(["Individual Id", "Date"])

med = med.set_index(["Individual Id", "Date"])

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

#Check bmi
med["Bmi Check"] = med["Weight"] / (med["Height"]/100)**2

with pd.ExcelWriter('~/mdc/mdc_clean.xlsx') as writer:  
    people.to_excel(writer, sheet_name='people')
    school.to_excel(writer, sheet_name='school')
    med.to_excel(writer, sheet_name='med_fairs')




