# Import Libraries
import pandas as pd
import numpy as np
import os
import glob
import re
from datetime import datetime, date
import hashlib

# hashing for dob
def hashing(dob):
    hashed_dob = hashlib.sha256(dob.encode()).hexdigest()[:5]  # encode() converts the string into bytes to be accepted by the hash function. Then, take only first five hash digits.
    return hashed_dob

# Calculate age as of 1 Jan 2022
def age(dob):
    dob = datetime.strptime(dob, "%Y%m%d").date()
    as_of_year, as_of_day, as_of_month = 2022, 1, 1  # Given as_of_date = 1 Jan 2022
    as_of_age = as_of_year - dob.year - ((as_of_month,  as_of_day) < (dob.month, dob.day))
    return as_of_age > 18

time_now  = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')

# Read all application batch CSV files from current working directory
application_batch_files = pd.concat(map(pd.read_csv, glob.glob(os.path.join(os.getcwd() , "applications_dataset*.csv"))),axis=0, ignore_index=True)

# application_batch_files.isnull().values.any()

# Split name into first_name and last_name
'''
Name field has below set of values concat with space in sequence :
1) Dr. | Mr. | Mrs. | Miss. - Ignored
2) <First Name> - Extracted
3) <Last Name> - Extracted
4) Jr. | PhD | MD | DDS | DVM - Ignored, as it is repeated for mutiple names, looks like Degree / position and not part of name
'''
name_pattern = re.compile(r'^(\s+)?(Mrs(\.)|Miss(\.)|Mr(\.)?|Dr(\.))?(?P<FIRST_NAME>.+)(\s+)((?P<LAST_NAME>.+)(\s+)?(Jr(\.)|PhD|MD|DDS|DVM)?)$', re.IGNORECASE)
application_batch_files['first_name'] = application_batch_files['name'].apply(lambda x: name_pattern.match(x).group('FIRST_NAME') ).str.strip()
application_batch_files['last_name'] = application_batch_files['name'].apply(lambda x: name_pattern.match(x).group('LAST_NAME') ).str.strip()
application_batch_files['no_name'] = application_batch_files['name'].isna()

# Standardise birth date field format as 'YYYYMMDD'
'''pandas to_datetime() function with parameter 
dayfirst=True helps to standarise the date'''
application_batch_files['date_of_birth_clean'] = np.where(application_batch_files['date_of_birth'].str.contains('/'), pd.to_datetime(application_batch_files['date_of_birth']).dt.strftime('%Y%m%d'), pd.to_datetime(application_batch_files['date_of_birth'], dayfirst=True).dt.strftime('%Y%m%d'))

# Create a new field named above_18 based on the applicant's birthday
application_batch_files['above_18'] =  application_batch_files['date_of_birth_clean'].apply(age)

# perform validity checks :
application_batch_files['mobile_validation'] = (application_batch_files['mobile_no'].apply(lambda x: len(x)) == 8).astype(bool)  # length of the mobile number should be 8
application_batch_files['age_validation'] = application_batch_files['above_18'].astype(bool) # age above 18

email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|net)$', re.IGNORECASE) # email ends with @emailprovider.com or @emailprovider.net
application_batch_files['email_validation'] = application_batch_files['email'].apply(lambda x: True if re.match(email_pattern,x) else False).astype(bool)
Validation = application_batch_files['mobile_validation']  & application_batch_files['age_validation'] & application_batch_files['email_validation']

Successful_application = application_batch_files[Validation].reset_index(drop=True)
Unsuccessful_application = application_batch_files[~Validation].reset_index(drop=True)

# create membership IDs for successful applications
hashed_dob = Successful_application['date_of_birth_clean'].apply(hashing)
Successful_application['Membership_ID'] = Successful_application['last_name'] + '_' + hashed_dob



if not os.path.exists('Successful_application'):
   os.makedirs('Successful_application')

if not os.path.exists('Unsuccessful_application'):
   os.makedirs('Unsuccessful_application')

Successful_application.to_csv(os.path.join(os.getcwd(),'Successful_application', 'Successful_application_'+time_now +'.csv'), index=False)
Unsuccessful_application.to_csv(os.path.join(os.getcwd(),'Unsuccessful_application', 'Unsuccessful_application_'+time_now +'.csv'), index=False)



