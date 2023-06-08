import pandas as pd 
import numpy as np

def text_clean(df): 
    df = df.apply(lambda x: x.str.lower().str.strip() if x.dtype == object else x)
    df.columns = df.columns.str.title().str.replace("\n", " ").str.strip()
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
    col = col.apply(lambda x: "no" if str.isnumeric(x) else "yes")
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

df = pd.read_excel('/Users/micahbenson/Downloads/mdc_main_data.xlsx', dtype=str)
drop = ['Picture 2021', 'Picture 2022', 'Ticket Number', "Relacion", "# of botellas", 
        "Feria de medico 5/21", "Feria de medico 11/21", "4/22 med fair", 
        "Invite april 2023 med fair", "Family never attended a medical fair"]
df = df.drop(columns=drop)
df = text_clean(df)

df = clean_fall_semester_2022(df, "Fall Semester 2022")
df = clean_spring_semester_2023(df, "Spring Semester 2023")
df = clean_summer_school_2022(df, "Summer School 2022")
df = clean_super_saturday(df, "Super Saturday")
df = clean_weight_loss(df, "Weight Loss")
df = clean_2021_pic(df, "Attended Pic Day 2021")
df = clean_dropout(df, "Dropped Out Of School", "Is Dropout")

#df = is_child(df, "Adult Or Child Number", "Is Child")

print(df)
