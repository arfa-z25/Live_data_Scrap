import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
cities = ["lahore" , "islamabad" , "murree" , "karachi" , "multan" , "faisalabad"]
#extracting the temperature value
import re

def extract_temp(temp_str):
    """Function to extract numeric temperature from string."""
    try:
        return int(re.search(r'\d+', temp_str).group())
    except AttributeError:
        return None  # Return None if no numeric value is found

def get_temperature(city):
    """Fetches the temperature from the given city's weather page and returns it."""
    url = f"https://www.timeanddate.com/weather/pakistan/{city}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the element containing the temperature (this may vary)
        temp_tag = soup.find('div', class_="h2")  # Update this selector as needed
        if temp_tag:
            temp_str = temp_tag.get_text(strip=True)
            return extract_temp(temp_str)
        return None  # If no temperature found, return None
    except requests.exceptions.RequestException:
        return None  # Return None if the request fails

def sorting(cities=[]):
    # Predefined top cities
    top_cities = ['lahore', 'karachi', 'islamabad', 'multan', 'faisalabad', 'murree']
    
    # Add user-entered cities to the list
    top_cities.extend(cities)
    
    # Dictionary to store city names with their temperatures
    city_temp_dict = {}
    
    # Extract temperatures for all cities and store them in the dictionary
    for city in top_cities:
        temp = get_temperature(city)
        if temp is not None:
            city_temp_dict[city] = temp
    
    # Sort the dictionary by temperatures (values)
    sorted_city_temp_dict = dict(sorted(city_temp_dict.items(), key=lambda item: item[1]))
    
    # Create a sorted list of city names based on temperatures
    sorted_list = list(sorted_city_temp_dict.keys())
    
    # Return the sorted list of city names
    return sorted_list
     
   
    
    

def calling(option):
    # Construct URL for the selected city
    url = f"https://www.timeanddate.com/weather/pakistan/{option}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract location and text data
    location = soup.find("h1")
    text_1 = soup.find("div", class_="h1")
    text_2 = soup.find("div", class_="h2")
    text_3 = soup.find("p")

    location_text = location.get_text(strip=True) if location else "Location Not Found"
    text_1_text = text_1.get_text(strip=True) if text_1 else ""
    text_2_text = text_2.get_text(strip=True) if text_2 else ""
    text_3_text = text_3.get_text(strip=True) if text_3 else ""

    combined_text = f"{location_text} {text_1_text}\t{text_2_text}\t{text_3_text}"
    st.subheader(combined_text)

    
    image_path = "https://c.tadst.com/gfx/citymap/pk-10.png?10"
    
    

    # Extract table data
    table_data = []
    table = soup.find('table', {'class': 'table'})  # Simplified class name
    if table:
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                data_row = [cell.get_text(strip=True).replace('\n', ' ') for cell in cells]
                table_data.append(data_row)

    # Build HTML structure for the table
    structure = f"""
    <html>
    
    <table border="4" style="width: 100%;">
        <tr>
            <th>Location</th>
            <td>{table_data[0][1] if table_data else 'N/A'}</td>
            <td rowspan="3"><img src="{image_path}" alt="map_location""></td>
        </tr>
        <tr>
            <th>Current Time</th>
            <td>{table_data[1][1] if len(table_data) > 1 else 'N/A'}</td>
        </tr>
        <tr>
            <th>Latest Report</th>
            <td>{table_data[2][1] if len(table_data) > 2 else 'N/A'}</td>
        </tr>
        <tr>
            <th>Pressure</th>
            <td>{table_data[4][1] if len(table_data) > 4 else 'N/A'}</td>
        </tr>
        <tr>
            <th>Humidity</th>
            <td>{table_data[5][1] if len(table_data) > 5 else 'N/A'}</td>
        </tr>
        <tr>
            <th>Dew Point</th>
            <td>{table_data[6][1] if len(table_data) > 6 else 'N/A'}</td>
        </tr>
    </table>
   
    </html>
    """
    st.markdown(structure, unsafe_allow_html=True)
 
 
 #display sorted   

# Define CSS for background image
background_image_css = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1581922819772-1cb6451adfc5?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
"""

# Title HTML
title_text = """
<html>
<h1 style="color: white; text-align: center; font-family: 'Arial', sans-serif; background: radial-gradient(circle at top left, #3e8ef7, #19398a, #050c4e); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    Weather Forecasting App
</h1>
</html>
"""





# Render custom HTML and CSS in Streamlit
st.markdown(title_text, unsafe_allow_html=True)
st.markdown(background_image_css, unsafe_allow_html=True)

# City selection
option = st.text_input("Search any city here..", )
button = st.button("Sort by temp")

    
# Handle city selection or default to Faisalabad
if option:
    option.lower()
    calling(option)
else:
    calling("faisalabad")
    
    
if button:
    sort = sorting(option)
    structure_sorted_cities = f""" 
<html>
<div class="main_div" style="display : flex ; gap : 30px ; border-radius:5px">
<div style="background-color : red ; color : white ; font-family: 'Arial', sans-serif; width:100% ; text-indent:6px ; font-size : 18px ; border-radius:2px">{sort[0]}</div>
<div style="background-color : orange; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px; border-radius:2px">{sort[1]}</div>
<div style="background-color : blue ; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">{sort[2]}</div>
<div style="background-color : purple; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">{sort[3]}</div>
<div style="background-color : brown ; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">{sort[4]}</div>
<div style="background-color : pink ; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">{sort[5]}</div>

</div>
</html>
"""    
    st.markdown(structure_sorted_cities ,unsafe_allow_html=True )
    
else:
     structure_cities = """ 
<html>
<div class="main_div" style="display : flex ; gap : 30px ; border-radius:5px">
<div style="background-color : red ; color : white ; font-family: 'Arial', sans-serif; width:100% ; text-indent:6px ; font-size : 18px ; border-radius:2px">Lahore</div>
<div style="background-color : orange; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px; border-radius:2px">Karachi</div>
<div style="background-color : blue ; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">Faisalabad</div>
<div style="background-color : purple; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">Rawalpindi</div>
<div style="background-color : brown ; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">Multan</div>
<div style="background-color : pink ; color : white ; font-family: 'Arial', sans-serif; width:100%;text-indent:6px;font-size : 18px;border-radius:2px">Murree</div>

</div>
</html>
"""   
     st.markdown(structure_cities , unsafe_allow_html=True)
        
