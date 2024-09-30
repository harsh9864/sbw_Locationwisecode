# # Copyright (c) 2024, Sanskar technolab and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class AreaZone(Document):
#     skip_unique_code_update = False
#     def before_save(self):
#         if self.is_new():
#             # Update the state count and unique code before saving
#             self.update_zone_wise_count()
#             self.update_unique_code()
            
#         # frappe.msgprint(f"State Wise Count in before_save: {self.zone_wise_count}")

#     def update_zone_wise_count(self):
#         # Fetch the single document from the 'Country Code Logic' doctype
#         location_settings = frappe.get_doc("Country Code Logic", self.country)

#         # Initialize final_code_digit_option
#         final_code_digit_option = None

#         # Check if the child table has at least one row
#         if location_settings.country_code_logic_table:
#             # Access the first row of the child table
#             first_row = location_settings.country_code_logic_table[6]
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

#         count = frappe.db.count("Area Zone", filters={"area": self.area}) + 1  # Always add 1 to the countt

#         max_single_count = 9  # For "Single(1)", max allowed count is 9
#         max_double_count = 99 

#         if self.code_digit_option == "Single(1)" and count > max_single_count:
#             frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
#         elif self.code_digit_option == "Double(01)" and count > max_double_count:
#             frappe.throw("Cannot add more records. Maximum limit of 99 reached.")



#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.zone_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.zone_wise_count = str(count).zfill(2) 

# AreaZone.py
import frappe
from frappe.model.document import Document

class AreaZone(Document):
    skip_unique_code_update = False

    def before_save(self):
        if self.is_new():
            # Update the zone count and unique code before saving
            self.update_zone_wise_count()
            self.update_unique_code()
            
    def update_zone_wise_count(self):
        # Fetch the single document from the 'Country Code Logic' doctype
        location_settings = frappe.get_doc("Country Code Logic", self.country)

        # Initialize final_code_digit_option
        final_code_digit_option = None

        # Check if the child table has at least one row
        if location_settings.country_code_logic_table:
            # Access the seventh row of the child table (for area zone logic)
            seventh_row = location_settings.country_code_logic_table[6]
            value = seventh_row.select  # Assuming 'select' is the field you need to check

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

        # Calculate the count for the Area Zone
        count = frappe.db.count("Area Zone", filters={"area": self.area}) + 1  # Always add 1 to the count

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

        # Set the zone_wise_count based on the code_digit_option
        if self.code_digit_option == "Single(1)":
            # For "Single(1)", display the count as a single digit
            self.zone_wise_count = str(count)  # No leading zero, starts from 1
        elif self.code_digit_option == "Double(01)":
            # For "Double(01)", display the count as two digits with leading zeros
            self.zone_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
        elif self.code_digit_option == "Triple(001)":
            # For "Triple(001)", display the count as three digits with leading zeros
            self.zone_wise_count = str(count).zfill(3)  # Format as three digits with leading zero
 

    def update_unique_code(self):
        if self.skip_unique_code_update:
            return
        # Fetch the custom country code from the 'Country' doctype
        country_code = frappe.db.get_value('Area', self.area, 'unique_code')
        
        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.zone_wise_count
        else:
            self.unique_code = self.zone_wise_count
    def after_insert(self):
        try:
            # Debugging before the method call
            print("Area zone doc...")
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
        area_zone = frappe.get_doc("Area", {"name": self.area})


        area_zone.flags.ignore_permissions = True  # Bypass permission checks
        area_zone.flags.ignore_validate_update_after_submit = True

       

        # Check if the state already exists in the child table
        existing_state = next((row for row in area_zone.area_zone_list if row.area_zone_id == self.name), None)
            
        if not existing_state:
            # Assign the area_wise_code for the new district
            count = frappe.db.count("Area Zone", filters={"area": self.area})
            new_code = count + 1
            
            # Append a new row in the area_zone_list child table of Districts
            new_row = area_zone.append("area_zone_list", {})
            new_row.area_zone_id = self.name
            new_row.zone_code = new_code

            # Save the Districts document
            area_zone.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.area_zone_id, row.zone_code) for row in area_zone.area_zone_list]
            # print(f"Updated Districts after update: {updated_states}")



    def entry_doc(self):
            print("Inside entry_doc function")
            # Fetch the document settings
            location_settings = frappe.get_doc("Country Code Logic", self.country)
            table = location_settings.country_code_logic_table
            doc_name = table[7]  # Assuming table[3] is correct

            print(f"Document name: {doc_name}\n")

            if doc_name.select == "Empty":
                # Prepare new document data
                new_doc_data = {
                    'doctype': 'Society',
                    "unique_code": self.unique_code,
                    "society_name": self.area_name,
                    "country": self.country,
                    # "state_code": self.unique_code,
                    "code_digit_option": "Single(1)",
                    "district_code": self.unique_code,
                    "area_zone":self.name,
                    "area_code":self.unique_code,
                    # "zone_type":"City",
                    # "district":self.name
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


# # AreaZone.py
# import frappe
# from frappe.model.document import Document

# class AreaZone(Document):
#     def before_save(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

#         if self.is_new():
#             # Update the state count and unique code before saving
#             self.update_state_count()
#             self.update_unique_code()

#     def update_state_count(self):
#         # Fetch settings to determine code formatting
#         location_settings = frappe.get_single("Location wise Code Settings")
#         code_digit_option = location_settings.states
#         self.code_digit_option = code_digit_option
#         count = frappe.db.count("Area Zone", filters={"area": self.area}) + 1

#         if self.code_digit_option == "Single(1)":
#             # Display the count as a single digit when 'Single(1)' is selected
#             self.zone_wise_count = str(count)

#         elif self.code_digit_option == "Double(01)":
#             # Display the count as two digits with leading zeros when 'Double(01)' is selected
#             self.zone_wise_count = str(count).zfill(2)

#     def update_unique_code(self):
#         # Fetch the unique code from the 'Area' doctype
#         country_code = frappe.db.get_value('Area', self.area, 'unique_code')

#         if country_code:
#             # Concatenate the area code with the formatted count
#             self.unique_code = country_code + self.zone_wise_count
#         else:
#             self.unique_code = self.zone_wise_count

#     def after_insert(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

#         self.update_district_on_states_save()

#     def update_district_on_states_save(self):
#         # Fetch the corresponding 'Area' document based on the area
#         area_zone = frappe.get_doc("Area", {"name": self.area})

#         # Check if the state already exists in the child table
#         existing_state = next((row for row in area_zone.area_zone_list if row.area_zone_id == self.name), None)

#         if not existing_state:
#             # Assign the zone code for the new area
#             count = frappe.db.count("Area Zone", filters={"area": self.area})
#             new_code = count + 1

#             # Append a new row in the area_zone_list child table of Area
#             new_row = area_zone.append("area_zone_list", {})
#             new_row.area_zone_id = self.name
#             new_row.zone_code = new_code

#             # Save the Area document
#             area_zone.save(ignore_permissions=True)

#             # Debug: Print the updated area zones and their codes (for debugging purposes)
#             updated_states = [(row.area_zone_id, row.zone_code) for row in area_zone.area_zone_list]
#             # print(f"Updated Areas after update: {updated_states}")
