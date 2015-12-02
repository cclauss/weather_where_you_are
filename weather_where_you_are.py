# Inspired by: https://github.com/kultprok/pythonista-drafts-recipes/blob/master/weatherdata/weatherdata.py
''' Print out current weather at your current location. '''
import location, requests, time
def getLocation():
    location.start_updates()
    time.sleep(1)
    currLoc = location.get_location()
    location.stop_updates() # stop GPS hardware ASAP to save battery
    return currLoc

your_loc = location.reverse_geocode(getLocation())[-1]
# import pprint ; pprint.pprint(your_loc) # useful for debugging
# See: http://bugs.openweathermap.org/projects/api/wiki
fmt = 'http://api.openweathermap.org/data/2.5/weather?q={City},+{State},+{CountryCode}'  # &units=metric'
url = fmt.format(**your_loc).replace(' ', '+')
print(url)
weather = requests.get(url).json()
if weather:
    # import pprint ; pprint.pprint(weather) # useful for debugging
    for item in ('temp_min', 'temp_max'):
        weather['main'][item] = weather['main'].get(item, None)  # create values if they are not present
    # weather is optional in weather!!
    weather['weather'] = weather.get('weather', [ {'description' : 'not available'} ])
    for item in ('sunrise', 'sunset'):
        weather['sys'][item] = time.ctime(weather['sys'][item]).split()[3] # just time, not date
    print('''Current weather at {name}, {sys[country]} is {weather[0][description]}.
        Temprature: {main[temp]}c ({main[temp_min]}c / {main[temp_max]}c) (min / max)
        Pressure: {main[pressure]} hPa
        Humidity: {main[humidity]}%
        Sunrise: {sys[sunrise]}
        Sunset: {sys[sunset]}
        Weather information provided by openweathermap.org'''.format(**weather))
