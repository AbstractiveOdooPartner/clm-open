{
    "name": "CLM Contact Manager Website Fix",
    "version": "17.0.0.0.0",
    "summary": "Fixes CLM Contact Manager error when Website is installed",
    "author": "Abstractive BV",
    "maintainer": "Abstractive BV",
    "website": "http://abstractive.be",
    "contributors": [
        "Sibert Aerts",
    ],
    "license": "Other proprietary",
    "category": "Uncategorized",
    "depends": [
        "website",
        "clm_contact_manager",
    ],
    "auto_install": True,
    "assets": {
        # NOTE: This asset inclusion is copied from website_form_project that suffers the exact same issue.
        "clm_contact_manager.webclient": [
            # In website, there is a patch of the LinkDialog (see
            # website/static/src/js/editor/editor.js) that require the utils.js.
            # Thus, when website is installed, this bundle need to have the
            # utils.js in its assets, otherwise, there will be an unmet
            # dependency.
            "website/static/src/js/utils.js",
            "web/static/src/core/autocomplete/*",
            "website/static/src/components/autocomplete_with_pages/*",
        ],
    },
}
