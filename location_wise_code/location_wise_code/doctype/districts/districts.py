# # Copyright (c) 2024, Sanskar technolab and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class Districts(Document):
#     skip_unique_code_update = False
#     def before_save(self):
#         if self.is_new():                                                                                                                      
#             self.update_zone_wise_count()
#             self.update_unique_code()

#     def update_zone_wise_count(self):
#         # Fetch the single document from the 'Country Code Logic' doctype
#         location_settings = frappe.get_doc("Country Code Logic", self.country)

#         # Initialize final_code_digit_option
#         final_code_digit_option = None

#         # Check if the child table has at least one row
#         if location_settings.country_code_logic_table:
#             # Access the first row of the child table
#             first_row = location_settings.country_code_logic_table[3]
#             value = first_row.select  # Assuming 'select' is the field you need to check

#             # Set final_code_digit_option based on the value of 'select'
#             if value == "Single":
#                 final_code_digit_option = "1"
#             elif value == "Double":
#                 final_code_digit_option = "01"
               
        
#         if final_code_digit_option =="1" :
#             self.code_digit_option = "Single(1)"
#         elif final_code_digit_option == "01":
#             self.code_digit_option = "Double(01)"

#         count = frappe.db.count("Districts", filters={"state_zone": self.state_zone}) + 1  # Always add 1 to the count

#         max_single_count = 9  # For "Single(1)", max allowed count is 9
#         max_double_count = 99 

#         if self.code_digit_option == "Single(1)" and count > max_single_count:
#             frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
#         elif self.code_digit_option == "Double(01)" and count > max_double_count:
#             frappe.throw("Cannot add more records. Maximum limit of 99 reached.")


#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.district_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.district_wise_count = str(count).zfill(2) 

# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Districts(Document):
    skip_unique_code_update = False

    def before_save(self):
        if self.is_new():
            self.update_zone_wise_count()
            self.update_unique_code()

    def update_zone_wise_count(self):
        # Fetch the single document from the 'Country Code Logic' doctype
        location_settings = frappe.get_doc("Country Code Logic", self.country)

        # Initialize final_code_digit_option
        final_code_digit_option = None

        # Check if the child table has at least one row
        if location_settings.country_code_logic_table:
            # Access the fourth row of the child table (for the district logic)
            fourth_row = location_settings.country_code_logic_table[3]
            value = fourth_row.select  # Assuming 'select' is the field you need to check

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

        # Calculate the count for the district in the given state zone
        count = frappe.db.count("Districts", filters={"state_zone": self.state_zone}) + 1  # Always add 1 to the count

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

        # Set the district_wise_count based on the code_digit_option
        if self.code_digit_option == "Single(1)":
            # For "Single(1)", display count as a single digit
            self.district_wise_count = str(count)  # No leading zeros, starts from 1
        elif self.code_digit_option == "Double(01)":
            # For "Double(01)", display count as two digits with leading zeros
            self.district_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
        elif self.code_digit_option == "Triple(001)":
            # For "Triple(001)", display count as three digits with leading zeros
            self.district_wise_count = str(count).zfill(3)  # Format as three digits with leading zero

    def update_unique_code(self):
        if self.skip_unique_code_update:
            return
        # Fetch the unique code from the 'State Zone' doctype
        country_code = frappe.db.get_value('State Zone', self.state_zone, 'unique_code')
        
        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.district_wise_count
        else:
            self.unique_code = self.district_wise_count

    def after_insert(self):
        # print("\n\n\n\n\n\n\n\n\n\n\n\n", "after insert")
        # self.entry_doc() 
        # self.update_district_on_states_save()

        try:
            # Debugging before the method call
            print("Before calling update_state_zone_on_states_save...")
            self.entry_doc() 
            self.update_district_on_states_save()
            print("After calling update_state_zone_on_states_save...")

            # Debugging before entry_doc method
            print("Attempting to call entry_doc...")
             # Attempt to call the function
            print("entry_doc() called successfully.")
        except Exception as e:
            print(f"Error while calling entry_doc(): {e}")
        
    def update_district_on_states_save(self):
        district = frappe.get_doc("State Zone", {"name": self.state_zone})
        district.flags.ignore_permissions = True  # Bypass permission checks
        district.flags.ignore_validate_update_after_submit = True
        

        
        

        # Check if the state already exists in the child table
        existing_state = next((row for row in district.district_list if row.district_id == self.district_name), None)
            
        if not existing_state:
            # Assign the district_code for the new district
            count = frappe.db.count("Districts", filters={"state_zone": self.state_zone})
            new_code = count + 1
            
            # Append a new row in the district_list child table of State Zone
            new_row = district.append("district_list", {})
            new_row.district_id = self.name
            new_row.district_code = new_code

            # Save the State Zone document
            district.save(ignore_permissions=True)
           

            

            # Debug: Print the updated districts and their codes
            updated_states = [(row.district_id, row.district_code) for row in district.district_list]
            # print(f"Updated Districts after update: {updated_states}")

    def entry_doc(self):
            print("Inside entry_doc function")
            # Fetch the document settings
            location_settings = frappe.get_doc("Country Code Logic", self.country)
            table = location_settings.country_code_logic_table
            doc_name = table[4]  # Assuming table[3] is correct

            print(f"Document name: {doc_name}\n")

            if doc_name.select == "Empty":
                # Prepare new document data
                new_doc_data = {
                    'doctype': 'District Zone',
                    "unique_code": self.unique_code,
                    "district": self.name,
                    "country": self.country,
                    "code_digit_option": "Single(1)",
                    "district_code": self.unique_code,
                    "zone_name":self.district_name,
                    "zone_type":"City"
                }
                
                # Create the new document
                new_doc = frappe.get_doc(new_doc_data)
                new_doc.skip_unique_code_update = True
                try:
                    new_doc.insert()
                    new_doc.save()
                    new_doc.submit()
                    frappe.db.commit()
                    print("New document created and committed successfully.")
                except Exception as e:
                    frappe.log_error(message=str(e), title="Error Creating States Document")
                    frappe.msgprint(f"Error: {str(e)}")
                    print(f"Error creating document: {e}")


