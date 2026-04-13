import os
import json

def count_json_objects(directory_path="Generated_Documentation"):
    total_objects = 0
    
    # Check if the directory exists to avoid errors
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' not found.")
        return 0

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        # Process only .json files
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    file_object_count = 0
                    
                    # If the JSON contains a list of objects
                    if isinstance(data, list):
                        file_object_count = len(data)
                    # If the JSON contains a single object (dictionary)
                    elif isinstance(data, dict):
                        file_object_count = 1
                    
                    # Print the count for the current file
                    print(f"Found {file_object_count} object(s) in '{filename}'")
                    
                    # Add to the running total
                    total_objects += file_object_count
                        
            except json.JSONDecodeError:
                print(f"Skipping '{filename}': Not a valid JSON or file is empty.")
            except Exception as e:
                print(f"Could not read '{filename}' due to an error: {e}")

    return total_objects

if __name__ == "__main__":
    print("Scanning directory...\n" + "-"*30)
    total_count = count_json_objects()
    print("-"*30)
    print(f"Total number of JSON objects found across all files: {total_count}")
