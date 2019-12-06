def calculate_fuel(mass, *, recursive=False):
    fuel = mass // 3 - 2

    if fuel <= 0:
        return 0

    if not recursive:
        return fuel

    return fuel + calculate_fuel(fuel, recursive=True)


def solve(file, verbose):
    modules = [int(module) for module in file]
    print('Part 1:', sum(calculate_fuel(m) for m in modules))
    print('Part 2:', sum(calculate_fuel(m, recursive=True) for m in modules))
