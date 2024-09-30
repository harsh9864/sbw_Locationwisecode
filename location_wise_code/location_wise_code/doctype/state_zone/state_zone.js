// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("State Zone", {
    refresh: function (frm) {
        frm.fields_dict['district_list'].grid.wrapper.find('.grid-add-row').hide();
        if (!frm.is_new()) {
            frm.set_df_property('zone_name', 'read_only', 1);
            frm.set_df_property('state', 'read_only', 1);
            frm.set_df_property('country', 'read_only', 1);

        }
    },
    
});
