# Copyright (c) 2024, Sanskar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


# class CountryZone(Document):
#     skip_unique_code_update = False
#     def before_save(self):
#         if self.is_new():
#             self.update_country_wise_count()
#             self.update_unique_code()
            

#     def update_country_wise_count(self):
#         # Fetch the single document from the 'Country Code Logic' doctype
#         location_settings = frappe.get_doc("Country Code Logic", self.country)

#         # Initialize final_code_digit_option
#         final_code_digit_option = None

#         # Check if the child table has at least one row
#         if location_settings.country_code_logic_table:
#             # Access the first row of the child table
#             first_row = location_settings.country_code_logic_table[0]
#             value = first_row.select  # Assuming 'select' is the field you need to check

#             # Set final_code_digit_option based on the value of 'select'
#             if value == "Single":
#                 final_code_digit_option = "1"
#             elif value == "Double":
#                 final_code_digit_option = "01"
            
        
#         if final_code_digit_option =="1":
#             self.code_digit_option = "Single(1)"
#         elif final_code_digit_option == "01":
#             self.code_digit_option = "Double(01)"

    
#         count = (
#             frappe.db.count("Country Zone", filters={"country": self.country}) + 1
#         )  # Always add 1 to the count

#         max_single_count = 9  # For "Single(1)", max allowed count is 9
#         max_double_count = 99 

#         if self.code_digit_option == "Single(1)" and count > max_single_count:
#             frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
#         elif self.code_digit_option == "Double(01)" and count > max_double_count:
#             frappe.throw("Cannot add more records. Maximum limit of 99 reached.")


#         if  self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.country_wise_count = str(count)  # No leading zero, starts from 1

