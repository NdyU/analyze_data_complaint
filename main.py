import requests
import pandas
from pandas.io.json import json_normalize
import json

r = requests.get("https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$select= *, COUNT(complaint_type) AS complaint_count&$where=created_date between '2017-01-01T12:00:00' and '2018-01-01T14:00:00'&$group=complaint_type&$order=complaint_count DESC&$limit=10")

r = requests.get("https://data.cityofnewyork.us/resource/fhrw-4uyv.json?&$where=created_date between '2017-01-01T12:00:00' and '2018-01-01T14:00:00'")
data_json = r.json()

complaint_in_nyc_2017 = json_normalize(data_json)

complaint_type = complaint_in_nyc_2017['complaint_type']

complaint_type_top_10 = complaint_type.value_counts().head(10)
list_complaint_type_top_10 = complaint_type.value_counts().head(10).index.tolist()

print(list_complaint_type_top_10)
filter_complaint_top_10 = complaint_in_nyc_2017['complaint_type'].isin(list_complaint_type_top_10)

complaint_top_10 = complaint_in_nyc_2017[filter_complaint_top_10]

unique_boroughs = complaint_top_10['borough'].unique()

print(unique_boroughs)

for borough in unique_boroughs:
    borough_filter = complaint_top_10['borough'] == borough
    complain_by_borough = complaint_top_10[borough_filter]
    borough_complain_freqs = complain_by_borough['complaint_type'].value_counts()
    print('\nCommon Complaint Counts for ' + borough + ':')
    print(borough_complain_freqs);
