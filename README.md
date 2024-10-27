# Python  -  Pipeline for Premji Invest Assignment

** CICD with GIT **

## Pipeline 1: 
1. Data Sources: (search for only two keywords: HDFC, Tata Motors, fetch 5 latest articles for each ticker)
2. Data Source1: https://yourstory.com
3. Data Source2: https://finshots.in/
4. schedule: 7pm every working day

## Steps:
1. Fetch data (text data of article) from Data Source1, Data Source2
2. Do basic cleaning and processing (prepping/deduplication on title/text data for that ticker) on the data
3. Generate sentiment score for the company (assume a mock/dummy API which can be called for it with input as news text and response as float between 0 to 1)
4. Persist final score in some DB, Data Lake or anything of your choice, and anything else you may consider necessary (with justification)