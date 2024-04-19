""" Splits the IDs in the GlyGen allbiomarkers-all.csv file. 
"""

import csv
import json

file_path = "./allbiomarkers-all.csv"


def main():

    # Holds the dictionary that maps the assessed biomarker
    # IDs to the disease instance second level IDs.
    id_map = {}
    # Holds the new dictionary rows that will be dumped to
    # the updated CSV file.
    new_rows = []

    # Loop through the existing CSV and map the second level IDs.
    biomarker_file = csv.DictReader(open(file_path, "r"))
    for idx, row in enumerate(biomarker_file):
        # Grab the row ID and disease.
        row_id = row["Assessed biomarker entity ID"]
        row_disease = row["Disease name"]
        # If the ID is not in the map, create a new entry for it.
        if row_id not in id_map:
            curr_id = 1
            new_id = f"{row_id}-{curr_id}"
            id_map[row_id] = {"curr_id": curr_id, row_disease: new_id}
        # If the ID is already in the map, check if the disease has
        # already been captured and handle accordingly.
        else:
            # If the disease is already captured, assign the record
            # the existing second level ID.
            if row_disease in id_map[row_id]:
                new_id = id_map[row_id][row_disease]
            # If the disease has not been captured, increment the
            # second level ID and add to the map.
            else:
                id_map[row_id]["curr_id"] += 1
                new_id = f"{row_id}-{id_map[row_id]['curr_id']}"
                id_map[row_id][row_disease] = new_id

        row["biomarker_id"] = new_id
        new_rows.append(row)

    with open("allbiomarkers-updated.csv", "w", newline="") as out:
        dict_writer = csv.DictWriter(out, new_rows[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(new_rows)

    with open("id_map.json", "w") as out:
        json.dump(id_map, out, indent=4)

if __name__ == "__main__":
    main()
