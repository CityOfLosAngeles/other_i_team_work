# -*- coding: utf-8 -*-
import os
import pandas as pd
os.chdir('C:/Users/373659/Documents/GitHub/other_i_team_work/data')
staff = pd.read_csv('los_angeles_city_staff.csv')
staff['EMPLOYMENT_DATE']= staff['EMPLOYMENT_DATE'].apply(lambda x: pd.to_datetime(x))

staff = staff.sort_values(by=['DEPARTMENT_TITLE','ANNUAL_RATE'],ascending=False)
staff_time = staff.sort_values(by=['DEPARTMENT_TITLE','JOB_CLASS_TITLE','EMPLOYMENT_DATE'])


#female frame
staff_female = staff[staff['GENDER']=='Female']
staff_female_time = staff_time[staff_time['GENDER']=='Female']

#filtered frames for top department
def filtered_frames(df):
    return df.drop_duplicates(subset='DEPARTMENT_TITLE'),df.drop_duplicates(subset=['DEPARTMENT_TITLE','JOB_CLASS_TITLE'])

f_top_dept, f_top_position = filtered_frames(staff_female)
f_top_dept_time, f_top_position_time = filtered_frames(staff_female_time)
top_dept, top_position = filtered_frames(staff)

csv_names = ['f_top_dept','f_top_position','top_dept','top_position','f_top_dept_time','f_top_position_time','city_f_all']
frame_list = [f_top_dept,f_top_position,top_dept,top_position,f_top_dept_time,f_top_position_time,staff_female_time]

os.chdir('C:/Users/373659/Documents/GitHub/other_i_team_work/outputs')
for item in range(len(csv_names)):
    frame_list[item].to_csv(csv_names[item]+'.csv')
    