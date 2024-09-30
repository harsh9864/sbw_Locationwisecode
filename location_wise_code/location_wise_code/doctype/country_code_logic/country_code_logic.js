// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("Country Code Logic", {
    onload(frm) {
		if (frm.doc.__islocal) {
			return frm.call("get_data").then(() => {
				frm.refresh_field("country_code_logic_table");
			});
		}
	},
	refresh(frm) {

	},
});

frappe.ui.form.on('Country Code Logic Table', {
    select: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn); // Get the current row
        let parent_value = frm.doc.country_code || ''; // Assuming this is the field you're updating based on logic
        let previous_preview_value = find_nearest_previous_value(frm, row.idx); // Function to find the nearest non-empty preview value

        // Generic function to handle value updates
        function update_preview(select_value, base_value) {
            switch (select_value) {
                case 'Single':
                    return base_value + "1";
                case 'Double':
                    return base_value + "01";
                case 'Triple':  // New case for "Triple"
                    return base_value + "001";
                case 'Empty':   
                    return base_value;
                case 'Not Required':
                    return "";
                default:
                    return base_value;
            }
        }

        // Determine base value based on doctype_list
        let base_value = (row.doctype_list === "Country Zone") ? parent_value : previous_preview_value;

        // Update the preview field based on the selection
        let new_preview_value = update_preview(row.select, base_value);
        frappe.model.set_value(cdt, cdn, 'preview', new_preview_value);

        // Handle "Not Required" case to set for all subsequent rows
        if (row.select === 'Not Required') {
            frm.doc.country_code_logic_table.forEach(function(d) {
                if (d.idx > row.idx) {
                    frappe.model.set_value(d.doctype, d.name, 'select', 'Not Required');
                }
            });
        }
    }
});

// Function to find the nearest non-empty previous row's preview value
function find_nearest_previous_value(frm, current_idx) {
    let previous_value = '';
    frm.doc.country_code_logic_table.forEach(function(d) {
        if (d.idx < current_idx && d.preview) {
            previous_value = d.preview;
        }
    });
    return previous_value;
}



// frappe.ui.form.on('Country Code Logic Table', {
//     refresh(frm) {
//         // Optional: You can use this if you need to refresh specific fields
//     },
//     select: function (frm, cdt, cdn) {
//         // Get the current row of the child table
//         let row = frappe.get_doc(cdt, cdn);
//         let parent_value = frm.doc.country_code; // Fetch the parent field value
//         let previous_preview_value = "";

//         // Find the index of the current row
//         const rowIndex = frm.doc.country_code_logic_table.findIndex(
//             r => r.name === row.name
//         );

//         // Access the preview value of the previous row, if available
//         if (rowIndex > 0) {
//             previous_preview_value = frm.doc.country_code_logic_table[rowIndex - 1].preview || "";
//         }

//         // Handling logic based on the row's doctype_list
//         if (row.doctype_list === "Country Zone") {
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', parent_value + "1");
//             } else if (row.select === 'Double') {
//                 let updated_value = parent_value + "01";
//                 frappe.model.set_value(cdt, cdn, 'preview', updated_value);
//                 console.log("Updated Value (Double):", updated_value);
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         } else if (row.doctype_list === "States") {
//             // Use the previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "State Zone") {
//             // Use the previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Districts") {
//             // Use the previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }else if (row.doctype_list === "District Zone") {
//             // Use the previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Area") {
//             // Use the previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         // Refresh the field after updating
//         frm.refresh_field('country_code_logic_table');
//     }
// });


// frappe.ui.form.on('Country Code Logic Table', {
//     refresh(frm) {
//         // Optional: Additional refresh logic if needed
//     },
//     select: function (frm, cdt, cdn) {
//         // Get the current row of the child table
//         let row = frappe.get_doc(cdt, cdn);
//         let parent_value = frm.doc.country_code; // Fetch the parent field value
//         let previous_preview_value = "";

//         // Find the index of the current row in the child table
//         const rowIndex = frm.doc.country_code_logic_table.findIndex(
//             r => r.name === row.name
//         );

//         // Find the nearest previous non-empty 'preview' value by looping backward
//         for (let i = rowIndex - 1; i >= 0; i--) {
//             const prevRow = frm.doc.country_code_logic_table[i];
//             if (prevRow.preview) {  // Check if the preview value is not empty
//                 previous_preview_value = prevRow.preview;
//                 console.log("preview value:",previous_preview_value);
//                 break; 
//             }
//         }

//         // Handling logic based on the row's doctype_list
//         if (row.doctype_list === "Country Zone") {
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', parent_value + "1");
//             } else if (row.select === 'Double') {
//                 let updated_value = parent_value + "01";
//                 frappe.model.set_value(cdt, cdn, 'preview', updated_value);
//                 console.log("Updated Value (Double):", updated_value);
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', parent_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         } else if (row.doctype_list === "States") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "State Zone") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Districts") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             } else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "District Zone") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             }  else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Area") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             }  else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Area Zone") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             }  else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Society") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             }  else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }
//         else if (row.doctype_list === "Street") {
//             // Use the nearest non-empty previous row's preview value in the conditions
//             if (row.select === 'Single') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "1");
//             } else if (row.select === 'Double') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value + "01");
//                 console.log("Updated Value (Double):", previous_preview_value + "0");
//             }  else if (row.select === 'Empty') {
//                 frappe.model.set_value(cdt, cdn, 'preview', previous_preview_value);
//             }
//             else if (row.select === 'Not Required') {
//                 frappe.model.set_value(cdt, cdn, 'preview', "");
//             }
//         }

//         // Refresh the field after updating the preview value
//         frm.refresh_field('country_code_logic_table');
//     }
// });
