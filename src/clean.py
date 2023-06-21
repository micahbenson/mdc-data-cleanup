import pandas as pd 
import numpy as np

def text_clean(df): 
    df = df.apply(lambda x: x.str.lower().str.strip() if x.dtype == object else x)
    df.columns = df.columns.str.title().str.strip()
    return df

def encode_if_word(df, cols, word, yes, no): 
    for col in cols:
        df[col] = df[col].apply(lambda x: yes if word in str(x) else no)
    return df

def clean_fall_semester_2022(df, name): 
    col = df[name]
    col = col.apply(lambda x: "yes" if "attend" in str(x) else x)
    col = np.where(col == "yes", "yes", "no")
    df[name] = col
    return df

def clean_summer_school_2022(df, name): 
    col = df[name]
    col = col.apply(lambda x: "yes" if "attend" in str(x) else "no")
    df[name] = col
    return df

def clean_spring_semester_2023(df, name): 
    col = df[name]
    col = col.apply(lambda x: "yes" if str(x) == "attend" else "no")
    df[name] = col
    return df

def is_child(df, name, new): 
    col = df[name]
    col = col.apply(lambda x: "yes" if "child" in str(x) else "no")
    df[new] = col
    return df

def clean_dropout(df, name, new): 
    col = df[name]
    list = ["in school", "in school (preschool)", "in school (kinder)"]
    col = col.apply(lambda x: "yes" if x in list else "no")
    df[new] = col
    return df

def clean_super_saturday(df, name): 
    col = df[name]
    some = ["sometimes", "past"]
    yes = ["yes", "ss"]
    col = col.apply(lambda x: "yes" if str(x) in yes else ("some" if str(x) in some else "no"))
    df[name] = col
    return df

def clean_2021_pic(df, name): 
    col = df[name]
    col = col.apply(lambda x: "yes" if "yes" in str(x) else "no")
    df[name] = col
    return df

def clean_weight_loss(df, name): 
    col = df[name]
    col = col.apply(lambda x: "yes" if str(x) == "yes" else "no")
    df[name] = col
    return df

def clean_high_risk(df, name): 
    col = df[name]
    list = ["yes", "depression", "depression 1", "high risk family"]
    col = col.apply(lambda x: "yes" if str(x) in list else "no")
    df[name] = col
    return df


def clean_heart(df, name): 
    col = df[name]
    col = col.apply(lambda x: "regular" if str(x) == "r" else("irregular" if str(x) == "i" else x))
    df[name] = col
    return df

def clean_flouride(df, name_list): 
    cols = df[name_list]
    cols = cols.applymap(lambda x: "yes" if str(x) == "y" else "yes" if str(x) == "yes" else x)
    df[name_list] = cols
    return df


def clean_hygiene(df, name): 
    col = df[name]
    col = col.apply(lambda x: "poor" if str(x) == "p" else "fair" if str(x) == "f" else "good" if str(x) == "g" else "excellent" if str(x) == "e" else x)
    df[name] = col
    return df

def clean_cavity_risk(df, name): 
    col = df[name]
    col = col.apply(lambda x: "low" if str(x) == "l" else "medium" if str(x) == "m" else "high" if str(x) == "h" else x)
    df[name] = col
    return df

def clean_med(df): 
    df = clean_heart(df, "4/22 Heart")
    df = clean_flouride(df, ["11/21 Flouride", "11/22 Flouride", "4/23 Flouride", "Flouride"])
    df = clean_hygiene(df, "4/22 Oral Hygiene")
    df = clean_cavity_risk(df, "4/22 Cavity Risk")
    return df


def clean_all(df):
    drop = [
        'Picture 2021', #link to a pic in dropbox
        'Picture 2022', 
        'Ticket Number', #not important
        "# of botellas", 
        "Feria de medico 5/21", #Duplicate
        "Feria de medico 11/21", #Duplicate
        "4/22 med fair", #Duplicate
        "Invite april 2023 med fair", #Duplicate
        "Family never attended a medical fair", 
        "EDAD", #Should just be calculated after data extraction, 
        "adult or child number", 
        "Attends School", #empty
        "Attendance", #meaningless
        ]

    df = df.drop(columns=drop) #Drop unneded columns
    df = df.drop(df.index[543:549]) #Remove empty rows
    df = text_clean(df) #Clean text format

    df = clean_fall_semester_2022(df, "Fall Semester 2022")
    df = clean_spring_semester_2023(df, "Spring Semester 2023")
    df = clean_summer_school_2022(df, "Summer School 2022")
    df = clean_super_saturday(df, "Super Saturday")
    df = clean_weight_loss(df, "Weight Loss")
    df = clean_2021_pic(df, "Attended Pic Day 2021")
    df = clean_dropout(df, "Dropped Out Of School", "Is Dropout")
    df = is_child(df, "Relacion", "Is Child")

    #Add dictionary of new col names... 
    new_col_names = {
        "Family Water Number" : "Family ID",
        "Unique Family Number" : "Individual ID",
        "Relacion" : "Family Role",
        "Fecha De Ignicio Agua" : "Water Start Date",
        "Dropped Out Of School" : "School Status", 
        "Work Program" : "Work Program",
        "Señas" : "Dreams", 
        "Género" : "Gender",
        "Paciente" : "Name", 
        "Fecha Nacimiento" : "Birthdate", 
        "Numero De Telefono" : "Phone Number",
        "Domicilio": "Address"
    }

    df = df.rename(columns = new_col_names)
    return df


data = pd.read_excel('/Users/micahbenson/Downloads/mdc_main_data.xlsx', dtype=str)
df = clean_all(data)