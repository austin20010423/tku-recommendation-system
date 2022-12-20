import pdfplumber
import pandas as pd
import nums_from_string as nfs


def read_pdf(file: str):
    with pdfplumber.open('./course_pdf/111_2_'+file+'.PDF') as pdf:

        first_page = pdf.pages[0]
        tb = first_page.extract_table()

    with pdfplumber.open('./course_pdf/111_2_'+file+'.PDF') as pdf:

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

    course_re = str()
    for course_re in course_name:
        course_re += course_name.replace('\n', '')

    class_re = str()
    for class_re in classes:
        class_re += classes.replace('\n', '')

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

    full_course = [teachers_re, course_re, class_re,
                   attendance, work, mid, final, other]
    return full_course


if __name__ == '__main__':
    course_collect = []
    for count in range(64, 84):
        course_collect.append(read_pdf('31'+str(count)))

course_collect = pd.DataFrame(course_collect)
print(course_collect)
course_collect.to_csv('out.csv')
