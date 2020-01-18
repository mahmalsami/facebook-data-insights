import pandas as pd


from pandas.io.json import json_normalize
import json
from datetime import datetime


#1.ADS
interactedAdvertiserList = pd.read_json (r'ads/advertisers_who_uploaded_a_contact_list_with_your_information_feedback.json')
print("Number of companies:", len(interactedAdvertiserList))

ds=interactedAdvertiserList["custom_audiences"].apply(pd.Series)
print(ds["value"].value_counts()/len(ds["value"])*100)

adsInteractions = pd.read_json (r"ads/advertisers_you've_interacted_with.json")
print("Number of ads interaction:",len(adsInteractions))

adsInterests = pd.read_json (r"ads/ads_interests.json")
print("Number of tracked ads topics :",len(adsInterests))



# 2.Location
# transfrom from JSON to GEOJSON for QGIS display purpose
#extacting frequency of extraction
frequency=[]
timestampArray=[]
rawJsonLocation = pd.read_json (r"location/location_history.json")
GeoJSONLocation = {
  "type": "FeatureCollection",
  "features": []}
i=0

for row in rawJsonLocation["location_history"]:
    #First I load the dict (one at a time)
	locationPoint={}

	locationPoint={
	  "type": "Feature",
	  "properties": {
    	"name": row['name'],
    	"timestamp": row['creation_timestamp']
	  },
	  "geometry": {
	    "type": "Point",
	    "coordinates": [row['coordinate']['longitude'], row['coordinate']['latitude']],
		}
	}
	#Timestamps seems unsorted, doing it manually
	timestampArray.append(row['creation_timestamp'])
	GeoJSONLocation["features"].append(locationPoint)

#Extracting info around location's timestamps
index=0
timestampArray.sort()

for row in timestampArray:
	diff=timestampArray[index]
	if index>1:
		diff=(timestampArray[index]-timestampArray[index-1])
	frequency.append(diff)
	index=index+1


#Extract location per timeslot (day, night)
#TODO


#Store all files
with open('location/location_parsed.json', 'w') as outfile:
    json.dump(GeoJSONLocation, outfile)
with open('location/frequency.json', 'w') as outfile:
    json.dump(frequency, outfile)


averageSeconds= sum(frequency) / float(len(frequency))
print("First location logged",datetime.fromtimestamp(GeoJSONLocation["features"][len(GeoJSONLocation["features"])-1]["properties"]["timestamp"]))
print("Last location logged",datetime.fromtimestamp(GeoJSONLocation["features"][0]["properties"]["timestamp"]))
print("Average of extractions in days",averageSeconds/(3600*24))
print("min frequency in seconds",min(frequency))
print("max frequency in days:",max(frequency)/(3600*24))






#Evaluate frequency of update. per month, year

#2.Comment
#Display in time + Subject extraction


#Likes & reactions




#Messages



#Others
	#Events, 

	#Following and followers

	#Friends
	#Groups
	#Photos
		#Would have expected some IA description


# for row in jsonData["custom_audiences"]:
#     #First I load the dict (one at a time)
# 	print(row)



##aadvertisers_you've_interacted_with
