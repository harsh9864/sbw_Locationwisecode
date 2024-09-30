# # Copyright (c) 2024, Sanskar technolab and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class StateZone(Document):
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
#             first_row = location_settings.country_code_logic_table[2]
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

#         count = frappe.db.count("State Zone", filters={"state": self.state}) + 1  # Always add 1 to the count
        
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
#             self.zone_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StateZone(Document):
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
            # Access the third row of the child table (for the zone logic)
            third_row = location_settings.country_code_logic_table[2]
            value = third_row.select  # Assuming 'select' is the field you need to check

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

        # Calculate the count for the zone in the given state
        count = frappe.db.count("State Zone", filters={"state": self.state}) + 1  # Always add 1 to the count

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
            # For "Single(1)", display count as a single digit
            self.zone_wise_count = str(count)  # No leading zeros, starts from 1
        elif self.code_digit_option == "Double(01)":
            # For "Double(01)", display count as two digits with leading zeros
            self.zone_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
        elif self.code_digit_option == "Triple(001)":
            # For "Triple(001)", display count as three digits with leading zeros
            self.zone_wise_count = str(count).zfill(3)  # Format as three digits with leading zero

    def update_unique_code(self):
        if self.skip_unique_code_update:
            return
        country_code = frappe.db.get_value("States", self.state, "unique_code")

        if country_code:
            self.unique_code = country_code + str(self.zone_wise_count)
        else:
            self.unique_code = str(self.zone_wise_count)
# class YourClassName:  # Replace with the actual class name
    def after_insert(self):
        print("\n\n\n\n\n\n\n\n\n\n\n\n", "after insert")
        
       
        try:
            # Debugging before the method call
            print("Before calling update_state_zone_on_states_save...")
            self.entry_doc()  
            print("After calling update_state_zone_on_states_save...")
            self.update_state_zone_on_states_save()
            # Debugging before entry_doc method
            print("Attempting to call entry_doc...")
            # Attempt to call the function
            print("entry_doc() called successfully.")
        except Exception as e:
            print(f"Error while calling entry_doc(): {e}")

    def entry_doc(self):
        print("Inside entry_doc function")
        try:
            # Fetch the document settings
            location_settings = frappe.get_doc("Country Code Logic", self.country)
            print(f"Fetched location settings: {location_settings}")
            table = location_settings.country_code_logic_table
            doc_name = table[3]  # Assuming table[3] is correct
            print(f"Document name: {doc_name}\n")

            if doc_name.select == "Empty":
                # Prepare new document data
                new_doc_data = {
                    'doctype': 'Districts',
                    "unique_code": self.unique_code,
                    "district_name": self.zone_name,
                    "country": self.country,
                    "state_code": self.unique_code,
                    "code_digit_option": "Single(1)",
                    "district_code": self.unique_code,
                    "state_zone":self.name
                }
                print(f"New document data prepared: {new_doc_data}")

                # Create the new document
                new_doc = frappe.get_doc(new_doc_data)
                new_doc.skip_unique_code_update = True

                print("New document instance created.")

                try:
                    new_doc.insert()
                    print("Document inserted.")
                    new_doc.save()
                    print("Document saved.")
                    new_doc.submit()
                    print("Document submitted.")
                    frappe.db.commit()
                    print("Database committed successfully.")
                except Exception as e:
                    frappe.log_error(message=str(e), title="Error Creating States Document")
                    frappe.msgprint(f"Error: {str(e)}")
                    print(f"Error creating document: {e}")
        except Exception as e:
            print(f"Error inside entry_doc: {e}")


    def update_state_zone_on_states_save(self):
        state_zone = frappe.get_doc("States", {"name": self.state})

        state_zone.flags.ignore_permissions = True  # Bypass permission checks
        state_zone.flags.ignore_validate_update_after_submit = True

        if not state_zone:
            
            return
        existing_state = next((row for row in state_zone.state_zone_list if row.state_zone_id == self.name), None)
            
        if not existing_state:
                # Assign the state_code for new state
                count = frappe.db.count("State Zone", filters={"state": self.state})
                new_code = count + 1
                
                # Append a new row in the state_zone_code child table of Country Zone
                new_row = state_zone.append("state_zone_list", {})
                new_row.state_zone_id = self.name
                new_row.state_zone_code = new_code

                # Save the Country Zone document
                state_zone.save(ignore_permissions=True)    
                

                # Debug: Print the updated states and their codes
                updated_states = [(row.state_zone_id, row.state_zone_code) for row in state_zone.state_zone_list]
                # print(f"Updated States after update: {updated_states}")
    
    
    # def entry_doc(self):
    #         print("Inside entry_doc function")
    #         # Fetch the document settings
    #         location_settings = frappe.get_doc("Country Code Logic", self.country)
    #         table = location_settings.country_code_logic_table
    #         doc_name = table[3]  # Assuming table[3] is correct

    #         print(f"Document name: {doc_name}\n")

    #         if doc_name.select == "Empty":
    #             # Prepare new document data
    #             new_doc_data = {
    #                 'doctype': 'Districts',
    #                 "unique_code": self.unique_code,
    #                 "district_name": self.name,
    #                 "country": self.country,
    #                 "state_code": self.unique_code,
    #                 "code_digit_option": "Single(1)",
    #                 "district_code": self.unique_code
    #             }
                
    #             # Create the new document
    #             new_doc = frappe.get_doc(new_doc_data)

    #             try:
    #                 new_doc.insert()
    #                 new_doc.save()
    #                 new_doc.submit()
    #                 frappe.db.commit()
    #                 print("New document created and committed successfully.")
    #             except Exception as e:
    #                 frappe.log_error(message=str(e), title="Error Creating States Document")
    #                 frappe.msgprint(f"Error: {str(e)}")
    #                 print(f"Error creating document: {e}")

