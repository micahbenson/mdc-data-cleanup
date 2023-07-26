import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
from ydata_profiling.visualisation.plot import timeseries_heatmap
import datetime

med = pd.read_csv("./data/med.csv")
people = pd.read_csv("./data/people.csv")
combined= pd.read_csv("./data/combined.csv")

med23 = med[med["Date"] == str(datetime.date(2023, 4, 1))]

profile = ProfileReport(combined, title="MdC Medical Data Report")
profile.to_file("/Users/micahbenson/mdc/profiling_report.html")