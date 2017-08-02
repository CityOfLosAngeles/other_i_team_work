import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc,classification_report

police_officer_class = ['POLICE OFFICER I','POLICE OFFICER II','POLICE OFFICER III',
                                       'MUNICIPAL POLICE OFFICER I','MUNICIPAL POLICE OFFICER II',
                                      'MUNICIPAL POLICE OFFICER III']

sgt_and_above = ['POLICE LIEUTENANT I',
                                         'POLICE LIEUTENANT II',
                                         'POLICE SERGEANT I',
                                        'POLICE SERGEANT II',
                                        'POLICE COMMANDER',
                                        'POLICE CAPTAIN I',
                                        'POLICE CAPTAIN II',
                                        'POLICE CAPTAIN III',
                                        'POLICE DEPUTY CHIEF I',
                                        'MUNICIPAL POLICE SERGEANT',
                                        'MUNICIPAL POLICE LIEUTENANT',
                                        'MUNICIPAL POLICE CAPTAIN I',
                                         'MUNICIPAL POLICE CAPTAIN II',
                                         'POLICE DEPUTY CHIEF II',
                                        'CH OF POLICE']
detective = ['POLICE DETECTIVE I','POLICE DETECTIVE II','POLICE DETECTIVE III']

def ethnicity_reclassfication(df,column='ETHNIC CODE'):
    eth_descr = {1:'Black',
           2:'Hispanic',
           3:'Asian_Filipino',
           4:'Caucasian',
           5:'American Indian',
           6:'Other',
           7:'Asian_Filipino',
           9: 'K-9'}

    return df[column].map(eth_descr)
def job_class_broad(df):
    job_class_broad = pd.Series(np.where(df['JOB_JOB_CLASS_TITLE'].isin(police_officer_class),
                                         'Police Officer', df['JOB_JOB_CLASS_TITLE']))

    job_class_broad = pd.Series(np.where(job_class_broad.isin(sgt_and_above),'Sgt and Above',job_class_broad))

    job_class_broad = pd.Series(np.where(job_class_broad.isin(detective),'Detective',job_class_broad))

    job_class_broad= pd.Series(np.where(~job_class_broad.isin(['Police Officer','Sgt and Above','Detective']),'Other',job_class_broad))

    return job_class_broad

def dummy_variable(df,field):
    return pd.get_dummies(df[field],prefix='dum')

def model_evaluation(model,X_test_set,y_test_set):
    """
    model = Model that has already be instantiated and first
    X_test_set = Array, Matrix or DataFrame representing X_test values
    y_test_set = Array representing Y_test values (response variable)
    """
    pred_flag = model.predict_proba(X_test_set)[:,1]>.7
    print (pd.crosstab(y_test_set,pred_flag))
    print ('-----------------------------------------------')
    print (classification_report(y_test_set,pred_flag))

def roc_score(model,X_test_set,y_test_set):
    """
    model = Model that has already be instantiated and first
    X_test_set = Array, Matrix or DataFrame representing X_test values
    y_test_set = Array representing Y_test values (response variable)
    """
    y_pred = model.predict_proba(X_test_set)[:,1]
    fpr,tpr,thresholds = roc_curve(y_test_set,y_pred)
    roc_auc=auc(fpr,tpr)
    print ("Area under the ROC curve : %f" % roc_auc)

def df_model_evaluation(model_name,train_field):
    coefficients = model_name.coef_.reshape(model_name.coef_.shape[1])
    return pd.DataFrame({'Variables':(train_field.columns),'Coefficients':coefficients})

def train_splitting(df,test_size=.3):
    """
    Faster way for using different dataframe to implement sci-kit learn's test train split
    """
    y = df.ix[:,0]
    X = df.ix[:,1:]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X_train, X_test, y_train, y_test

def ssn_convert(df_,ssn_col):

    string_length = [len(str(df_[ssn_col][x])) for x in range(len(df_))]
    string_frame= pd.DataFrame({'orig_4':df_[ssn_col],'len':string_length})

    def reclass_len(df):
        if df['len']==4:
            return df['orig_4']
        elif df['len']==3:
            return str('0')+str(df['orig_4'])
        elif df['len']==2:
            return str('00')+str(df['orig_4'])
        elif df['len']==1:
            return str('000')+str(df['orig_4'])

    return string_frame.apply(reclass_len,axis=1).astype('str')
