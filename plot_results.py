import csv

def parse_results_file(filepath):
    frames = []
    fault_rates = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("total memory frames:"):
                frames.append(int(line.split(":")[1].strip()))
            elif line.startswith("page fault rate:"):
                fault_rates.append(float(line.split(":")[1].strip()))
    hit_rates = [(1 - fr) * 100 for fr in fault_rates]
    return dict(zip(frames, hit_rates))

# Map your result files for sixpack
algo_files = {
    "Rand": ["sixpack_rand_shortage.txt", "sixpack_rand_workingset.txt", "sixpack_rand_excess.txt"],
    "LRU": ["sixpack_lru_shortage.txt", "sixpack_lru_workingset.txt", "sixpack_lru_excess.txt"],
    "Clock": ["sixpack_clock_shortage.txt", "sixpack_clock_workingset.txt", "sixpack_clock_excess.txt"],
}

# Collect all data
combined_data = {}
for algo, files in algo_files.items():
    for file in files:
        results = parse_results_file(file)
        for frame, hit_rate in results.items():
            if frame not in combined_data:
                combined_data[frame] = {}
            combined_data[frame][algo] = hit_rate

# Write to CSV
with open("sixpack_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Frames", "Rand", "LRU", "Clock"])
    for frame in sorted(combined_data.keys()):
        row = [frame,
               combined_data[frame].get("Rand", ""),
               combined_data[frame].get("LRU", ""),
               combined_data[frame].get("Clock", "")]
        writer.writerow(row)

print("✅ CSV file created: sixpack_results.csv")
