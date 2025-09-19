import pandas as pd


def read_xlsx_to_dataframe(path: str) -> pd.DataFrame:
    """
    Reads all sheets from an Excel file and returns them
    as a single pandas DataFrame (merged).
    """
    all_sheets = pd.read_excel(path, sheet_name=None)

    df = pd.concat(all_sheets.values(), ignore_index=True)
    return df


def get_question_six_answers(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Surname", "First name", "Email address", "Response 6"]]


def get_question_six_grades(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Surname", "First name", "Email address", "Q. 6 /4.00"]]


if __name__ == "__main__":
    file_path = "dataset/IF1210_01-Ujian Akhir Semester-responses.xlsx"
    answers_df = read_xlsx_to_dataframe(file_path)
    grades_df = read_xlsx_to_dataframe(
        "dataset/IF1210_01-Ujian Akhir Semester-grades.xlsx"
    )

    print(get_question_six_answers(answers_df))
    print(get_question_six_grades(grades_df))
