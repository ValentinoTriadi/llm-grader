from example import run_main_with_input
from read_data import (
    get_question_six_answers,
    get_question_six_grades,
    read_xlsx_to_dataframe,
)


seed = 123456

question6 = """Jawab dalam bahasa Indonesia. Ini menggunakan bahasa notal ITB.
Suatu ketika, kepala sekolah Monster University ingin mengetahui prestasi dari para monster pada kelas yang dibuka. Data setiap monster disimpan menggunakan tipe data yang terdefinisi  sebagai berikut. 

constant NMax : integer = 100 
 
{ NilaiMons: Nilai untuk monster dengan nomor id monster = ID, pada kelas berkode KodeKls, dengan nilai = Nilai } 
type NilaiMons : < ID : string,  
                   KodeKls : string,  
                   Nilai : integer[0..100] > 
 
{ Tabel berisi data nilai semua monster } 
type ArrNilai : < TNilai : array [1..NMax] of NilaiMons, { penampung data nilai monster } 
                  Neff : integer[0..NMax]  { Nilai efektif tabel, Neff=0 berarti tabel kosong } >  
 
{ Tabel berisi data nama-nama monster } 
type ArrNamaMonst : < TNM : array [1..Nmax+1] of string,  
                      Neff : integer[0..NMax] { Nilai efektif tabel, Neff=0 berarti tabel kosong } >

Untuk soal-soal berikut, tuliskan secara lengkap: definisi/header, spesifikasi, dan body/realisasi fungsi. Tidak diperkenankan membuat dan menggunakan type/fungsi/prosedur baru. 
Buatlah fungsi NilaiMaxKelas yang menerima input ArrNilai (misalnya T) dan kode kelas (misalnya KodeKls), kemudian mengembalikan nilai yang merupakan nilai tertinggi untuk kelas KodeKls. Jika array kosong atau jika KodeKls tidak ditemukan di array, dihasilkan nilai -1.
"""
question6_answers = get_question_six_answers(
    read_xlsx_to_dataframe("dataset/IF1210_01-Ujian Akhir Semester-responses.xlsx")
)
question6_grades = get_question_six_grades(
    read_xlsx_to_dataframe("dataset/IF1210_01-Ujian Akhir Semester-grades.xlsx")
)

answer_sample = question6_answers.sample(n=10, random_state=seed)
grade_sample = question6_grades.sample(n=10, random_state=seed)

answer_sample = answer_sample.reset_index(drop=True)
grade_sample = grade_sample.reset_index(drop=True)

for index, students in answer_sample.iterrows():
    print(f"Original grade: {grade_sample.loc[index]['Q. 6 /4.00']}")
    run_main_with_input(
        problem=question6,
        code=answer_sample.loc[index]["Response 6"],
        student_id=str(answer_sample.loc[index]["First name"]),
    )
