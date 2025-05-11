from preprocessing import parse_data, check_compatibility, calculate_dissimilarities
from part1_max_priority import solve_part1
from part2_min_dissimilarity import solve_part2
from utils import save_assignments, plot_tradeoff

def main():
    seekers, jobs, location_distances = parse_data(
        '../data/seekers.csv', '../data/jobs.csv', '../data/location_distances.csv'
    )

    location_distances.to_csv('../results/location_distance_matrix.csv')


    compatiblity_values = check_compatibility(seekers, jobs, location_distances)
    pairs = [
        (i, j) for i in seekers.index 
        for j in jobs.index 
    ]
    dissimilarities = calculate_dissimilarities(seekers, jobs, pairs)

    M_w, assignments_p1 = solve_part1(seekers, jobs, compatiblity_values, pairs)
    save_assignments(assignments_p1, '../results/assignments/part1_assignments.csv')

    omega_values = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    results = []

    for omega in omega_values:
        max_d, assignments = solve_part2(omega, M_w, seekers, jobs, compatiblity_values, pairs, dissimilarities)
        save_assignments(assignments, f'../results/assignments/part2_omega_{omega}.csv')
        results.append((omega, max_d))

    plot_tradeoff(*zip(*results), save_path='../results/plots/tradeoff_curve.png')

    print(f"Part 1 completed. Max priority weight: {M_w}")
    print("Part 2 completed. Results saved.")

if __name__ == "__main__":
    main()
