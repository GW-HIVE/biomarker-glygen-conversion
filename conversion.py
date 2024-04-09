""" Example conversion from GlyGen biomarker data model to Biomarker-Partnership data model.
This script is based on the A0001 entry and assumes all instances are a singular biomarker (i.e. not
a panel or multi-component biomarker).
"""

import json
import helpers


def main():

    # Holds the converted biomarker entries.
    result_data = []

    # Read in glygen biomarker record.
    with open("glygen_biomarker.json", "r") as f:

        glygen_biomarker = json.load(f)

        # Grab common fields that will be shared across the records after being split.
        biomarker_id = glygen_biomarker["biomarker_id"]
        assessed_entity_type = glygen_biomarker["assessed_entity_type"]
        # The A0001 record only has one value for the components[protein] array. Not
        # sure how/what it means when there are multiple values here. For this example,
        # just hardcoding for the assumption of one value.
        assessed_biomarker_entity = glygen_biomarker["components"]["protein"][0]["name"]
        # In our data model, the ID value is formatted as "{resource acronym}:{accession}", so
        # this value should be "UPKB:P05231-1". For different assessed entity type biomarkers
        # we have to support multiple databases so the resource acronym/namespace is required.
        # Not sure if you will have to support this.
        assessed_biomarker_entity_id = glygen_biomarker["components"]["protein"][0][
            "accession"
        ]

        # Loop through instances.
        for instance in glygen_biomarker["instances"]:

            # Build biomarker component.
            biomarker_component = helpers.build_biomarker_component(
                assessed_biomarker_entity,
                assessed_biomarker_entity_id,
                assessed_entity_type,
                instance
            )

            # Build best biomarker role object.
            # TODO

            # Build condition object.
            condition_object = helpers.build_condition_object(instance["disease"])

            # Build the full biomarker record.
            result_data.append(helpers.build_record(biomarker_id, biomarker_component, condition_object))

    with open('converted_data.json', 'w') as f:
        json.dump(result_data, f)

if __name__ == "__main__":
    main()
