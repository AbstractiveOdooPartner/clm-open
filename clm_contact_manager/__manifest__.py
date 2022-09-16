{
    "name": "clm_contact_manager",
    "version": "15.0.0.0.0",
    "author": "Abstractive BV",
    "maintainer": "Abstractive BV",
    "website": "http://abstractive.be",
    "contributors": ["Odoo SA","Vincent Baggerman","Bart D'haese"],
    "license": "Other proprietary",
    "category": "Uncategorized",
    # any module necessary for this one to work correctly
    "depends": ["base", "base_setup", "web", "contacts", "portal", "mail", "web_tour"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/contact_portal.xml",
    ],
    "assets": {
        "web.assets_backend_legacy_lazy": [
            "project/static/src/js/*_legacy.js",
        ],
        "clm_contact_manager.assets_qweb": [
            ("include", "web.assets_qweb"),
            "clm_contact_manager/static/src/contact_sharing/**/*.xml",
        ],
        "clm_contact_manager.webclient": [
            ("include", "web.assets_backend"),
            # Remove some fancy form rendering css
            (
                "remove",
                "web/static/src/legacy/scss/form_view_extra.scss",
            ),
            # Remove Longpolling bus and packages needed this bus
            ("remove", "bus/static/src/js/services/assets_watchdog_service.js"),
            ("remove", "mail/static/src/services/messaging/messaging.js"),
            ("remove", "mail/static/src/components/dialog_manager/dialog_manager.js"),
            ("remove", "mail/static/src/services/dialog_service/dialog_service.js"),
            ("remove", "mail/static/src/components/chat_window_manager/chat_window_manager.js"),
            ("remove", "mail/static/src/services/chat_window_service/chat_window_service.js"),
            "web/static/src/legacy/js/public/public_widget.js",
            "portal/static/src/js/portal_chatter.js",
            "portal/static/src/js/portal_composer.js",
            "clm_contact_manager/static/src/contact_sharing/**/*.js",
            "clm_contact_manager/static/src/scss/contact_sharing/*",
            "web/static/src/start.js",
            "web/static/src/legacy/legacy_setup.js",
        ],
    },
}
