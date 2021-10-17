from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "hr.job"

    l10n_ir_hard_harmful_job = fields.Boolean(
        string="Is the job hard and harmful?",
        store=True,
        help="	Declare if this job is known hard or harmful by insurance company.",
    )
    l10n_ir_hard_harmful_rate = fields.Float(
        string="Rate of harness of the job",
        store=True,
        help="Rate of harness of the job defined by insurance company.",
    )
    l10n_ir_insurance_code = fields.Char(
        string="Insurance code",
        store=True,
        help="A code for the job from list given by insurance company.",
    )
