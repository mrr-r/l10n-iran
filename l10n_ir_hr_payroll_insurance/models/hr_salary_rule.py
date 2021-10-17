from odoo import fields, models


class HrSalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    l10n_ir_insured = fields.Boolean(string="insured", store=True)
