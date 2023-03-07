from datetime import date, timedelta
import notion_df as nd
import pandas as pd
nd.pandas()


# Notion information needed for access to employee database
notion_token = "secret_omL8nzIdOZySUeAtSOCHm0bUNh2ydXdohuePKPBXkxm"
employee_db_id = "03764697bdf74f2b938313815cf62069"
ee_db_url = "https://www.notion.so/03764697bdf74f2b938313815cf62069?v=e856d446c1a44cfcb8857b014f591284"

# Define/Select the Excel file that we will use to output our reports


# Create a pandas dataframe from the employee database
ee_df = pd.DataFrame(nd.download(employee_db_id, api_key=notion_token))

# Create a report of the counts of employees per site
## Limit the dataframe to active employees
site_totals = ee_df[['EE Code', 'Home Base']][ee_df['Status']=='Active']
print(site_totals)


#Create a report of the empty positions per site
## select the position seat report and create a df

ps = pd.read_csv("/Users/tomiawodiya/Library/CloudStorage/OneDrive-Personal/Desktop/TOBOLA QA REVIEW/Data_Pulls/2023/2_February/2.27.23/positionseats.csv")

# Dataframe of the current empty positions
ps = ps[["Seat Number", "Incumbent", "Work Location"]][ps["Incumbent"].isnull()]
print(ps)

# Create a report of the new hires within the past 30 days
new_hire_report = pd.DataFrame(nd.download(employee_db_id, api_key=notion_token))
nhr = new_hire_report[["EE Code", "Full Name", "Hire Date"]][new_hire_report["Status"]=='Active']
nhr["Hire Date"] = pd.to_datetime(nhr["Hire Date"]).dt.date
days_before = pd.to_datetime(date.today()-timedelta(days=30))
nhr = nhr[nhr["Hire Date"]>=days_before]
print(nhr)

# Employees hired in the last 6 months (180 days)
l6m = new_hire_report[["EE Code", "Full Name", "Hire Date", "Termination Date"]]
l6m["Hire Date"] = pd.to_datetime(l6m["Hire Date"]).dt.date
months_before = pd.to_datetime(date.today()-timedelta(days=180))
l6m = l6m[l6m["Hire Date"]>=months_before]
print(l6m)


# Employees hired in the last 12 months (365 days)
last_year = new_hire_report[["EE Code", "Full Name", "Hire Date", "Termination Date"]]
last_year["Hire Date"] = pd.to_datetime(last_year["Hire Date"]).dt.date
months_before = pd.to_datetime(date.today()-timedelta(days=365))
last_year = last_year[(last_year["Hire Date"]>=months_before)]
print(last_year)