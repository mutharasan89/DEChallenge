# Senior Data Enginer Tech Challenge
---
This test is split into 5 sections:
1. Data Pipelines
2. Databases 
3. System Design
4. Charts & APIs
5. Machine Learning

---
## Section1: Data Pipelines

Mandatory to setup python environments by installing packages using requirements.txt file

The script is supposed to run in the foresaid created environment.

- Ingest.py will copy the files from IN folder and ingest to HDFS with proper naming standard
- datapipeline.py will read all the files together as dataframe from HDFS, then undergo cleaning process, specific transformation as mentioned in section-1, data validation checks and then successful applicants and unsuccessful applicant's processed data are stored into seperate folder. Later, processed file names are logged seperately, so in upcoming batch run system will have information about processed files names and thereby script will pick only new files for processing

Processed files are saved under corresponding folder with naming convention provided below:

./Successful_application/Successful_application_YYYY_MM_DD_hh_mm_ss.csv
./Unsuccessful_application/Unsuccessful_application_YYYY_MM_DD_hh_mm_ss.csv

Cron job is set as per below [onetime setup] which runs every one hour on daily basis.

- Launch terminal in server and then open crontab file by using below command
 <br>`crontab -e`
- Add a task to crontab to schedule shell script hourly
 <br>`0 * * * * <path to current working directory>/workflow.sh`

Assumption : Cron is already installed. Python env is setup already using requirements.txt file.
