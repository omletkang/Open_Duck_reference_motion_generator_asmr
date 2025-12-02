import json
import glob
import os

def find_min_max(folder_path):
    # 1. Setup the path to search for *.json files
    search_path = os.path.join(folder_path, "*.json")
    files = glob.glob(search_path)
    
    print(f"Found {len(files)} JSON files in {folder_path}. Processing...")

    # 2. Initialize variables with Infinity for comparison
    # This ensures the first valid number found will become the new min/max
    stats = {
        "Vel_x": {"min": float('inf'), "max": float('-inf'), "count": 0},
        "Vel_y": {"min": float('inf'), "max": float('-inf'), "count": 0},
        "Yaw": {"min": float('inf'), "max": float('-inf'), "count": 0},
    }

    # 3. Loop through every file
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Helper function to update stats for a single dictionary
                def update_stats(record):
                    for key in ["Vel_x", "Vel_y", "Yaw"]:
                        if key in record and isinstance(record[key], (int, float)):
                            val = record[key]
                            if val < stats[key]["min"]: stats[key]["min"] = val
                            if val > stats[key]["max"]: stats[key]["max"] = val
                            stats[key]["count"] += 1

                # Handle case where JSON is a list of records
                if isinstance(data, list):
                    for item in data:
                        update_stats(item)
                # Handle case where JSON is a single object
                elif isinstance(data, dict):
                    update_stats(data)

        except json.JSONDecodeError:
            print(f"Warning: Could not parse {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {e}")

    # 4. Print Results
    print("-" * 40)
    for key in ["Vel_x", "Vel_y", "Yaw"]:
        if stats[key]["count"] > 0:
            print(f"Key: {key}")
            print(f"  Min: {stats[key]['min']}")
            print(f"  Max: {stats[key]['max']}")
            print(f"  Data points processed: {stats[key]['count']}")
        else:
            print(f"Key: {key} - No valid numeric data found.")
    print("-" * 40)

# Run the function
# Ensure this matches your folder name exactly
target_folder = "./recordings_our_robot_251119" # ASMR
find_min_max(target_folder)