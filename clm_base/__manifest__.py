{
    "name": "CLM Base",
    "version": "15.0.0.0.0",
    "author": "Abstractive BV",
    "maintainer": "Abstractive BV",
    "website": "http://abstractive.be",
    "contributors": ["Bart D'haese"],
    "license": "Other proprietary",
    "category": "Uncategorized",
    # any module necessary for this one to work correctly
    "depends": ["contacts", "website",],
    # always loaded
    "data": [
        "data/ir_model_data.xml",
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/website_form_entry.xml",
    ],
    'assets': {
        'website.assets_editor': [
            'clm_base/static/src/**/*',
        ],
    },
}
