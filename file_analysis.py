def get_year(line):
    try:
        return int(line.split('(')[1][:4])
    except ValueError:
        return 0
    except IndexError:
        pass


def get_place(line):
    temp = line.strip().split('\t')
    if temp[-1].startswith('('):
        temp = temp[-2]
    else:
        temp = temp[-1]

    temp = temp.strip()

    if temp.count(',') > 0:
        temp = temp.split(', ')[-2:]
        return ', '.join(temp)
    else:
        return temp


def get_name(line):
    try:
        return line.split('\"')[1]
    except IndexError:
        return line.split('(')[0][:-1]


def main(year):

    series_or_not = {}
    movies_by_locations = {}

    with open ("locations.list", 'r') as source:
        source = iter(source)
        line = next(source)
        while not line.startswith('==='):
            line = next(source)
        while True:
            try:
                line = next(source)
                if get_year(line) == year:
                    name = get_name(line)
                    place = get_place(line)
                    if place in movies_by_locations:
                        movies_by_locations[place].add(name)
                    else:
                        movies_by_locations[place] = set()
                        movies_by_locations[place].add(name)
                    series_or_not[name] = series_or_not.get(name, 0) + 1

            except StopIteration:
                break
            # except BaseException:
            #     pass

    return (series_or_not, movies_by_locations)


if __name__ == "__main__":
    main(1890)