# # Copyright (c) 2024, Sanskar technolab and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document


# class Street(Document):
#     def before_save(self):
#         if self.is_new():
#             self.update_street_wise_count()
#             self.update_unique_code()

#     def update_street_wise_count(self):
#         # Count the number of 'Street' records for the specified sub-society
#         location_settings = frappe.get_single("Location wise Code Settings")

#         # Retrieve the code_digit_option from the settings document
#         code_digit_option = location_settings.states
#         # frappe.msgprint(f"Code Digit Option: {code_digit_option}")

#         # Set the `code_digit_option` field in the CountryZone doctype
#         self.code_digit_option = code_digit_option
#         count = (
#             frappe.db.count("Street", filters={"sub_society": self.sub_society}) + 1
#         )  # Always add 1 to start count from 1

#         max_single_count = 9  # For "Single(1)", max allowed count is 9
#         max_double_count = 99 

#         if self.code_digit_option == "Single(1)" and count > max_single_count:
#             frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
#         elif self.code_digit_option == "Double(01)" and count > max_double_count:
#             frappe.throw("Cannot add more records. Maximum limit of 99 reached.")

#         if self.code_digit_option == "Single(1)" :
#             # When 'Single(1)' is selected, display the count as a single digit
#             self.street_wise_count = str(count)  # No leading zero

#         elif self.code_digit_option == "Double(01)":
#             # When 'Double(01)' is selected, display the count as two digits with leading zeros
#             self.street_wise_count = str(count).zfill(
#                 2
#             )  # Format as two digits with leading zero

#     def update_unique_code(self):
#         # Fetch the custom country code from the 'Country' doctype
#         country_code = frappe.db.get_value(
#             "Sub Society", self.sub_society, "unique_code"
#         )

#         if country_code:
#             # Concatenate the country code with the formatted count
#             self.unique_code = country_code + self.street_wise_count
#         else:
#             self.unique_code = self.street_wise_count

#     def after_insert(self):
#         self.update_district_on_states_save()
#         # # Retrieve the Country Code Logic document based on the country of the current Street instance
#         # country_code_logic_doc = frappe.db.get_value("Country Code Logic", {"country": self.country}, "name")

#         # if country_code_logic_doc:
#         #     country_code_logic_doc = frappe.get_doc("Country Code Logic", {"country": self.country})
#         #     is_street_empty = any(
#         #         row.doctype_list == "Street" and row.select == "Empty"
#         #         for row in country_code_logic_doc.country_code_logic_table
#         #     )

#         #     if is_street_empty:
#         #         return
        

#     def update_district_on_states_save(self):
#         # Get the Sub Society document associated with this Street instance
#         sub_society_doc = frappe.get_doc("Sub Society", {"name": self.sub_society})

#         sub_society_doc.flags.ignore_permissions = True  # Bypass permission checks
#         sub_society_doc.flags.ignore_validate_update_after_submit = True

#         # Check if the street already exists in the child table
#         existing_street = next((row for row in sub_society_doc.street_list if row.street_id == self.name), None)

#         if not existing_street:
#             count = frappe.db.count("Street", filters={"sub_society": self.sub_society})
#             new_code = count + 1

#             new_row = sub_society_doc.append("street_list", {})
#             new_row.street_id = self.name
#             new_row.street_code = new_code

#             sub_society_doc.save(ignore_permissions=True)

#         updated_streets = [(row.street_id, row.street_code) for row in sub_society_doc.street_list]
#         print(f"Updated Streets after update: {updated_streets}")




import frappe
from frappe.model.document import Document

class Street(Document):

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
            # Access the first row of the child table
            first_row = location_settings.country_code_logic_table[9]
            value = first_row.select  # Assuming 'select' is the field you need to check

            # Set final_code_digit_option based on the value of 'select'
            if value == "Single":
                final_code_digit_option = "1"
            elif value == "Double":
                final_code_digit_option = "01"
              
        
        if final_code_digit_option =="1":
            self.code_digit_option = "Single(1)"
        elif final_code_digit_option == "01":
            self.code_digit_option = "Double(01)"

        count = (
            frappe.db.count("Street", filters={"sub_society": self.sub_society}) + 1
        )  
        
        max_single_count = 9  # For "Single(1)", max allowed count is 9
        max_double_count = 99 

        if self.code_digit_option == "Single(1)" and count > max_single_count:
            frappe.throw("Cannot add more records. Maximum limit of 9 reached .")
        elif self.code_digit_option == "Double(01)" and count > max_double_count:
            frappe.throw("Cannot add more records. Maximum limit of 99 reached.")



        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.street_wise_count = str(count)  # No leading zero, starts from 1

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.street_wise_count = str(count).zfill(2) 


   
    def update_unique_code(self):
        # Fetch the unique code from the 'Sub Society' doctype
        country_code = frappe.db.get_value("Sub Society", self.sub_society, "unique_code")
        print("country_code...",type(country_code))
        print("self.street_wise_count",self.street_wise_count)


        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.street_wise_count
        else:
            self.unique_code = self.street_wise_count

    def after_insert(self):
        self.update_district_on_states_save()
        # # Check if the current process is running within an RQ job context
        # if frappe.flags.in_rq_job:
        #     # Skip the update logic when running in RQ job context
        #     return

        # # Retrieve the Country Code Logic document based on the country of the current Street instance
        # country_code_logic_doc = frappe.db.get_value("Country Code Logic", {"country": self.country}, "name")

        # if country_code_logic_doc:
        #     country_code_logic_doc = frappe.get_doc("Country Code Logic", {"country": self.country})
        #     is_street_empty = any(
        #         row.doctype_list == "Street" and row.select == "Empty"
        #         for row in country_code_logic_doc.country_code_logic_table
        #     )

        #     if is_street_empty:
        #         return
        

    def update_district_on_states_save(self):
        # Get the Sub Society document associated with this Street instance
        sub_society_doc = frappe.get_doc("Sub Society", {"name": self.sub_society})


        sub_society_doc.flags.ignore_permissions = True  # Bypass permission checks
        sub_society_doc.flags.ignore_validate_update_after_submit = True


        # Check if the street already exists in the child table
        existing_street = next(
            (row for row in sub_society_doc.street_list if row.street_id == self.name), None
        )

        if not existing_street:
            count = frappe.db.count("Street", filters={"sub_society": self.sub_society})
            new_code = count + 1

            new_row = sub_society_doc.append("street_list", {})
            new_row.street_id = self.name
            new_row.street_code = new_code

            sub_society_doc.save(ignore_permissions=True)

        # Debug: Print the updated streets and their codes
        updated_streets = [(row.street_id, row.street_code) for row in sub_society_doc.street_list]
        print(f"Updated Streets after update: {updated_streets}")
