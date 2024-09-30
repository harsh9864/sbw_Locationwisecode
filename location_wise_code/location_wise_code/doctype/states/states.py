# import frappe
# from frappe.model.document import Document

# class States(Document):
#     skip_unique_code_update = False
#     def before_save(self):
#         if self.is_new():
#         # Update the state count and unique code before saving
#             self.update_state_count()
#             self.update_unique_code() 
            
        


    

#     def update_state_count(self):
#         # Fetch the single document from the 'Country Code Logic' doctype
#         location_settings = frappe.get_doc("Country Code Logic", self.country)

#         # Initialize final_code_digit_option
#         final_code_digit_option = None

#         # Check if the child table has at least one row
#         if location_settings.country_code_logic_table:
#             # Access the first row of the child table
#             first_row = location_settings.country_code_logic_table[1]
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

#         count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country}) + 1  # Always add 1 to the count

#         max_single_count = 9  # For "Single(1)", max allowed count is 9
#         max_double_count = 99 

#         if self.code_digit_option == "Single(1)" and count > max_single_count:
#             frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
#         elif self.code_digit_option == "Double(01)" and count > max_double_count:
#             frappe.throw("Cannot add more records. Maximum limit of 99 reached.")


#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.state_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.state_wise_count = str(count).zfill(2) 
import frappe
from frappe.model.document import Document

class States(Document):
    skip_unique_code_update = False

    def before_save(self):
        if self.is_new():
            # Update the state count and unique code before saving
            self.update_state_count()
            self.update_unique_code()

    def update_state_count(self):
        # Fetch the single document from the 'Country Code Logic' doctype
        location_settings = frappe.get_doc("Country Code Logic", self.country)

        # Initialize final_code_digit_option
        final_code_digit_option = None

        # Check if the child table has at least one row
        if location_settings.country_code_logic_table:
            # Access the first row of the child table (assuming second row is relevant here)
            first_row = location_settings.country_code_logic_table[1]
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

        # Calculate the count for the state in the given zone and country
        count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country}) + 1  # Always add 1 to the count

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

        # Set the state_wise_count based on the code_digit_option
        if self.code_digit_option == "Single(1)":
            # For "Single(1)", display count as a single digit
            self.state_wise_count = str(count)  # No leading zeros, starts from 1
        elif self.code_digit_option == "Double(01)":
            # For "Double(01)", display count as two digits with leading zeros
            self.state_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
        elif self.code_digit_option == "Triple(001)":
            # For "Triple(001)", display count as three digits with leading zeros
            self.state_wise_count = str(count).zfill(3)  # Format as three digits with leading zero

    def update_unique_code(self):
        if self.skip_unique_code_update:
            return
        # Fetch the unique code from the Country Zone
        unique_code = frappe.db.get_value('Country Zone', self.country_zone, 'unique_code')

        # Concatenate the unique code with state_wise_count
        self.unique_code = unique_code + str(self.state_wise_count) if unique_code else str(self.state_wise_count)

    def after_insert(self):
        # Validate method is called before saving; update the Country Zone as needed
        # print("Validating State")
        # print("\n\n\n\n\n\n\n\n\n\n\n\n","STats",)
        self.update_country_zone_on_states_save()
        self.entry_doc()
        

    def update_country_zone_on_states_save(self):
      
        country_zone = frappe.get_doc("Country Zone", {"name": self.country_zone})


        country_zone.flags.ignore_permissions = True  # Bypass permission checks
        country_zone.flags.ignore_validate_update_after_submit = True

        if not country_zone:
            
            return

        
        existing_states = [(row.state_name, row.state_code) for row in country_zone.states_list]
        
        existing_state = next((row for row in country_zone.states_list if row.state_id == self.name), None)
        
        if not existing_state:
           
            count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country})
            new_code = count + 1
            
            
            new_row = country_zone.append("states_list", {})
            new_row.state_id = self.name
            new_row.state_code = new_code

            
            country_zone.save(ignore_permissions=True)

            # Debug: Print the updated states and their codes
            updated_states = [(row.state_id, row.state_code) for row in country_zone.states_list]
            # print(f"Updated States after update: {updated_states}")

    def entry_doc(self):
        location_settings = frappe.get_doc("Country Code Logic", self.country)
        table = location_settings.country_code_logic_table
        doc_name = table[2]

        if doc_name.select == "Empty":
            
            new_doc_data = {
                'doctype': 'State Zone',
                "unique_code": self.unique_code,
                "state": self.name,
                "country": self.country,
                "state_code":self.unique_code,
                "code_digit_option": "Single(1)",
                "state":self.name,
                "zone_name": self.state_name,  # Fallback to empty string if zone_name is missing
            }
            
            # Create the document
            new_doc = frappe.get_doc(new_doc_data)
            new_doc.skip_unique_code_update = True


            try:
                new_doc.insert()
                new_doc.save()
                new_doc.submit()
                frappe.db.commit()
            except Exception as e:
                frappe.log_error(message=str(e), title="Error Creating States Document")
                frappe.msgprint(f"Error: {str(e)}")


