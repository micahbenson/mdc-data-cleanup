import pandas as pd
from src import clean_med

def test_lbs_to_kg():
    df = pd.DataFrame(
        {
            "Date" : ["04/01/2022", "04/01/2022", "04/01/2022", "03/23/2021"],
            "Weight" : [50, 30, 40, 20]
        }
    ).set_index("Date")

    soln = pd.DataFrame(
        {
            "Date" : ["04/01/2022", "04/01/2022", "04/01/2022", "03/23/2021"],
            "Weight" : [50*0.45359237, 30*0.45359237, 40*0.45359237, 20]
        }
    ).set_index("Date")

    pd.testing.assert_frame_equal(
        clean_med.lbs_to_kg(df, "04/01/2022"),
        soln
    )