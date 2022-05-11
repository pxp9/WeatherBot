# importing library
from pyowm.owm import OWM  
from pyowm.utils.config import get_default_config
import telegram
import main
import os

""" OPEN WEATHER MAP API KEY """
config_dict = get_default_config()
owm = OWM(os.environ['OPEN_WEATHER_MAP_API_TOKEN'])


""" FUNCTION TO GET WEATHER INFO AS A STRING THROW OPEN WEATHER MAP API """

def get_weather(city_str , default_LANG):

   city_text=""
   hour_text=""
   temp_max_text=""
   temp_min_text=""
   weather_status_text=""
   wind_speed_text=""
   precipitation_text=""
   if(default_LANG == main.SPANISH_LANG):
       config_dict['language'] = 'es'
       city_text=u'🏢'+" Ciudad: "
       hour_text=u'🕰'+" Hora de la medida: "
       temp_max_text=u'🌡'+" Temperatura máxima: "
       temp_min_text=u'🌡'+" Temperatura mínima: "
       weather_status_text=u'🌍'+" Estado general: "
       wind_speed_text=u'💨'+" Velocidad del viento: "
       precipitation_text=u'☔️'+" Probabilidad precipitación: "
       
   elif(default_LANG == main.ENGLISH_LANG):
       config_dict['language'] = 'en'
       city_text=u'🏢'+" City: "
       hour_text=u'🕰'+" Measurement time: "
       temp_max_text=u'🌡'+" Maximum temperature: "
       temp_min_text=u'🌡'+" Minimum temperature: "
       weather_status_text=u'🌍'+" General Status: "
       wind_speed_text=u'💨'+" Wind Speed: "
       precipitation_text=u'☔️'+"Precipitation probability: "
 
   mgr = owm.weather_manager()
   reg = owm.city_id_registry()

   list_of_locations=[] 
   city={}
   
   list = city_str.split(",")

   try: 
    if(len(list) == 1):
        list_of_locations = reg.locations_for(city_str)
        city = list_of_locations[0]
    else:
        list_of_locations = reg.locations_for(city_name=list[0] , country=list[1].upper())
        city = list_of_locations[0]
   except:
       if(default_LANG == main.ENGLISH_LANG):
           return "ERROR maybe city is not valid try to rewrite it" 
       elif(default_LANG == main.SPANISH_LANG):
           return "ERROR puede que la ciudad no sea válida prueba a reescribirla"     
   

   city_id = city.id

   lat = city.lat

   lon = city.lon
       
   weather = mgr.weather_at_place(city_str).weather
   switcher ={
            "humo":u'🌫',
            "smoke":u'🌫',
            "lluvia y nieve":u'🌨',
            "rain and snow":u'🌨',
            "snow":u'🌨',
            "nieve":u'🌨',
            "lluvia de gran intensidad":u'🌧 🌧 🌧',
            "heavy intensity rain":u'🌧 🌧 🌧',
            "lluvia ligera": u'🌧',
            "light rain": u'🌧',
            "lluvia moderada": u'🌧 🌧',
            "chubasco": u'🌧 🌧',
            "moderate rain": u'🌧 🌧',
            "algo de nubes":u'🌤',
            "few clouds":u'🌤',
            "cielo claro":u'☀️',
            "clear sky":u'☀️',
            "nubes dispersas":u'⛅️',
            "scattered clouds":u'⛅️',
            "muy nuboso":u'☁️☁️☁️☁️',
            "broken clouds":u'☁️☁️☁️☁️',
            "nubes":u'🌥',
            "overcast clouds":u'🌥' , 
            "tormenta con lluvia":u'⛈ ' ,
            "lluvia muy fuerte": u'🌧 🌧 ' , 
            "very heavy rain":u'🌧 🌧 🌧' 
            }
   status_text= str(weather.detailed_status)
   if(status_text == "rain and snow" and default_LANG == main.SPANISH_LANG):
        status_text ='lluvia y nieve'+" "+switcher['lluvia y nieve']
   else:
        status_text += " "+switcher[status_text] 

   current_str_weather = city_text+city_str+"\n"+hour_text+weather.reference_time('iso')[0:16]+"\n"+temp_max_text+str(weather.temperature('celsius')['temp_max'])+" Cº"+"\n"+temp_min_text+str(weather.temperature('celsius')['temp_min'])+" Cº"+"\n"+weather_status_text+status_text+"\n"+wind_speed_text+str(round(weather.wind('km_hour')['speed'] , 2))+" km/h"+"\n\n"


   daily_forecast = mgr.one_call(lat,lon).forecast_daily
   i = 0 
   
   forecast_str_weather=""
   while(i<8):

        forecast_str_weather += "=="*5+str(daily_forecast[i].reference_time('iso')[0:10])+"=="*5+"\n\n"  
        forecast_str_weather += temp_max_text+str(daily_forecast[i].temperature('celsius')['max'])+" Cº\n"

        forecast_str_weather += temp_min_text+str(daily_forecast[i].temperature('celsius')['min'])+" Cº\n"

        status_text= str(daily_forecast[i].detailed_status)
        
        if(status_text == "rain and snow" and default_LANG == main.SPANISH_LANG):
            status_text ='lluvia y nieve'+" "+switcher['lluvia y nieve']
        else:
            status_text += " "+switcher[status_text]
        
        forecast_str_weather += weather_status_text+status_text+"\n"

        forecast_str_weather += wind_speed_text+str(round(daily_forecast[i].wind('km_hour')['speed'],2))+" km/h\n"

        
        forecast_str_weather += precipitation_text+str(int(daily_forecast[i].precipitation_probability*100))+"%\n\n"

        i += 1

    
   return current_str_weather +forecast_str_weather

def city_valid(city:str):
        reg = owm.city_id_registry()
        list_of_locations = reg.locations_for(city)
        city = list_of_locations[0]
 
