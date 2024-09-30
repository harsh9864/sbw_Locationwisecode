# # Area.py
# import frappe
# from frappe.model.document import Document

# class Area(Document):
#     skip_unique_code_update = False
#     def before_save(self):
#         # Check if the current process is running within an RQ job context
#         if frappe.flags.in_rq_job:
#             # Skip the update logic when running in RQ job context
#             return

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
#             first_row = location_settings.country_code_logic_table[5]
#             value = first_row.select  # Assuming 'select' is the field you need to check

#             # Set final_code_digit_option based on the value of 'select'
#             if value == "Single":
#                 final_code_digit_option = "1"
#             elif value == "Double":
#                 final_code_digit_option = "01"
              
        
#         if final_code_digit_option == "1":
#             self.code_digit_option = "Single(1)"
#         elif final_code_digit_option == "01":
#             self.code_digit_option = "Double(01)"

#         count = frappe.db.count("Area", filters={"district_zone": self.district_zone}) + 1  # Always add 1 to the count

#         # Define maximum allowed counts based on code_digit_option
#         max_single_count = 9  # For "Single(1)", max allowed count is 9
#         max_double_count = 99  # For "Double(01)", max allowed count is 99

#         # Check if the count exceeds the maximum allowed based on code_digit_option
#         if self.code_digit_option == "Single(1)" and count > max_single_count:
#             frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
#         elif self.code_digit_option == "Double(01)" and count > max_double_count:
#             frappe.throw("Cannot add more records. Maximum limit of 99 reached.")

#         if self.code_digit_option == "Single(1)":
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.area_wise_count = str(count)  # No leading zero, starts from 1

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.area_wise_count = str(count).zfill(2)
# Area.py
import frappe
from frappe.model.document import Document

class Area(Document):
    skip_unique_code_update = False

    def before_save(self):
        # Check if the current process is running within an RQ job context
        if frappe.flags.in_rq_job:
            # Skip the update logic when running in RQ job context
            return

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
            # Access the sixth row of the child table (for the area logic)
            sixth_row = location_settings.country_code_logic_table[5]
            value = sixth_row.select  # Assuming 'select' is the field you need to check

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

        # Calculate the count for the area
        count = frappe.db.count("Area", filters={"district_zone": self.district_zone}) + 1  # Always add 1 to the count

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

        # Set the area_wise_count based on the code_digit_option
        if self.code_digit_option == "Single(1)":
            # For "Single(1)", display the count as a single digit
            self.area_wise_count = str(count)  # No leading zero, starts from 1
        elif self.code_digit_option == "Double(01)":
            # For "Double(01)", display the count as two digits with leading zeros
            self.area_wise_count = str(count).zfill(2)  # Format as two digits with leading zero
        elif self.code_digit_option == "Triple(001)":
            # For "Triple(001)", display the count as three digits with leading zeros
            self.area_wise_count = str(count).zfill(3)  # Format as three digits with leading zero


    def update_unique_code(self):
        if self.skip_unique_code_update:
            return
        # Fetch the unique code from the 'District Zone' doctype
        country_code = frappe.db.get_value("District Zone", self.district_zone, "unique_code")

        if country_code:
            # Concatenate the district zone code with the formatted count
            self.unique_code = country_code + self.area_wise_count
        else:
            self.unique_code = self.area_wise_count

    def after_insert(self):
        # Check if the current process is running within an RQ job context
        print("\n\n\n\n\n\n\n\n\n\n\n\n", "after insert")

        try:
            # Debugging before the method call
            print("Before calling update_state_zone_on_states_save...")
            self.update_district_on_states_save()
            print("After calling update_state_zone_on_states_save...")

            # Debugging before entry_doc method
            print("Attempting to call entry_doc...")
            self.entry_doc()  # Attempt to call the function
            print("entry_doc() called successfully.")
        except Exception as e:
            print(f"Error while calling entry_doc(): {e}")

    def update_district_on_states_save(self):
        # Fetch the corresponding 'District Zone' document based on the district zone
        area = frappe.get_doc("District Zone", {"name": self.district_zone})


        area.flags.ignore_permissions = True  # Bypass permission checks
        area.flags.ignore_validate_update_after_submit = True


        # Check if the area already exists in the child table
        existing_state = next((row for row in area.area_list if row.area_id == self.name), None)

        if not existing_state:
            # Assign the area_wise_code for the new area
            count = frappe.db.count("Area", filters={"district_zone": self.district_zone})
            new_code = count + 1

            # Append a new row in the area_list child table of District Zone
            new_row = area.append("area_list", {})
            new_row.area_id = self.name
            new_row.area_wise_code = new_code

            # Save the District Zone document
            area.save(ignore_permissions=True)

            # Debug: Print the updated areas and their codes (for debugging purposes)
            updated_states = [(row.area_id, row.area_wise_code) for row in area.area_list]
            # print(f"Updated Areas after update: {updated_states}")


    
    def entry_doc(self):
            print("Inside entry_doc function")
            # Fetch the document settings
            location_settings = frappe.get_doc("Country Code Logic", self.country)
            table = location_settings.country_code_logic_table
            doc_name = table[6]  # Assuming table[3] is correct

            
            if doc_name.select == "Empty":
                print(f"Document ppp: {doc_name.select}\n")

                # Prepare new document data
                new_doc_data = {
                    'doctype': 'Area Zone',
                    "unique_code": self.unique_code,
                    "area_name": self.name,
                    "country": self.country,
                    # "state_code": self.unique_code,
                    "code_digit_option": "Single(1)",
                    "district_code": self.unique_code,
                    "zone_name":self.area_name,
                    "area":self.name,
                    "area_code":self.unique_code,
                    "area_name":self.name,
                    # "zone_type":"City",
                    # "district":self.name
                }
                
                # Create the new document
                new_doc = frappe.get_doc(new_doc_data)
                new_doc.skip_unique_code_update = True
                print(f"New document: {new_doc}")

                try:
                    new_doc.insert()
                    new_doc.save()
                    new_doc.submit()
                    frappe.db.commit()
                    print("New document created and committed ful.")
                except Exception as e:
                    frappe.log_error(message=str(e), title="Error Creating States Document")
                    frappe.msgprint(f"Error: {str(e)}")
                    print(f"Error creating document: {e}")

