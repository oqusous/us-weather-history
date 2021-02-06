# us-weather-history

## Content
The data in "us-weather-history" is a collection of weather data for the US cities of Charlotte (NC), Los Angeles (CA), Houston (TX), Indianapolis (IN), Jacksonville (FL), Chicago (IL), New York (NY), Philadelphia (PA), Phoenix(AZ) and Seattle (WA) for the dates between July 2014 to June 2015. The data shows:
- The maximum, minimum and average temperatures measured each day.
- The maximum, minimum and average temperatures recorded historically.
- The measured, historically recorded and average rain fall for each day.

The file us-weather-history.py uses Streamlit to build an App that has three exploratory plots aimed to understand the data. It allows the user to choose the city of interest from the set above to view the plots relative to its data.

The file "df.csv" is the cleaned compiled data which was done in the us-weather-history.ipynb notebook. The notebook also contains the same plots used in the Streamlit app.

## Launching the us-weather-history app

To view data, clone the repo and launch the us-weather-history.py file. Please ensure you have installed Streamlit library.

> pip install streamlit

In IDE's terminal and while in the directory of the folder, run the file using the code:

> streamlit run us-weather-history.py

This will hosted the locally using your default web browser (Firefox or Chrome are preferred) where you can choose which city you wish to view the plots for.

