# b4-demo-day-g1, webapp for Rmotr Python Class
uTakeout  

## General
When we think about the Quality of nearby takeout, often what comes to mind is the quality of Food. However, when faced with the prospect of walking or driving, different considerations must be made, such as the safety of the area, accessibility of the area, or the travel time to a given restuarant. uTakeout seeks to bridge these factors and provide a comprehensive review of the quality and accessibility of takeout around a given address.

## How uTakeout Works
1. The user enters their address on the home page and presses "Go"
2. The address is geocoded into a lat/lon through the Google Geocode API 
3. The lat/lon is then used to query Yelp for the nearest 40 restaurants and relevent information is extracted from each
4. The travel distance from the given address is then calculated against each restaurant 3 times - once for walking, once for driving in no traffic, and once for driving in heavy traffic (Monday at 6:00pm). 
5. The home location is then matched to the nearest police agency (straight line distance) that reports crime statistics to the FBI and those statistics are extracted
6. The home location is then matched to a "Land Use Mix" statistic based on zip-code
7. All statistics gathered are then analyzed and combined into 3 letter grades that range from F to A+ that provide comprehensive reviews of all factors as they relate to food quality, walkability, and driveability.
8. The user is then presented with all gathered information along with a map of the restaurants and links to their yelp pages. 

-No data is stored from the user or any API calls

### Optional Future Features

+ Add Walk and Drive time histograms 
+ Change Crime Statistics to Robbery, Larceny and Auto Theft
+ Implement dynamic weighting that redistributes the factor weight according to how far away the police agency is
+ Change layout to 1-2-1-map (now it’s 1-3-map)
+ Build JS popup box that explains the LUM and Box Plots 
+ Map travel distances to restaurants (refactor distance collection process)
+ Improve restaurant grading
+ Implement Overall grade
+ Add "methodology" page that gives descriptions for each factor and describes scoring system

### Completed:
+ Convert given address into lat/lon
+ Gather yelp restuarants
+ Gather travel times for walking/driving_good/driving_bad
+ Build database for housing crime and LUM statistics
+ Communicate with database for crime and lum
+ Create boxplot using matlibplot to display travel information succinctly 
+ Build grading formula for factor analysis
+ Convert grades into 0-100 scale and subsequent letter grades
+ Show map of all restaurants in relation to home
+ Display restaurant info in table
+ Add button-disable to prevent multiple form submissions
+ Error catch invalid addresses and prevent subsequent API calls
+ Add "About" page that gives more detail and explains what the website is