# import frappe
# from frappe.model.document import Document

# class States(Document):
#     def before_save(self):
#         # Skip incrementing the unique code if the document is added via RQ job
#         if frappe.flags.in_rq_job:
#             return
        
#         if self.is_new():
#             # Update the state count and unique code before saving
#             self.update_state_count()
#             self.update_unique_code()
#             self.entry_doc()

#     def update_state_count(self):
#         location_settings = frappe.get_single("Location wise Code Settings")
        
#         # Retrieve the code_digit_option from the settings document
#         code_digit_option = location_settings.states

#         # Set the `code_digit_option` field in the CountryZone doctype
#         self.code_digit_option = code_digit_option

#         # Query to get the count of records for the current country and zone name
#         count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country}) + 1  # Always add 1 to the count

#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.state_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.state_wise_count = str(count).zfill(2)  # Format as two digits with leading zero

#     def update_unique_code(self):
#         # Skip updating the unique code if the document is added via RQ job
#         if frappe.flags.in_rq_job:
#             return
        
#         # Fetch the unique code from the Country Zone
#         unique_code = frappe.db.get_value('Country Zone', self.country_zone, 'unique_code')

#         # Concatenate the unique code with state_wise_count
#         self.unique_code = unique_code + str(self.state_wise_count) if unique_code else str(self.state_wise_count)

#     def after_insert(self):
#         # Skip updating the Country Zone if the document is added via RQ job
#         if frappe.flags.in_rq_job:
#             return
        
#         # Validate method is called before saving; update the Country Zone as needed
#         self.update_country_zone_on_states_save()

#     def update_country_zone_on_states_save(self):
#         # Skip updating the Country Zone if the document is added via RQ job
#         if frappe.flags.in_rq_job:
#             return
        
#         # Fetch the corresponding Country Zone based on the state
#         country_zone = frappe.get_doc("Country Zone", {"name": self.country_zone})
#         if not country_zone:
#             return

#         # Check if the state already exists in the child table
#         existing_state = next((row for row in country_zone.states_list if row.state_id == self.name), None)
        
#         if not existing_state:
#             # Assign the state_code for new state
#             count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country})
#             new_code = count + 1
            
#             # Append a new row in the states_list child table of Country Zone
#             new_row = country_zone.append("states_list", {})
#             new_row.state_id = self.name
#             new_row.state_code = new_code

#             # Save the Country Zone document
#             country_zone.save(ignore_permissions=True)

#     def entry_doc(self):
#         # Fetch the single document from the 'Country Code Logic' doctype
#         try:
#             location_settings = frappe.get_doc("Country Code Logic", self.country)
#         except Exception as e:
#             frappe.log_error(f"Error fetching Country Code Logic document: {str(e)}")
#             frappe.msgprint(f"Error fetching Country Code Logic document: {str(e)}")
#             return

#         # Iterate through each row in the child table 'country_code_logic_table'
#         for i, row in enumerate(location_settings.country_code_logic_table):
#             doctype_name = row.doctype_list
#             current_row_condition = row.select in ["Empty", "Not Required","Single","Double"]

#             # Check if doctype_name matches the desired doctype
#             if doctype_name == row.doctype_list:
#                 # Check if current row condition is met
#                 frappe.msgprint("Country Zone")
#                 if current_row_condition:
#                     frappe.msgprint("Current row condition")
#                     # Check if the next row exists and if its 'select' field value is "Empty" or "Not Required"
#                     if i + 1 < len(location_settings.country_code_logic_table):
#                         next_row = location_settings.country_code_logic_table[2]
#                         frappe.msgprint("Current row conditionooo",next_row.doctype_list)
#                         next_row_condition = next_row.select in ["Empty", "Not Required"]
                        
#                         if next_row_condition:
#                             frappe.msgprint("Current row for tets",next_row_condition)
#                             # Enqueue document creation to run in the background
#                             frappe.enqueue(
#                                 'location_wise_code.api.create_document',
#                                 doctype_name=doctype_name,
#                                 value_to_use=self.unique_code,
#                                 country=location_settings.country,
#                                 name=self.name,
#                                 zone_name=self.zone_name,
#                                 from_rq_job=True  # Pass the flag indicating it's from an RQ job
#                             )
