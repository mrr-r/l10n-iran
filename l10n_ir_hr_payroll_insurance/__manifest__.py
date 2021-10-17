# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Iran - Employee payroll insurance",
    "version": "14.0.3.0.0",
    "author": "Fadoo, Odoo Community Association (OCA)",
    "maintainer": ["saeed-raesi"],
    "website": "https://github.com/OCA/l10n-iran",
    "license": "AGPL-3",
    "category": "l10n/Technical",
    "summary": "Iran Localization",
    "depends": ["hr", "l10n_ir_base", "om_hr_payroll"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_insurance_disk_view.xml",
        "views/hr_job_inherit.xml",
        "views/hr_salary_rule_inherit.xml",
        "views/res_company_inherit.xml",
    ],
    "external_dependencies": {
        "python": ["jdatetime"],
    },
    "installable": True,
}
