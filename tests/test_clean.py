import pandas as pd
from src import clean

# def test_encode_if_word():
#     df = pd.DataFrame(
#                 {
#                     "A": ["xxxdog", "xsdfds", "doijg"],
#                     "B": ["dogsdff", "sdfdogfsd", "fdsdfds"],
#                     "C": ["a", "b", "c"]
#                 }
#             )
#     soln = pd.DataFrame(
#                 {
#                     "A": [1, 0, 0],
#                     "B": [1, 1, 0],
#                     "C": ["a", "b", "c"]
#                 }
#             )
#     pd.testing.assert_frame_equal(
#         clean.encode_if_word(df, ["A", "B"], "dog", 1, 0),
#         soln
#     )

def test_text_clean(): 
    df = pd.DataFrame(
                {
                    "fav\nfruit  ": ["Apples", " baNnAnas", " blue Berries"],
                    "fAv VEG": ["CarroT", "OlIVE", "pepper"],
                }
            )
    soln = pd.DataFrame(
                {
                    "Fav Fruit": ["apples", "bannanas", "blue berries"],
                    "Fav Veg": ["carrot", "olive", "pepper"]
                }
            )
    pd.testing.assert_frame_equal(
        clean.text_clean(df),
        soln
    )

def test_clean_fall_semester_2022(): 
    df = pd.DataFrame(
                {
                    "Fall Semester 2022": ["parent", "yes", "attend", pd.NA],
                }
            )
    soln = pd.DataFrame(
                {
                    "Fall Semester 2022": ["no", "yes", "yes", "no"]
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_fall_semester_2022(df, "Fall Semester 2022"),
        soln
    )

def test_clean_summer_school_2022(): 
    df = pd.DataFrame(
                {
                    "Summer School 2022": ["attend", pd.NA],
                }
            )
    soln = pd.DataFrame(
                {
                    "Summer School 2022": ["yes", "no"]
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_fall_semester_2022(df, "Summer School 2022"),
        soln
    )

def test_clean_spring_semester_2023(): 
    name = "Spring Semester 2023"
    df = pd.DataFrame(
                {
                    name: ["attend", pd.NA, "parent, child attends"],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["yes", "no", "no"]
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_spring_semester_2023(df, name),
        soln
    )

def test_is_child(): 
    name = "Adult Or Child Number"
    new = "is_child"
    df = pd.DataFrame(
                {
                    name: ["a", "1", "b", "2"],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["a", "1", "b", "2"],
                    new: ["yes", "no", "yes", "no"]
                }
            )
    pd.testing.assert_frame_equal(
        clean.is_child(df, name, new),
        soln
    )

def dropout(): 
    name = "Dropped Out Of School"
    new = "is_in_school"
    df = pd.DataFrame(
                {
                    name: [
                        "not in school", 
                        "in school", 
                        "too young",
                        "is a nurse"
                        "in school (preschool)"
                        "not in school, working"
                        "in school (kinder)", 
                        pd.NA]
                }
            )
    soln = pd.DataFrame(
                {
                    name: [
                        "not in school", 
                        "in school", 
                        "too young",
                        "is a nurse"
                        "in school (preschool)"
                        "not in school, working"
                        "in school (kinder)"
                        ],
                    new: ["no", "yes", "no", "no", "yes", "no", "yes", "no"],
                }
            )
    pd.testing.assert_frame_equal(
        clean.is_child(df, name, new),
        soln
    )

def test_is_child(): 
    name = "Adult Or Child Number"
    new = "is_child"
    df = pd.DataFrame(
                {
                    name: ["a", "1", "b", "2"],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["a", "1", "b", "2"],
                    new: ["yes", "no", "yes", "no"]
                }
            )
    pd.testing.assert_frame_equal(
        clean.is_child(df, name, new),
        soln
    )

def test_super_saturday(): 
    name = "Super Saturday"
    df = pd.DataFrame(
                {
                    name: ["ss", "no", "yes", "past","sometimes", pd.NA],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["yes", "no", "yes", "some", "some", "no"],
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_super_saturday(df, name),
        soln
    )

def test_clean_2021_pic(): 
    name = "2021 Pic Attendance"
    df = pd.DataFrame(
                {
                    name: ["yes", "no", pd.NA, "yes https://www.dropbox.com/s/ngnpdgqnm7mfpuy/_MG_2255%281%29.JPG?dl=0"],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["yes", "no", "no", "yes"],
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_2021_pic(df, name),
        soln
    )

def test_weight_loss(): 
    name = "Weight Loss"
    df = pd.DataFrame(
                {
                    name: ["yes", pd.NA],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["yes", "no"],
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_2021_pic(df, name),
        soln
    )

def test_high_risk(): 
    name = "High Risk"
    df = pd.DataFrame(
                {
                    name: ["yes", pd.NA, "depression", "depression 1", "high risk family"],
                }
            )
    soln = pd.DataFrame(
                {
                    name: ["yes", "no", "yes", "yes", "yes"],
                }
            )
    pd.testing.assert_frame_equal(
        clean.clean_high_risk(df, name),
        soln
    )


