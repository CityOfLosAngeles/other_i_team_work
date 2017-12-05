# -*- coding: utf-8 -*-
import os
import pandas as pd
os.chdir('C:/Users/373659/Documents/GitHub/other_i_team_work/data')
staff = pd.read_csv('los_angeles_city_staff.csv')
staff = staff.sort_values(by=['DEPARTMENT_TITLE','ANNUAL_RATE'],ascending=False)

#female frame
staff_female = staff[staff['GENDER']=='Female']

#filtered frames for top department
def filtered_frames(df):
    return df.drop_duplicates(subset='DEPARTMENT_TITLE'),df.drop_duplicates(subset=['DEPARTMENT_TITLE','JOB_CLASS_TITLE'])

f_top_dept, f_top_position = filtered_frames(staff_female)
top_dept, top_position = filtered_frames(staff)

csv_names = ['f_top_dept','f_top_position','top_dept','top_position']
frame_list = [f_top_dept,f_top_position,top_dept,top_position]

os.chdir('C:/Users/373659/Documents/GitHub/other_i_team_work/outputs')
for item in range(4):
    frame_list[item].to_csv(csv_names[item]+'.csv')
    