# Case study explanation.
Given a `.zip` file that contains multiple CSVs, all the CSVs have data with the following columns:

| col name       | col format      | col desc                               |
|----------------|-----------------|----------------------------------------|
| uuid           | UUID (36 chars) | uuid of an order (primary key)         |
| restuuid       | UUID (36 chars) | uuid of a restaurant                   |
| user_uuid      | UUID (36 chars) | uuid of a user                         |
| orderdate      | date (%Y-%m-%d) | date of the order                      |
| is_group_order | bool            | shows if this was a group order or not |

calculate the following two KPIs:
1. overall monthly retenetion rate.
2. monthly retenetion rate by restaurant.

# Tech Stack choice
The zip file provided had three CSVs with a total size of less than 1 GB. this means we can **easily** do the following:
1. Extract the CSVs to disk.
2. Read each CSV in a [pandas DataFrame](https://pandas.pydata.org/).
3. Concat all DataFrames and carry out the needed transformations and get the KPIs.

But if we instead have 1000+ CSVs (extracted from an OLTP for example) with a total size exceeding that of the current machine's memory, the above solution would not work.

So as a proof of concept, another system was chosen as follows:
1. Read the CSVs line by line, validating each line according to a predefined schema and constraints (format mostly).
2. After reading a predefined batch size, upload all those rows to a SQL database. (thus we are using O(1) memory complexity for each batch)
3. Create indices on that SQL table to carry out transformation on scale easily.

Which the latter solution is still not **THE MOST OPTIMIZED**, it's a step above the first solution and has much better scalability.

# How to navigate this repo:
You can start with [main.ipynb](https://github.com/AndrewBasem1/Restaurant-retention-rate---data-engineering-case-study/blob/main/main.ipynb) this notebook will have the script logic laid down step by step. you'll find that I'm importing some libraries from other .py files, this is done to keep version control better, and to break down the code into seperate files with seperate functions to follow best practices.
