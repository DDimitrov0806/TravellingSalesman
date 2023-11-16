import random
import math
import csv

CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2

class Route():
    def __init__(self,cities: list) -> None:
        self.cities = cities
        #Overall distance 
        self.distance = self.calculate_distance()
    
    def calculate_distance(self):
        distance = 0
        for index in range(len(self.cities) - 1):
            #Calculate distance between two cities
            distance += math.sqrt((self.cities[index+1][1] - self.cities[index][1])**2 + (self.cities[index+1][2] - self.cities[index][2])**2)

        return distance
    
def crossover(route):
    #Randomly choose 4 routes from the original routes and get the best of them
    #These will be our 2 parents from which we will create 2 childrens using crossover
    parent_cities_1 = sorted(random.choices(route, k=4), key=lambda x: x.distance)[0].cities.copy()
    parent_cities_2 = sorted(random.choices(route, k=4), key=lambda x: x.distance)[0].cities.copy()

    #Get what part of the parents will be the same
    stopper = random.randint(0, len(parent_cities_1)-2)
    children_1 = parent_cities_1[0:stopper]
    children_2 = parent_cities_2[0:stopper]

    #If a city is not in the child, add it
    for city in parent_cities_1:
        if city not in children_2:
            children_2.append(city)
    
    for city in parent_cities_2:
        if city not in children_1:
            children_1.append(city)

    return children_1, children_2

def mutation(cities):
    #Determine which positions will be swapped 
    index1 = random.randint(0, len(cities)-1)
    index2 = random.randint(0, len(cities)-1)

    cities[index1], cities[index2] = cities[index2], cities[index1]

    return cities

def print_best_route(routes):
    best_route = sorted(routes, key=lambda x: x.distance)[0]
    print("Best route: ", [city[0] for city in best_route.cities])
    print("Distance length:", best_route.distance)

def genetic_algorithm(route: list):
    generation_iteration = len(route)
    for generation in range(10000):
        sorted_route = sorted(route, key=lambda x: x.distance)
        new_route = []
        new_route.append(sorted_route[0])
        new_route.append(sorted_route[1])

        #On every iteration we will generate 2 new routes and we already picked 2 of the best current routes
        for i in range(generation_iteration):
            if random.random() < CROSSOVER_RATE:
                new_cities_1, new_cities_2 = crossover(route)
            else:
                new_cities_1 = random.choice(route).cities.copy()
                new_cities_2 = random.choice(route).cities.copy()

            if random.random() < MUTATION_RATE:
                new_cities_1 = mutation(new_cities_1)
                new_cities_2 = mutation(new_cities_2)
            
            new_route.append(Route(new_cities_1))
            new_route.append(Route(new_cities_2))

        route = new_route

        if generation % 1000 == 0:
            print_best_route(route)


if __name__ == "__main__":
    '''
    #This will be needed for the presentation
    cities_name_file = "uk12_name.csv"
    cities_coords_file = "uk12_xy.csv"

    cities_names = []
    with open(cities_name_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            cities_names.append(row[0])

    cities_coords = []
    with open(cities_coords_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            cities_coords.append((float(row[0]), float(row[1])))

    cities = [(x, y[0], y[1]) for x,y in zip(cities_names, cities_coords)]
    cities_count = len(cities)

    '''
    
    cities_count = int(input())

    cities = []
    for city_id in range(cities_count):
        x = random.randint(0,1000)
        y = random.randint(0,1000)
        cities.append((str(city_id), float(x), float(y)))

    routes = []
    for _ in range(cities_count):
        cities_copy = cities.copy()
        random.shuffle(cities_copy)
        routes.append(Route(cities_copy))

    genetic_algorithm(routes)
    