# # Districts.py
# import frappe
# from frappe.model.document import Document

# class Districts(Document):
#     def before_save(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

#         if self.is_new():
#             self.update_district_wise_count()
#             self.update_unique_code()

#     def update_district_wise_count(self):
#         # Count the number of 'Districts' records for the specified state zone
#         location_settings = frappe.get_single("Location wise Code Settings")
        
#         # Retrieve the code_digit_option from the settings document
#         code_digit_option = location_settings.states
        
#         # Set the `code_digit_option` field in the CountryZone doctype
#         self.code_digit_option = code_digit_option
#         count = frappe.db.count("Districts", filters={"state_zone": self.state_zone}) + 1  # Always add 1 to the count

#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.district_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.district_wise_count = str(count).zfill(2)  # Format as two digits with leading zero

#     def update_unique_code(self):
#         # Fetch the unique code from the 'State Zone' doctype
#         country_code = frappe.db.get_value('State Zone', self.state_zone, 'unique_code')
        
#         if country_code:
#             # Concatenate the country code with the formatted count
#             self.unique_code = country_code + self.district_wise_count
#         else:
#             self.unique_code = self.district_wise_count

#     def after_insert(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

#         self.update_district_on_states_save()

#     def update_district_on_states_save(self):
#         # Fetch the corresponding 'State Zone' document based on the state zone
#         district = frappe.get_doc("State Zone", {"name": self.state_zone})

#         # Check if the district already exists in the child table
#         existing_state = next((row for row in district.district_list if row.district_id == self.district_name), None)
            
#         if not existing_state:
#             # Assign the district_code for the new district
#             count = frappe.db.count("Districts", filters={"state_zone": self.state_zone})
#             new_code = count + 1
            
#             # Append a new row in the district_list child table of State Zone
#             new_row = district.append("district_list", {})
#             new_row.district_id = self.name
#             new_row.district_code = new_code

#             # Save the State Zone document
#             district.save(ignore_permissions=True)

#             # Debug: Print the updated districts and their codes (for debugging purposes)
#             updated_states = [(row.district_id, row.district_code) for row in district.district_list]
#             # print(f"Updated Districts after update: {updated_states}")
