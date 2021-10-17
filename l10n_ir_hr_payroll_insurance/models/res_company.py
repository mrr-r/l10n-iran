from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ir_employer_id = fields.Many2one(
        "res.partner", string="Employer", store=True, ondelete="set null"
    )
    l10n_ir_insurance_contract_line = fields.Char(
        string="Contract line", help="Insurance contract line"
    )
    l10n_ir_insurance_rate = sequence = fields.Integer(
        string="Employer insurance share", default=23
    )
    l10n_ir_insurance_workshop_code = fields.Char(
        string="Workshop code", help="Insurance workshop code", store=True
    )
    l10n_ir_workshop_address = fields.Char(
        string="Workshop address",
        size=40,
        help="Insurance workshop address limited to 40 characters.",
    )
