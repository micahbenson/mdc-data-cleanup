import clean
import pandas as pd
import numpy as np
import re
import datetime


def school(df): 
    children = df[df["Is Child"]=="yes"]

    school_df = children[[
        "Individual Id", 
        "Family Id",
        "School Status", 
        "Is Dropout", 
        "Fall Semester 2022", 
        "Summer School 2022", 
        "Spring Semester 2023",
    ]]
    return school_df

def people(df): 
    people_df = df[[
        "Family Id", 
        "Individual Id", 
        "Name", 
        "Gender", 
        "Birthdate",
        "Address",
        "Phone Number",
        "Is Child", 
        "Family Role", 
        ]]
    return people_df


def med_april_2023(df): 
    #get the columns specific to the fair
    df_april_2023 = df.iloc[:, 258:285]

    #Get rid of random spaces in the column names
    df_april_2023.columns = df_april_2023.columns.str.strip()

    #rename columns
    #Add dictionary of new col names... 
    new_col_names = {
        "4/23 Height" : "Height", 
        "4/23 Weight" : "Weight", 	
        "4/23 BMI" : "BMI",
        "4/23 fast" : "Fast",
        "4/23 BLD Su" : "Blood Sugar",	
        "4/23 Heart" : "Heart",
        "4/23 Lung" : "Lung",
        "4/23 BP" : "Blood Pressure",
        "4/23 Su/Drinks/Day" : "Su/Drinks/Day",	
        "4/23 O2" : "O2",
        "4/23 Pulse" : "Pulse",	
        "4/23 safe" : "Safe",
        "4/23 LMP" : "LMP",
        "4/23 alcohol" : "Alcohol",
        "4/23 smoke" : "Smoke",
        "4/23 Medical Notes" : "Medical Notes", 
        "4/23 Flouride" : "Flouride",
        "4/23 Oral Hygiene" : "Oral Hygiene",
        "4/23 Cavity Risk" : "Cavity Risk",
        "4/23 Cavitys" : "Cavities",
        "4/23 Fractures" : "Fractures",
        "4/23 Missing" : "Missing",	
        "4/23 SDF" : "SDF", 
        "4/23 Sealant" : "Sealant",
        "4/23 Filling" : "Filling",
        "4/23 Extractions" : "Extractions",
        "4/23 Notes" : "Dental Notes"
    }

    df_april_2023 = df_april_2023.rename(columns = new_col_names)
    df_april_2023["Date"] = datetime.date(2023, 4, 1)
    df_april_2023["Individual Id"] = df["Unique family number"]
    df_april_2023["Family Id"] = df["Family Water Number"]

    return df_april_2023

def med_nov_2022(df): 
    df_nov_2022 = df.iloc[:, 203:224]

    df_nov_2022.columns = df_nov_2022.columns.str.strip()

    new_col_names = {
        "11/22 Height" : "Height",
        "11/22 Weight" : "Weight",	
        "11/22 BMI" : "BMI",
        "11/22 BLD Su" : "Blood Sugar",
        "11/22 Heart" : "Heart",
        "11/22 Lung" : "Lung",
        "11/22 BP" : "Blood Pressure", 
        "11/22 Su/Drinks/Day" : "Su/Drinks/Day",
        "11/22 O2" : "O2",	
        "11/22 Pulse" : "Pulse",
        "11/22 NOTES" : "Medical Notes",
        "11/22 Flouride" : "Flouride",
        "11/22 Oral Hygiene" : "Oral Hygiene",
        "11/22 Cavity Risk" : "Cavity Risk",	
        "11/22 Cavitys" : "Cavities",
        "11/22 Fractures" : "Fractures",
        "11/22 Missing" : "Missing",
        "11/22 SDF" : "SDF",
        "11/22 Sealant" : "Sealant",
        "11/22 Filling" : "Filling",
        "11/22 Notes" : "Dental Notes"
    }

    df_nov_2022 = df_nov_2022.rename(columns = new_col_names)
    df_nov_2022["Date"] = datetime.date(2022, 11, 1)
    df_nov_2022["Individual Id"] = df["Unique family number"]
    df_nov_2022["Family Id"] = df["Family Water Number"]

    return df_nov_2022

