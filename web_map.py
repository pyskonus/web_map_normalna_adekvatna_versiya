import folium


def read_year():
    # This functions reads the year and processes al the exceptions
    try:
        year = int(input("Type in the year: "))
        if year <= 0:
            print("The input must be positive")
            return

    except ValueError:
        print("The input must be an integer")
        return

    return year


def search_for_coord(place):
    # This function gets a string value that represents a place name and
    # searches for its coordinates in a specific file.
    with open("coordinates.list", 'r') as THEFILE:
        THEFILE = iter(THEFILE)
        while True:
            try:
                line = next(THEFILE)
                temp = line.strip().split('\t')
                if temp[0] == place:
                    return [float(temp[1].split(' ')[0]), float(temp[1].split(' ')[1])]
            except StopIteration:
                return []


def main():
    # Read the year
    year = read_year()
    if not year:
        return

    from geopy.geocoders import MapBox
    geolocator = \
        MapBox(api_key='pk.eyJ1IjoicHlza29zeWsiLCJhIjoiY2pyd2R4Y25vMGFzZTN5b2FhdGo2b29laiJ9.JudhuawYhM1Pwx5qTMcrnQ')
    f = open("coordinates.list", 'a')
    import file_analysis
    movies_to_amount = file_analysis.main(year)[0]
    place_to_movie = file_analysis.main(year)[1]

    myMap = folium.Map(location=[49.817545, 24.023932], zoom_start=4)

    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                    encoding='utf-8-sig').read(),
                    style_function=lambda x: {'fillColor': 'green'
                    if x['properties']['POP2005'] < 10000000
                    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                    else 'red'}))
    fg_series = folium.FeatureGroup(name="Series")
    fg_films = folium.FeatureGroup(name="Films")

    for place in place_to_movie:
        message_s = ''
        message_f = ''
        coordinates = search_for_coord(place)
        if not coordinates:
            try:
                coordinates = [geolocator.geocode(place).latitude, geolocator.geocode(place).longitude]
                f.write(place + '\t' + str(coordinates[0]) + ' ' +
                        str(coordinates[1]) + '\n')
            except BaseException:
                continue

        Sum = 0
        films_set = set()

        for movie in place_to_movie[place]:
            if movies_to_amount[movie] < 5:
                message_f += movie + '</br>'
                films_set.add(movie)

            else:
                message_s += movie + ' (' + str(movies_to_amount[movie]) + ' series)' + '</br>'
                Sum += movies_to_amount[movie]

        message_s = message_s[:-1]
        message_f = message_f[:-1]

        if message_s:
            if Sum == 1:
                tooltip_s = 'One episode has been shot here'
            else:
                tooltip_s = str(Sum) + ' ' + "episodes have been shot here"
            fg_series.add_child(folium.Marker(coordinates,
                                              popup=message_s,
                                              tooltip=tooltip_s,
                                              icon=folium.features.CustomIcon('series_icon.png',
                                                                              icon_size=(25, 25))))
        if message_f:
            if len(films_set) == 1:
                tooltip_f = "One film has been shot here"
            else:
                tooltip_f = str(len(films_set)) + ' ' + "films have been shot here"
            fg_films.add_child(folium.Marker(coordinates,
                                             popup=message_f,
                                             tooltip=tooltip_f,
                                             icon=folium.features.CustomIcon('film_icon.png',
                                                                             icon_size=(25, 25))))

    myMap.add_child(fg_pp)
    myMap.add_child(fg_series)
    myMap.add_child(fg_films)
    myMap.add_child(folium.LayerControl())

    f.close()

    myMap.save("Films_map.html")


main()
