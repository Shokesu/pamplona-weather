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
'''
El siguiente ejemplo muestra como obtener información meteorológica de la ciudad de Pamplona
entre las fechas 6/7/2017 - 14/7/2017. Las distintas observaciones meteorológicas se agregan por
día y se muestra las condiciones meteorológicas que más han aparecido.
'''
from pamplona_weather import get_pamplona_weather_history
from datetime import datetime

if __name__ == '__main__':
    weather_history = get_pamplona_weather_history(
        start = datetime(year = 2017, month = 7, day = 6),
        end = datetime(year = 2017, month = 7, day = 15))

    conditions = {}

    for observation in weather_history:
        for condition in observation.get_conditions():
            if not condition in conditions:
                conditions[condition] = 1
            else:
                conditions[condition] += 1


    conditions = [condition for condition, count in sorted([entry for entry in conditions.items()],
                                              key = lambda entry:entry[1], reverse = True)]

    print('Most common weather conditions in Pamplona between 6/7/2017 and 15/7/2017')

    print('\n'.join(['{}º: {}'.format(position+1, conditions[position])
               for position in range(0, len(conditions))]))