def med_april_2022(df): 
    df_april_2022 = df.iloc[:, 99:122]

    df_april_2022.columns = df_april_2022.columns.str.strip()

    new_col_names = {
        "4/22 Weight" : "Height",
        "4/22 Height" : "Weight",
        "4/22 BMI" : "BMI", 
        "4/22 BLD Su" : "Blood Sugar", 
        "4/22 Heart" : "Heart",
        "4/22 Lung" : "Lung",
        "4/22 BP" : "Blood Pressure",
        "4/22 Su/Drinks/Day" : "Su/Drinks/Day",
        "4/22 O2" : "O2", 
        "4/22 P" : "Pulse",
        "4/22 NOTES" : "Medical Notes", 
        "4/22 Flouride" : "Flouride",
        "4/22 Oral Hygiene" : "Oral Hygiene",
        "4/22 Cavity Risk" : "Cavity Risk",	
        "4/22 Cavitys" : "Cavities",
        "4/22 Fractures" : "Fractures",
        "4/22 Missing" : "Missing",
        "4/22 SDF" : "SDF",
        "4/22 Sealant" : "Sealant",
        "4/22 Filling" : "Filling",
        "4/22 Notes" : "Dental Notes",
        "4/22 Glasses" : "Glasses",
        "4/22 Letters" : "Letters"
    }

    df_april_2022 = df_april_2022.rename(columns = new_col_names)
    df_april_2022["Date"] = datetime.date(2022, 4, 1)

    df_april_2022["Individual Id"] = df["Unique family number"]
    df_april_2022["Family Id"] = df["Family Water Number"]

    return df_april_2022

def med_nov_2021(df): 

    df_nov_2021 = df.iloc[:, 122:146]

    df_nov_2021.columns = df_nov_2021.columns.str.strip()

    new_col_names = {
        "11/21 - Weight" : "Weight",
        "11/21 - Height" : "Height",
        "11/21 - BMI" : "BMI",
        "11/21 - Blood Sugar" : "Blood Sugar",
        "11/21 - Breathing/heart/lung/abdomen" : "??",
        "11/21 - Sugar drinks per day" : "Su/Drinks/Day",
        "11/21 - med, vaccine, risk assess" : "?",	
        "11/21 - medical notes" : "Medical Notes",
        "11/21 - # of cavities" : "Cavities",
        "11/21 - # of rootips" : "Rootips",
        "11/21 - Missing teeth" : "Missing",
        "Received Silver Dioxide Flouride (SDF)" : "SDF",
        "11/21 - Dentation" : "Dentation",
        "11/21 - Oral Hygiene" : "Oral Hygiene", 
        "11/21 - Cavities Risk" : "Cavity Risk",
        "11/21 dental notes" : "Dental Notes",
        "11/21 - reading glasses" : "Reading Glasses",
        "11/21 prescription glasses" : "Perscription Glasses",
        "11/21 vision notes" : "Vision Notes",
        "11/21 Flouride" : "Flouride"
    }

    df_nov_2021 = df_nov_2021.rename(columns=new_col_names)
    df_nov_2021["Date"] = datetime.date(2021, 11, 1)

    df_nov_2021["Individual Id"] = df["Unique family number"]
    df_nov_2021["Family Id"] = df["Family Water Number"]

    return df_nov_2021


def med_may_2021(df):
    df_may_2021 = df.iloc[:, 147:170]

    df_may_2021.columns = df_may_2021.columns.str.strip()

    new_col_names = {
        "May 2021 Height" : "Height",
        "May 2021 Weight" : "Weight",     	
        "May 2021 BMI" : "BMI", 
        "May 2021 BP" : "Blood Pressure",
        "May 2021 Blood Sugar" : "Blood Sugar",
        "May 2021 Medication/Quantity" : "Medication",
        "May 2021 Heart Rhythm" : "Heart",
        "May 2021 Lung Sounds" : "Lung",
        "May 2021 Abdomen" : "Abdomen",
        "May 2021 Sugar Drinks per day" : "Su/Drinks/Day",
        "May 2021 Risk assessment - Safety" : "Risk",
        "May 2021 Inquire on Vaccines" : "Vaccine",
        "May 2021 Vision" : "Vision",
        "May 2021 Breathing" : "Breathing", 
        "May 2021 Meds Despensed" : "Meds Despensed",
        "May 2021 What meds despensed and dosge" : "Meds Type And Dose", 
        "May 2021 Follow-up" : "Follow Up",
        "May 2021 # of Baby Cavities": "Baby Cavities",	
        "May 2021 # of Adult cavities" : "Adult Cavities",
        "May 2021 # of Missing Teeth" : "Missing",	
        "Total cavities" : "Cavities",
        "May 2021 Recent Dentist Visit?" : "Recent Dentist Visit",
        "May 2021 Other Dental Needs" : "Dental Notes",
    }

    df_may_2021 = df_may_2021.rename(columns=new_col_names)
    df_may_2021["Date"] = datetime.date(2021, 5, 1)

    df_may_2021["Individual Id"] = df["Unique family number"]
    df_may_2021["Family Id"] = df["Family Water Number"]

    return df_may_2021