#         elif  self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.country_wise_count = str(count).zfill(
#                 2
#             )  # Format as two digits with leading zero

    
class CountryZone(Document):
    skip_unique_code_update = False

    def before_save(self):
        if self.is_new():
            self.update_country_wise_count()
            self.update_unique_code()

    def update_country_wise_count(self):
        # Fetch the single document from the 'Country Code Logic' doctype
        location_settings = frappe.get_doc("Country Code Logic", self.country)

        # Initialize final_code_digit_option
        final_code_digit_option = None

        # Check if the child table has at least one row
        if location_settings.country_code_logic_table:
            # Access the first row of the child table
            first_row = location_settings.country_code_logic_table[0]
            value = first_row.select  # Assuming 'select' is the field you need to check

            # Set final_code_digit_option based on the value of 'select'
            if value == "Single":
                final_code_digit_option = "1"
            elif value == "Double":
                final_code_digit_option = "01"
            elif value == "Triple":
                final_code_digit_option = "001"

        # Set code_digit_option based on the final_code_digit_option
        if final_code_digit_option == "1":
            self.code_digit_option = "Single(1)"
        elif final_code_digit_option == "01":
            self.code_digit_option = "Double(01)"
        elif final_code_digit_option == "001":
            self.code_digit_option = "Triple(001)"

        # Calculate the count for the country
        count = frappe.db.count("Country Zone", filters={"country": self.country}) + 1  # Always add 1 to the count

        # Define max counts based on the code_digit_option
        max_single_count = 9  # For "Single(1)", max allowed count is 9
        max_double_count = 99  # For "Double(01)", max allowed count is 99
        max_triple_count = 999  # For "Triple(001)", max allowed count is 999

        # Validate count based on code_digit_option
        if self.code_digit_option == "Single(1)" and count > max_single_count:
            frappe.throw("Cannot add more records. Maximum limit of 9 reached.")
        elif self.code_digit_option == "Double(01)" and count > max_double_count:
            frappe.throw("Cannot add more records. Maximum limit of 99 reached.")
        elif self.code_digit_option == "Triple(001)" and count > max_triple_count:
            frappe.throw("Cannot add more records. Maximum limit of 999 reached.")

        # Set the country_wise_count based on the code_digit_option
        if self.code_digit_option == "Single(1)":
            # For "Single(1)", display count as a single digit
            self.country_wise_count = str(count)  # No leading zeros, starts from 1
        elif self.code_digit_option == "Double(01)":
            # For "Double(01)", display count as two digits with leading zeros
            self.country_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
        elif self.code_digit_option == "Triple(001)":
            # For "Triple(001)", display count as three digits with leading zeros
            self.country_wise_count = str(count).zfill(3)  # Format as three digits with leading zero


    def update_unique_code(self):
        if self.skip_unique_code_update:
            return
        # Fetch the custom country code from the 'Country' doctype
        country_code = frappe.db.get_value(
            "Country", self.country, "custom_country_code"
        )

        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.country_wise_count
        else:
            self.unique_code = self.country_wise_count


    def after_insert(self):
        self.update_district_on_states_save()
        self.entry_doc()

    def update_district_on_states_save(self):
        # Fetch the country document using its name
        country = frappe.get_doc("Country", {"name": self.country})
        # frappe.msgprint(f"Processing country: {country.name}")

        country.flags.ignore_permissions = True  # Bypass permission checks
        country.flags.ignore_validate_update_after_submit = True


        # Check if the state already exists in the child table
        existing_state = next((row for row in country.custom_country_zone_list if row.country_zone == self.name), None)

        if not existing_state:
            # Assign a new area_wise_code for the new district
            count = frappe.db.count("Country Zone", filters={"country": self.country})
            new_code = count + 1

            # Append a new row in the custom_country_zone_list child table of Districts
            new_row = country.append("custom_country_zone_list", {})
            new_row.country_zone = self.name
            new_row.zone_code = new_code

            # Save the updated Country document
            country.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.country_zone, row.zone_code) for row in country.custom_country_zone_list]
            # frappe.msgprint(f"Updated Districts after update: {updated_states}")




    def entry_doc(self):
        location_settings = frappe.get_doc("Country Code Logic", self.country)
        table = location_settings.country_code_logic_table
        doc_name = table[1]
        if doc_name.select == "Empty":
            # Create the States document
            new_doc_data = {
                'doctype': 'States',
                "unique_code": self.unique_code,
                "state_name": self.name,
                "state_type": "State",
                "country_zone": self.name,
                "country": self.country,
                "code_digit_option": "Single(1)",
                # Ensure zone_name is correctly assigned
                "zone_name": getattr(self, 'zone_name', ''),  # Fallback to empty string if zone_name is missing
                # Add other fields as needed
            }
            
            # Create the document
            new_doc = frappe.get_doc(new_doc_data)
            new_doc.skip_unique_code_update = True

            try:
                new_doc.insert()
                new_doc.save()
                new_doc.submit()
            except Exception as e:
                frappe.log_error(message=str(e), title="Error Creating States Document")
                frappe.msgprint(f"Error: {str(e)}")

            


    # def entry_doc(self):
    #     # Fetch the single document from the 'Country Code Logic' doctype
    #     try:
    #         location_settings = frappe.get_doc("Country Code Logic", self.country)
    #     except Exception as e:
    #         frappe.log_error(f"Error fetching Country Code Logic document: {str(e)}")
    #         frappe.msgprint(f"Error fetching Country Code Logic document: {str(e)}")
    #         return

    #     # Iterate through each row in the child table 'country_code_logic_table'
    #     for row in location_settings.country_code_logic_table:
    #         doctype_name = row.doctype_list

    #         # Check if doctype_name exists and proceed only if it's not empty
    #         if doctype_name:
    #             # Determine if 'select' field value is "Empty"
    #             if row.select == "Empty":
    #                 # Enqueue document creation to run in the background
    #                 frappe.enqueue(
    #                     'location_wise_code.api.create_document',
    #                     doctype_name=doctype_name,
    #                     value_to_use=self.unique_code,
    #                     country=location_settings.country,
    #                     name=self.name,
    #                     zone_name=self.zone_name,
    #                     from_rq_job=True  # Pass the flag indicating it's from an RQ job
    #                 )
   

  
    # def entry_doc(self):
    #     doc_name = "Country Zone"

    #     # Fetch the parent document and the child table
    #     location_settings = frappe.get_doc("Country Code Logic", self.country)
    #     table = location_settings.country_code_logic_table

    #     # Iterate through the rows of the child table
    #     for idx, row in enumerate(table):
    #         # Check if the current row's doctype_list contains the doc_name
    #         if doc_name in row.doctype_list:
    #             # Check if the select field of the current row is "Empty" or "Not Required"
    #             if row.select  in ["Empty", "Not Required"]:
    #                 # Show the message and skip to the next iteration if conditions are met
    #                 frappe.msgprint("next_row")
    #                 continue

    #         # Check the select field value in the next row, if it exists
    #         if idx + 1 < len(table):
                
    #             next_row = table[1]
    #             #  Print the index of the next row
    #             print("idx: " + str(next_row.idx) + "\n\n\n\n\n\n\n\n\n\n\n")
            
    #             # Check if the next row's select field is "Empty" or "Not Required"
    #             if next_row.select in ["Empty", "Not Required"]:
    #                 frappe.enqueue('location_wise_code.api.create_document', doc="Country Zone",id=next_row.idx,country=self.country)

    #                 continue

          