


frappe.ui.form.on('Location wise Code Settings', {
    country_zone: function(frm) {
        update_preview_fields(frm);
    },
    states: function(frm) {
        update_preview_fields(frm);
    },
    state_zone: function(frm) {
        update_preview_fields(frm);
    },
    districts: function(frm) {
        update_preview_fields(frm);
    },
    district_zone: function(frm) {
        update_preview_fields(frm);
    },
    area: function(frm) {
        update_preview_fields(frm);
    },
    area_zone: function(frm) {
        update_preview_fields(frm);
    },
    society: function(frm) {
        update_preview_fields(frm);
    },
    sub_society: function(frm) {
        update_preview_fields(frm);
    },
    street: function(frm) {
        update_preview_fields(frm);
    }
});

// Unified function to update preview fields based on the values of each selection
function update_preview_fields(frm) {
    // Base codes based on field selections
    const code_map = {
        'Single(1)': '1',
        'Double(01)': '01'
    };

    // Fetch values based on the selected options and update corresponding preview fields
    const country_code = frm.doc.country_zone === 'Single(1)' ? '911' : frm.doc.country_zone === 'Double(01)' ? '9101' : '';
    const state_code = frm.doc.states ? code_map[frm.doc.states] || '' : '';
    const state_zone_code = frm.doc.state_zone ? code_map[frm.doc.state_zone] || '' : '';
    const district_code = frm.doc.districts ? code_map[frm.doc.districts] || '' : '';
    const district_zone_code = frm.doc.district_zone ? code_map[frm.doc.district_zone] || '' : '';
    const area_code = frm.doc.area ? code_map[frm.doc.area] || '' : '';
    const area_zone_code = frm.doc.area_zone ? code_map[frm.doc.area_zone] || '' : '';
    const society_code = frm.doc.society ? code_map[frm.doc.society] || '' : '';
    const sub_society_code = frm.doc.sub_society ? code_map[frm.doc.sub_society] || '' : '';
    const street_code = frm.doc.street ? code_map[frm.doc.street] || '' : '';

    // Set preview fields based on combined codes
    frm.set_value('data_uink', country_code );
    frm.set_value('states_preview', country_code + state_code);
    frm.set_value('state_zone_preview', country_code + state_code + state_zone_code);
    frm.set_value('districts_preview', country_code + state_code + state_zone_code + district_code);
    frm.set_value('districts_zone_preview', country_code + state_code + state_zone_code + district_code + district_zone_code);
    frm.set_value('districts_zone_preview____copy', country_code + state_code + state_zone_code + district_code + district_zone_code + area_code);
    frm.set_value('area_zone_preview', country_code + state_code + state_zone_code + district_code + district_zone_code + area_code + area_zone_code);
    frm.set_value('society_preview', country_code + state_code + state_zone_code + district_code + district_zone_code + area_code + area_zone_code + society_code);
    frm.set_value('sub_society_preview', country_code + state_code + state_zone_code + district_code + district_zone_code + area_code + area_zone_code + society_code + sub_society_code);
    frm.set_value('street_preview', country_code + state_code + state_zone_code + district_code + district_zone_code + area_code + area_zone_code + society_code + sub_society_code + street_code);
}