def normalize_all(df): 

    #adjust datatypes: 
    df = df.apply(lambda x: x.str.lower().str.strip() if x.dtype == object else x)

    #df["Unique family number"] = df["Unique family number"].apply(lambda x: int(x) if pd.notna(x) else x)
    #df = clean.clean_family(df, "Family Water Number")

    df = clean.clean_med(df)

    april_2023 = med_april_2023(df)
    april_2023 = clean.text_clean(april_2023)

    nov_2022 = med_nov_2022(df)
    nov_2022 = clean.text_clean(nov_2022)


    april_2022 = med_april_2022(df)
    april_2022 = clean.text_clean(april_2022)

    nov_2021 = med_nov_2021(df)
    nov_2021 = clean.text_clean(nov_2021)

    may_2021 = med_may_2021(df)
    may_2021 = clean.text_clean(may_2021)

    df = clean.clean_all(df)

    people_df = people(df)

    school_df = school(df)

    #Creating the merged medical fair dataframe
    april_2023 = april_2023.set_index(["Individual Id", "Date", "Family Id"])
    nov_2022 = nov_2022.set_index(["Individual Id", "Date", "Family Id"])
    april_2022 = april_2022.set_index(["Individual Id", "Date", "Family Id"])
    nov_2021 = nov_2021.set_index(["Individual Id", "Date", "Family Id"])
    may_2021 = may_2021.set_index(["Individual Id", "Date", "Family Id"])

    med_fairs = pd.concat([april_2022, april_2023, nov_2022, nov_2021, may_2021])
    #Drop if everything is NaN
    med_fairs = med_fairs.dropna(how="all", axis=0)

    numeric = ["Weight", "Height", "Bmi", "Blood Sugar", 
        "O2", "Pulse", "Cavities", "Fractures", "Missing", "Sdf"]

    med_fairs[numeric] = med_fairs[numeric].applymap(lambda x: str(x))
    med_fairs[numeric] = med_fairs[numeric].applymap(lambda x: (re.sub(r'^(.*?)\s.*', r'\1', x)))
    med_fairs[numeric] = med_fairs[numeric].applymap(lambda x: float(x) if x.replace(".", "").isnumeric() \
              else float((re.sub(r'[^.\d]', '', x))) if re.sub(r'[^\d]', '', x).isnumeric() else pd.NA)



    # with pd.ExcelWriter('~/mdc/mdc_people.xlsx') as writer:  
    #     people_df.to_excel(writer, sheet_name='people')
    #     school_df.to_excel(writer, sheet_name='school')
    #     april_2023.to_excel(writer, sheet_name='med_4_23')
    #     nov_2022.to_excel(writer, sheet_name='med_11_22')
    #     april_2022.to_excel(writer, sheet_name='med_4_22')
    #     nov_2021.to_excel(writer, sheet_name='med_11_21')
    #     may_2021.to_excel(writer, sheet_name='med_05_21')
    #     med_fairs.to_excel(writer, sheet_name='med_fairs')
    return people_df, school_df, med_fairs


data = pd.read_excel('/Users/micahbenson/mdc/mdc_nikita.xlsx', sheet_name="mdc_nikita", dtype=str)

#normalize_all(data)

print(data.shape)



## TO DO
# May 2021 data import
# Standardize data representation across med fairs 
# Apply all this to the real sheet after discussions with Jean/Nikita










