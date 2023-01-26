import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

df_lecture = pd.read_csv(
    './_General_courses/general_courses.csv', encoding='utf_8_sig')
df_lecture['teacher_course'] = df_lecture['teacher'] + \
    ' - ' + df_lecture['course_name']
df_lecture = df_lecture.reindex(columns=['id', 'teacher', 'course_name',
                                'teacher_course', 'assignment', 'report', 'test', 'in_group', 'attend'])
df_lecture['ratings'] = ''

types = ['assignment', 'report', 'test', 'in_group', 'attend']
s = []
for i in range(len(df_lecture)):
    for type in types:
        s.append(df_lecture.at[i, type])
    df_lecture.at[i, 'ratings'] = s
    s = []

types = ['assignment', 'report', 'test', 'in_group', 'attend']
s = []
features = {}
for i in range(1, len(df_lecture.index)):
    for type in types:
        s.append(df_lecture.at[i, type])
    features[df_lecture.at[i, 'teacher_course']] = s
    s = []


def recommend(course_name):
    temp = {}
    for course in features.keys():
        temp[course] = cosine_similarity(
            [features[course_name]], [features[course]])[0][0]
    temp.pop(course_name)
    top = sorted(temp.items(), key=lambda x: x[1], reverse=True)
    top = top[1:12]
    for i in range(10):
        print(top[i][0])


recommend('周厚文 - 半導體與生活')
Recommendation = recommend('周厚文 - 半導體與生活')
print(type(Recommendation))
