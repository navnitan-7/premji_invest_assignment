# Python  -  Pipeline for Premji Invest Assignment


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

## Pipeline 2: schedule: 8pm every working day:
1. Condition: skip if pipeline 1 has failed/not completed on same day run
2. Data Source : https://grouplens.org/datasets/movielens/, ml-100k.
3. Metadata and other details are given there. http://files.grouplens.org/datasets/movielens/ml-100k-README.txt
  
### create 4 tasks,
  1. Find the mean age of users in each occupation
  2. Find the names of top 20 highest rated movies. (at least 35 times rated by Users)
  3. Find the top genres rated by users of each occupation in every age-groups. age-groups can be defined as 20-25, 25-35, 35-45, 45 and older
  4. Given one movie, find top 10 similar movies. The similarity calculation can change according to the algorithm.
  Described below is one way of finding similar movies. You can define your own algorithm.
  Finding the most similar movies based on user ratings.
  users   movie    rating 
  U1      M1       R1
  U2      M1       R2
  U1      M2       R3
