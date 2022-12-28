import pdfplumber
import pandas as pd
import nums_from_string as nfs


def read_pdf(file_name: str, file_num: str):
    with pdfplumber.open('./'+file_name+'/111_2_'+file_num+'.PDF') as pdf:

        first_page = pdf.pages[0]
        tb = first_page.extract_table()

    with pdfplumber.open('./'+file_name+'/111_2_'+file_num+'.PDF') as pdf:

        first_page = pdf.pages[2]
        page2 = first_page.extract_table()

    # clean none value
    new_tb = []
    for row in tb:
        clean_row = [i for i in row if i]
        new_tb.append(clean_row)

    new_page2 = []
    for row_page2 in page2:
        clean_page2 = [j for j in row_page2 if j]
        new_page2.append(clean_page2)

    course_name = new_tb[0][1]
    teacher = new_tb[0][3]
    classes = new_tb[2][1]

    teachers_re = str()
    for teachers in teacher:
        teachers_re += teachers.replace('\n', '')

    if len(course_name) > 10:
        course_re = str()
        for course_re in course_name:
            course_re += course_name.replace('\n', '')
        course_name = course_re

        class_re = str()
        for class_re in classes:
            class_re += classes.replace('\n', '')
        classes = class_re

    number_list = []
    grade = []
    for i in range(0, len(new_page2)):
        for j in range(0, len(new_page2[i])):
            number_list.append(nfs.get_nums(new_page2[i][j]))

    # initialize parameters
    attendance = 0
    work = 0
    mid = 0
    final = 0
    other = 0

    size = len(number_list)
    grade = number_list[size-3]
    if len(grade) == 1:
        if grade[0] < 30:
            attendance = grade[0]
            work = 0
            mid = 0
            final = 0
            other = 0
        else:
            attendance = 0
            work = 0
            mid = 0
            final = 0
            other = grade[0]

    if len(grade) == 2:
        if grade[0] < 30:
            attendance = grade[0]
            work = 0
            mid = 0
            final = 0
            other = grade[1]
        else:
            attendance = 0
            work = 0
            mid = grade[0]
            final = grade[1]
            other = 0

    if len(grade) == 3:
        attendance = 0
        work = grade[0]
        mid = grade[1]
        final = grade[2]
        other = 0

    if len(grade) == 4:
        attendance = grade[0]
        work = grade[1]
        mid = grade[2]
        final = grade[3]
        other = 0

    full_course = [teachers_re, course_name, classes,
                   attendance, work, mid, final, other]
    return full_course


def read_out_all(fileName: str, front_num: str, start: int, end: int) -> list:

    course_collect = []
    for count in range(start, end):
        course_collect.append(read_pdf(fileName, front_num + str(count)))

    return course_collect


if __name__ == '__main__':

    course_name = str(input('enter course field: '))
    front = str(input('enter front_number: '))
    start = int(input('start number: '))
    end = int(input('end number: '))

    collected_course = read_out_all(course_name, front, start, end)

    print(collected_course)
    collected_course = pd.DataFrame(collected_course, columns=[
        'teacher', 'course_name', 'course_field', 'attendance', 'work', 'midterm', 'final', 'other'])
    collected_course.to_csv(course_name+'.csv')
