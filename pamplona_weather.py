'''
Copyright (c) 2017 Víctor Ruiz Gómez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from datetime import datetime
from re import findall
from pyvalid import accepts
import sqlite3 as sqlite
from os.path import join, dirname
from weather import Weather

@accepts(datetime, (datetime, None))
def get_pamplona_weather_history(start, end = None):
    '''
    Obtiene mediciones meteorológicas históricas de la ciudad de Pamplona, Navarra entre
    las fechas indicadas como parámetros
    :param start: Es la fecha de inicio (una instancia de la clase datetime.datetime en formato UTC)
    :param end: Es la fecha de fin (una instancia de la clase datetime.datetime en formato UTC) Por defecto,
    se usará la fecha datetime.utcnow()
    :return: Devuelve un listado de informaciones meteorologicas entre las fechas establecidas
    (serán instancias de la clase weather.Weather)
    '''

    if end is None:
        end = datetime.utcnow()

    # Nos conectamos a la base de datos con la información meteorológica de Pamplona
    with sqlite.connect(join(dirname(__file__), 'data', 'pamplona-weather-history.db')) as pamplona_weather_db:
        cursor = pamplona_weather_db.cursor()

        attrs = ['description', 'conditions', 'temperature', 'min_temperature', 'max_temperature',
                       'atmospheric_sea_pressure', 'atmospheric_ground_pressure', 'humidity',
                       'wind_speed', 'wind_direction', 'clouds_level', 'rain_volume', 'snow_volume',
                       'timestamp']

        # Construimos la query
        query = 'SELECT {} FROM pamplona_weather_history WHERE timestamp BETWEEN ? AND ?'.format(
            ', '.join(attrs)
        )
        # Creamos los parámetros que pasaremos junto con la query
        params = [int(date.strftime('%s')) for date in [start, end]]

        # Ejecutamos la query
        cursor.execute(query, params)

        # Obtenemos el resultado
        registers = cursor.fetchall()

        # Procesamos el resultado.
        weather_history = []
        for register in registers:
            params = dict(zip(attrs, register))

            # Procesamos algunos parámetros
            params['timestamp'] = datetime.utcfromtimestamp(params['timestamp'])
            params['conditions'] = findall('[ ]*([^,]+)[ ]*,?', params['conditions'])

            weather = Weather(**params)
            weather_history.append(weather)

        return weather_history