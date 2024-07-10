{
    "name": "CLM Contact Manager",
    "version": "17.0.0.0.0",
    "summary": "Replaces /my/account with an embedded back-end res.partner form view",
    "author": "Abstractive BV",
    "maintainer": "Abstractive BV",
    "website": "http://abstractive.be",
    "contributors": [
        "Odoo SA",
        "Vincent Baggerman",
        "Bart D'haese",
        "Sibert Aerts",
    ],
    "license": "Other proprietary",
    "category": "Uncategorized",
    "depends": [
        "base_setup",
        "contacts",
        "portal",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "templates/contact_portal.xml",
    ],
    "assets": {
        # NOTE: This entire block is copied and adjusted from "project.webclient"
        "clm_contact_manager.webclient": [
            ("include", "web._assets_helpers"),
            ("include", "web._assets_backend_helpers"),

            "web/static/src/scss/pre_variables.scss",
            "web/static/lib/bootstrap/scss/_variables.scss",

            "web/static/src/libs/fontawesome/css/font-awesome.css",
            "web/static/lib/odoo_ui_icons/*",
            "web/static/lib/select2/select2.css",
            "web/static/lib/select2-bootstrap-css/select2-bootstrap.css",
            "web/static/src/webclient/navbar/navbar.scss",
            "web/static/src/scss/animation.scss",
            "web/static/src/core/colorpicker/colorpicker.scss",
            "web/static/src/scss/mimetypes.scss",
            "web/static/src/scss/ui.scss",
            "web/static/src/legacy/scss/ui.scss",
            "web/static/src/views/fields/translation_dialog.scss",
            "web/static/src/scss/fontawesome_overridden.scss",

            "web/static/src/module_loader.js",
            "web/static/src/session.js",

            "web/static/lib/luxon/luxon.js",
            "web/static/lib/owl/owl.js",
            "web/static/lib/owl/odoo_module.js",
            "web/static/lib/jquery/jquery.js",
            "web/static/lib/popper/popper.js",
            "web/static/lib/bootstrap/js/dist/dom/data.js",
            "web/static/lib/bootstrap/js/dist/dom/event-handler.js",
            "web/static/lib/bootstrap/js/dist/dom/manipulator.js",
            "web/static/lib/bootstrap/js/dist/dom/selector-engine.js",
            "web/static/lib/bootstrap/js/dist/base-component.js",
            "web/static/lib/bootstrap/js/dist/alert.js",
            "web/static/lib/bootstrap/js/dist/button.js",
            "web/static/lib/bootstrap/js/dist/carousel.js",
            "web/static/lib/bootstrap/js/dist/collapse.js",
            "web/static/lib/bootstrap/js/dist/dropdown.js",
            "web/static/lib/bootstrap/js/dist/modal.js",
            "web/static/lib/bootstrap/js/dist/offcanvas.js",
            "web/static/lib/bootstrap/js/dist/tooltip.js",
            "web/static/lib/bootstrap/js/dist/popover.js",
            "web/static/lib/bootstrap/js/dist/scrollspy.js",
            "web/static/lib/bootstrap/js/dist/tab.js",
            "web/static/lib/bootstrap/js/dist/toast.js",
            "web/static/lib/select2/select2.js",
            "web/static/src/legacy/js/libs/bootstrap.js",
            "web/static/src/legacy/js/libs/jquery.js",
            ("include", "web._assets_bootstrap_backend"),

            "base/static/src/css/modules.css",

            "web/static/src/core/utils/transitions.scss",
            "web/static/src/core/**/*",
            "web/static/src/model/**/*",
            "web/static/src/search/**/*",
            "web/static/src/webclient/icons.scss", # variables required in list_controller.scss
            "web/static/src/views/**/*.js",
            "web/static/src/views/*.xml",
            "web/static/src/views/*.scss",
            "web/static/src/views/fields/**/*",
            "web/static/src/views/form/**/*",
            "web/static/src/views/kanban/**/*",
            "web/static/src/views/list/**/*",
            "web/static/src/views/view_button/**/*",
            "web/static/src/views/view_components/**/*",
            "web/static/src/views/view_dialogs/**/*",
            "web/static/src/views/widgets/**/*",
            "web/static/src/webclient/**/*",
            ("remove", "web/static/src/webclient/clickbot/clickbot.js"), # lazy loaded
            ("remove", "web/static/src/views/form/button_box/*.scss"),
            ("remove", "web/static/src/core/emoji_picker/emoji_data.js"),

            # remove the report code and whitelist only what"s needed
            ("remove", "web/static/src/webclient/actions/reports/**/*"),
            "web/static/src/webclient/actions/reports/*.js",
            "web/static/src/webclient/actions/reports/*.xml",

            "web/static/src/env.js",

            ("include", "web_editor.assets_wysiwyg"),

            "web/static/src/legacy/scss/fields.scss",

            "base/static/src/scss/res_partner.scss",

            # Form style should be computed before
            "web/static/src/views/form/button_box/*.scss",

            "web_editor/static/src/js/editor/odoo-editor/src/base_style.scss",
            "web_editor/static/lib/vkbeautify/**/*",
            "web_editor/static/src/js/common/**/*",
            "web_editor/static/src/js/editor/odoo-editor/src/utils/utils.js",
            "web_editor/static/src/js/wysiwyg/fonts.js",

            "web_editor/static/src/components/**/*",
            "web_editor/static/src/scss/web_editor.common.scss",
            "web_editor/static/src/scss/web_editor.backend.scss",

            "web_editor/static/src/js/backend/**/*",
            "web_editor/static/src/xml/backend.xml",

            "mail/static/src/scss/variables/*.scss",
            "mail/static/src/views/web/form/form_renderer.scss",

            "clm_contact_manager/static/src/contact_sharing/**/*",

            "web/static/src/start.js",
        ],
    },
}