# StateZone.py
# import frappe
# from frappe.model.document import Document

# class StateZone(Document):
#     def before_save(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

#         if self.is_new():
#             self.update_zone_wise_count()
#             self.update_unique_code()
            

#     def update_zone_wise_count(self):
#         # Count the number of 'State Zone' records for the specified state
#         location_settings = frappe.get_single("Location wise Code Settings")
        
#         # Retrieve the code_digit_option from the settings document
#         code_digit_option = location_settings.states
    
#         # Set the `code_digit_option` field in the CountryZone doctype
#         self.code_digit_option = code_digit_option
#         count = frappe.db.count("State Zone", filters={"state": self.state}) + 1  # Always add 1 to the count

#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.zone_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.zone_wise_count = str(count).zfill(2)  # Format as two digits with leading zero

#     def update_unique_code(self):
#         # Fetch the unique code from the "States" document
#         country_code = frappe.db.get_value("States", self.state, "unique_code")

#         if country_code:
#             self.unique_code = country_code + str(self.zone_wise_count)
#         else:
#             self.unique_code = str(self.zone_wise_count)

#     def after_insert(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

#         self.update_state_zone_on_states_save()
#         self.entry_doc()
       

#     def update_state_zone_on_states_save(self):
#         # Fetch the corresponding "States" document based on the state
#         state_zone = frappe.get_doc("States", {"name": self.state})

#         # Check if the state already exists in the child table
#         existing_state = next((row for row in state_zone.state_zone_list if row.state_zone_id == self.name), None)
            
#         if not existing_state:
#             # Assign the state_code for new state
#             count = frappe.db.count("State Zone", filters={"state": self.state})
#             new_code = count + 1
            
#             # Append a new row in the state_zone_code child table of the "States" document
#             new_row = state_zone.append("state_zone_list", {})
#             new_row.state_zone_id = self.name
#             new_row.state_zone_code = new_code

#             # Save the "States" document
#             state_zone.save(ignore_permissions=True)    

#             # Debug: Print the updated states and their codes (for debugging purposes)
#             updated_states = [(row.state_zone_id, row.state_zone_code) for row in state_zone.state_zone_list]
#             # print(f"Updated States after update: {updated_states}")

#     def entry_doc(self):
#             location_settings = frappe.get_doc("Country Code Logic", self.country)
#             table = location_settings.country_code_logic_table
#             doc_name = table[3]
            
#             if doc_name.select == "Empty":
#                 # Create the States document
               
#                 new_doc_data = {
#                     'doctype': 'Districts',
#                     "unique_code": self.unique_code,
#                    "zone_type": "City",
#                     "district_name":self.name,
#                     "country": self.country,
#                     "state_code":self.unique_code,
#                     "code_digit_option": "Single(1)",
                    
#                     "zone_name": getattr(self, 'zone_name', ''),
#                      "district_code":self.unique_code 
                            
#             # Fallback to empty string if zone_name is missing
#                     # Add other fields as needed
#                 }
                
#                 # Create the document
#                 new_doc = frappe.get_doc(new_doc_data)

#                 try:
#                     new_doc.insert()
#                     new_doc.save()
#                     new_doc.submit()
#                     frappe.db.commit()

#                 except Exception as e:
#                     frappe.log_error(message=str(e), title="Error Creating States Document")
#                     frappe.msgprint(f"Error: {str(e)}")