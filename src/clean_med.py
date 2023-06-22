import pandas as pd
import numpy as np
import normalize

data = pd.read_excel('/Users/micahbenson/mdc/mdc_nikita.xlsx', sheet_name="mdc_nikita", dtype=str)

people, school, med = normalize.normalize_all(data)


def lbs_to_kg(med, date):
    april_22 = med[med.index.get_level_values("Date")== date] 

    april_22.loc[:, "Weight"] = april_22.loc[:, "Weight"] * 0.45359237 #convert from lbs to kg

    med[med.index.get_level_values("Date")== date] = april_22
    return med

med = lbs_to_kg(med, "04/01/2022")
