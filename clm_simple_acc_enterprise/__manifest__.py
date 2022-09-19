{
    "name": "CLM Simple Accounting View (Enterprise)",
    "version": "15.0.0.0.0",
    "author": "Abstractive BV",
    "maintainer": "Abstractive BV",
    "website": "http://abstractive.be",
    "contributors": ["Bart D'haese"],
    "license": "Other proprietary",
    "category": "Uncategorized",
    # any module necessary for this one to work correctly
    "depends": ["account"],
    # always loaded
    "data": [
        "data/res_groups.xml",
        "data/ir_rule.xml",
        "data/ir_ui_view.xml",
    ],
}
