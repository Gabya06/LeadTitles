# LeadTitles
Repository for code to update title scores on new leads and contacts in SalesForce

The title score is a score between 0 and 100 that is populated on a lead in order to help SDRs prioritize which leads to focus on. 
It makes up 50% of the Eloqua score used to score Marketing sourced leads. 

On the server, there is a cron job that runs every 5 minutes and triggers the script to query SalesForce for new unconverted leads with titles that have not been scored yet. 
If a new and unconverted lead with a title is found, the title is scored based on the title score matrix.
To calculate the score for a lead, the title must first be cleaned, parsed and separated into job level and title, and then matched against the target title matrix. 
The target title matrix is a lookup matrix where the score can be found based on job level and title. It is updated with titles from attendees at events and seminars on data governance. 
The target title file contains best titles targeted and keywords which are matched against the lead title for scoring. 

When scoring the lead title, there are a few possible cases that are taken into account:
* If the lead title matches a combination of job level and target title then it is scored based on the target title matrix. 
* If there is no job level, 'Individual contributor' is assigned as the job level and the score is based on the combination of Individual contributor and target title
* If the lead title doesn't match any of the target titles, then the title score starts at 50 and points are added or subtracted based on keywords (BCBS239, CCAR …), job titles and job levels found in the title.
