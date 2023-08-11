def main():
    num_cities = int(input("Enter the number of cities: "))
    cities = []
    distances = []

    for i in range(num_cities):
        city_name = input(f"Enter city name {i+1}: ")
        cities.append(city_name)
        distance_row = []
        for j in range(num_cities):
            distance = int(input(f"Enter distance from {city_name} to {cities[j]}: "))
            distance_row.append(distance)
        distances.append(distance_row)

    best_route, min_distance = traveling_salesman_bruteforce(cities, distances)

    print("\nShortest route:", [cities[i] for i in best_route])
    print("Total distance:", min_distance)

if __name__ == "__main__":
    main()
