odoo.define('clm_base.form', function (require) {
'use strict';

var core = require('web.core');
var FormEditorRegistry = require('website.form_editor_registry');

var _t = core._t;

FormEditorRegistry.add('website_form_entry', {
    formFields: [{
        type: 'char',
        required: true,
        readonly: true,
        fillWith: 'name',
        name: 'name',
        string: 'Your Name',
    }, {
        type: 'email',
        required: true,
        readonly: true,
        fillWith: 'email',
        name: 'email_from',
        string: 'Your Email',
    }, {
        type: 'char',
        name: 'description',
        string: 'Description',
    }],
});

});
