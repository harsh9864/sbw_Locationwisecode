import frappe

def create_document(zone_name,name, country, doctype_name="Districts", value_to_use="9125", from_rq_job=False):
    # Set the RQ job flag in context if called from an RQ job
    if from_rq_job:
        frappe.flags.in_rq_job = True
    # location_settings = frappe.get_doc("Country Code Logic", country)
    # table = location_settings.country_code_logic_table
    # table.idx=id 

    # Define mappings for each doctype
    field_mappings = {
        "States": {
            "unique_code": value_to_use,
            "state_name": name,
            "state_type": "State",
            "country_zone": name,
            "country": country,
            "code_digit_option": "Single(1)",
            "zone_name":zone_name,
        },
        "State Zone": {
            "unique_code": value_to_use,
            "state": "State",
            "country": country,
            "state_code":value_to_use,
            "code_digit_option": "Single(1)",
            "zone_name":zone_name,
            # Add more fields as required
        },
        "Districts": {
            "unique_code": value_to_use,
            "zone_type": "City",
            "country": country,
            "district_name":name,
            "state_code":value_to_use,
           
            "code_digit_option": "Single(1)",
            "zone_name":zone_name,
            "district_code":value_to_use
            # Add more fields as required
        },
        "District Zone":{
            "unique_code": value_to_use,
            "zone_type": "City",
            "country": country,
            # "state_code":value_to_use,
            "code_digit_option": "Single(1)",
            "zone_name":zone_name,
            "district_code":value_to_use
        },
        "Area": {
            "unique_code": value_to_use,
            "zone_type": "City",
            "country": country,
            "area_name":name,
            "district_code":value_to_use,
            "code_digit_option": "Single(1)",
            "district_zone":zone_name,
            "district_code":value_to_use
            # Add more fields as required
        },
         "Area Zone": {
            "unique_code": value_to_use,
            "zone_type": "City",
            "country": country,
            "area_name":name,
            "area_code":value_to_use,
            "code_digit_option": "Single(1)",
            "zone_name":zone_name,
          
            # Add more fields as required
        },
            "Society": {
            "unique_code": value_to_use,
            "zone_type": "City",
            "country": country,
            "area_zone":name,
            "society_name":name,
            "area_code":value_to_use,
            "code_digit_option": "Single(1)",
           
          
            # Add more fields as required
        },
         "Sub Society": {
            "unique_code": value_to_use,
            "zone_type": "City",
            "country": country,
            "society":name,
            "sub_society_name":name,
            "area_code":value_to_use,
            "society_name":name,
            "code_digit_option": "Single(1)",
           
          
            # Add more fields as required
        },
        "Street": {
            # "unique_code": value_to_use,
            "country": country,
            "street_name":name,
            "sub_society_code":value_to_use,
            # "society_name":name,
            "code_digit_option": "Single(1)",
           
          
            # Add more fields as required
        },

        # Add more doctypes and their respective fields here
    }

    # Prepare the data for the new document based on doctype_name
    doc_data = {"doctype": doctype_name}
    if doctype_name in field_mappings:
        doc_data.update(field_mappings[doctype_name])
    else:
        frappe.msgprint(f"No field mappings found for doctype: {doctype_name}")
        return
    
    try:
        # Create and insert the new document
        new_doc = frappe.get_doc(doc_data)
        new_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Document created in {doctype_name} with value: {value_to_use}")
    except Exception as e:
        frappe.log_error(f"Error creating document in {doctype_name}: {str(e)}")
