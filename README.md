# Cloud data warehouse for Sparkify Data

## About 

Sparkify is a fictional music application that store songs and users' activity logs in separate **JSON** files. When the application started to grow, it becomes extremely difficult for the company to handle and benefit from these files. The suggested solution is to start investing in cloud solution. In this project Amazon Web services will be used. 

## About Redshift

Fully manged cloud data warehouse, supports parallel processing. designed for large scale data storage and analysis. 

## Database design

Since the company deal with huge amount of data, **Star schema** database design is the perfect fit for this application cause it facilitates insert and update processes. The database consist of the following tables:

 - **Staging events** (Load log dataset)
 - **Staging songs** (Load songs dataset)
 - **Song play** (The fact table)
 - **Songs** (Dimensional table extracted from song_data files)
 - **Artists** (Dimensional table extracted from song_data files)
 - **Users** (Dimensional table extracted from log_data files)
 - **Time** (Dimensional table extracted from Timestamp column)

## User Manual:

To Run the codes do the following instructions in the same exact order

 1. Run IaC file till the cluster is up and running
 3. Open the terminal or bash in windows
 4. Write *python create_tables.py* then click enter to execute the commands
 5. Write *python etl.py* then wait until the processing is completed 
 6. Go to Amazon Redshift > Cluster > Query Editor> Preview Data to check if the data inserted successfully or not




Regards,
Noof Aleliwi