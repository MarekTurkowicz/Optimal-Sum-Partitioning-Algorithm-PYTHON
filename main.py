class Crystal:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


class CrystalCombination:
    def __init__(self, fuel_amount, crystal_count):
        self.fuel_amount = fuel_amount
        self.crystal_count = crystal_count


class StarFleetFuelProblem:
    def __init__(self):
        self.max_fuel = 100
        self.seen_crystals = [[[None for _ in range(self.max_fuel + 1)]
                               for _ in range(self.max_fuel + 1)]
                              for _ in range(self.max_fuel + 1)]

    def find_optimal_fuel_amount(self, crystals):
        return self._find_optimal(crystals, 0, 0, 0, 0, len(crystals))

    def _find_optimal(self, crystals, index, sum_x, sum_y, sum_z, n):
        if sum_x > self.max_fuel or sum_y > self.max_fuel or sum_z > self.max_fuel:
            return CrystalCombination(0, float('inf'))

        if index == n:
            if sum_x == sum_y == sum_z and sum_x != 0:
                return CrystalCombination(sum_x * 3, 0)
            return CrystalCombination(0, float('inf'))

        if self.seen_crystals[sum_x][sum_y][sum_z] is not None:
            return self.seen_crystals[sum_x][sum_y][sum_z]

        current_crystal = crystals[index]
        include_current = self._find_optimal(
            crystals, index + 1, sum_x + current_crystal.x,
            sum_y + current_crystal.y, sum_z + current_crystal.z, n)
        exclude_current = self._find_optimal(crystals, index + 1, sum_x, sum_y, sum_z, n)

        if (include_current.fuel_amount > exclude_current.fuel_amount or
                (include_current.fuel_amount == exclude_current.fuel_amount and
                 include_current.crystal_count < exclude_current.crystal_count)):
            best_combination = CrystalCombination(include_current.fuel_amount, include_current.crystal_count + 1)
        else:
            best_combination = exclude_current

        self.seen_crystals[sum_x][sum_y][sum_z] = best_combination
        return best_combination

import os

def read_crystals_from_file(file_path):
    crystals = []
    with open(file_path, 'r') as file:
        num_crystals = int(file.readline().strip())
        for _ in range(num_crystals):
            x, y, z = map(int, file.readline().split())
            crystals.append(Crystal(x, y, z))
    return crystals
import time
def main():
    file_path = "duzytestCEZ2"
    # Sprawdzenie, czy plik istnieje
    if not os.path.exists(file_path):
        print(f"Nie znaleziono pliku: {file_path}")
        return
    x=time.time()
    crystals = read_crystals_from_file(file_path)
    problem_solver = StarFleetFuelProblem()
    result = problem_solver.find_optimal_fuel_amount(crystals)
    y=time.time()
    resultt = y-x
    print(f'{resultt} sec')
    if result.fuel_amount == 0:
        print("NIE")
    else:
        print(f"Maksymalna ilość paliwa: {result.fuel_amount}")
        print(f"Minimalna liczba kryształów: {result.crystal_count}")

if __name__ == "__main__":
    main()

