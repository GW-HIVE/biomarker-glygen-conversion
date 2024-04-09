def build_biomarker_component(
    assessed_biomarker_entity: str,
    assessed_biomarker_entity_id: str,
    assessed_entity_type: str,
    instance: dict,
) -> list:
    """Takes in the GlyGen biomarker instance and builds the biomarker component in accordance
    with the Biomarker-Partnership data model. This assumes a non-panel/multi-component biomarker
    meaning that it returns just one biomarker component entry.

    Parameters
    ----------
    assessed_biomarker_entity : str
        The assessed biomarker entity.
    assessed_biomarker_entity_id : str
        The assessed biomarker entity id.
    assessed_entity_type : str
        The assessed entity type.
    instance : dict
        The GlyGen biomarker instance.

    Returns
    -------
    list
        The biomarker component according to the Biomarker-Partnership data model.
    """

    biomarker_component = {
        "biomarker": instance["status"],
        "assessed_biomarker_entity": {
            "recommended_name": assessed_biomarker_entity,
            # Not sure if the GlyGen data model supports synonyms,
            # if not then this can be left empty. When the Biomarker-Partnership
            # data is converted it hits the corresponding data resource API to
            # automatically pull in synonyms. Don't have to populate this if
            # this won't be used for searching.
            "synonyms": [],
        },
        "assessed_biomarker_entity_id": assessed_biomarker_entity_id,
        "assessed_entity_type": assessed_entity_type,
        "specimen": [
            {
                "name": instance["tissue"]["name"],
                # Similar to the note about the assessed_biomarker_entity_id in the
                # conversion.py script, our ID field includes the namespace. So in
                # our data model this would be "UBERON:0000178".
                "id": instance["tissue"]["id"],
                "name_space": instance["tissue"]["namespace"],
                "url": instance["tissue"]["url"],
                "loinc_code": instance["loinc_code"],
            }
        ],
        "evidence_source": build_evidence_sources(instance["evidence"]),
    }

    return [biomarker_component]


def build_evidence_sources(evidences: list) -> list:
    """Builds the evidence source list in accordance to the Biomarker-Partnership data model.
    We talked about the difference in philosophy with how the evidence source object is
    structured. The frontend will likely have to be slightly different based on the difference
    in structure. Make edits to this as you see fit.

    Parameters
    ----------
    evidence : list
        The evidence list from the GlyGen data model.

    Returns
    -------
    list
        The Biomarker-Partnership formatted evidence list.
    """
    evidence_sources: list = []

    for evidence in evidences:
        evidence_source = {
            "id": evidence["id"],
            "database": evidence["database"],
            "url": evidence["url"],
            # Not sure what to map here. GlyGen has the literature evidence field
            # but it is unclear to me if all evidence values have that direct
            # quote in the literature evidence field. Leaving this blank.
            "evidence_list": [],
            # Not sure if you will be able to retroactively add evidence tags.
            "tags": [],
        }
        evidence_sources.append(evidence_source)

    return evidence_sources

def build_condition_object(disease_instance: dict) -> dict:
    """Builds the condition object in accordance to the Biomarker-Partnership
    data model.

    Parameters
    ----------
    disease_instance : dict
        The instance disease object from the GLyGen data model.

    Returns
    -------
    dict
        The condition object formatted according to the Biomarker-Partnership
        data model.
    """

    # Build top level condition object.
    condition_object = {
        "id": disease_instance["disease_id"],
        "recommended_name": {
            "id": disease_instance["recommended_name"]["id"],
            "name": disease_instance["recommended_name"]["name"],
            "description": disease_instance["recommended_name"]["description"],
            "resource": disease_instance["recommended_name"]["resource"],
            "url": disease_instance["recommended_name"]["url"],
        },
        "synonyms": [],
    }

    # Loop through condition synonyms and add to synonym array.
    for synonym_entry in disease_instance["synonyms"]:
        condition_object["synonyms"].append(
            {
                "id": synonym_entry["id"],
                "name": synonym_entry["name"],
                "resource": synonym_entry["resource"],
                "url": synonym_entry["url"],
            }
        )

    return condition_object

def build_record(
    biomarker_id: str, biomarker_component: list, condition_object: dict
) -> dict:
    """Takes in the individual formatted components and builds the full
    biomarker record in accordance to the Biomarker-Partnership data model.

    Parameters
    ----------
    biomarker_id : str
        The biomarker ID.
    biomarker_component : list
        The biomarker component array.
    condition_object : dict
        The condition object.

    Returns
    -------
    dict
        The formatted biomarker record.
    """
    return {
        "biomarker_id": biomarker_id,
        "biomarker_component": biomarker_component,
        "condition": condition_object,
    }
