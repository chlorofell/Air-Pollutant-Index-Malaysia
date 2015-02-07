Sorry the code is messy.

Step 1: Run prepDB to ensure your DB is up to date. You'll need to manually change the variables D1 and D2 as the start and end date of the test.
Step 2: Run "RUNAPIScan.py" , the default is 3 scanners, which means there will be 3 concurrent processes scrapping data from the website.
Step 3: You can run generateCSVs.py to generate readings by each region.

In the next version, I'll make it so step 1 isn't necessary---promise.

ReadingsByRegion.zip has the readings broken by region from August 2013, till Feb-2015. 


The API.SQL file already has all the readings will Feb-2015, so you don't need to run this process for all the days prior to that. You can also perform your analysis.

