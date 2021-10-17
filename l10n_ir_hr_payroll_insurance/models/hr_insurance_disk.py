import jdatetime

from odoo import _, api, fields, models
from odoo.tools.misc import get_lang


class HrInsuranceDiskLine(models.Model):
    _name = "l10n.ir.hr.insurance.disk"
    _description = "Insurance Disk"
    _order = "date_insurance desc, id desc"
    # _order = 'id desc'
    # _inherit = ['mail.thread', 'sequence.mixin']
    _inherit = ["mail.thread"]
    _check_company_auto = True

    date_insurance = fields.Datetime(
        string="Insurance Date",
        required=True,
        readonly=True,
        index=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        copy=False,
        default=fields.Datetime.now,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
    )

    start_date = fields.Date(
        string="Start Date", default=lambda self: self._get_start_date(), store=True
    )

    move_id = fields.Many2one(
        "account.move",
        string="Accounting data",
        readonly=True,
        store=True,
        ondelete="set null",
    )

    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )

    mon_pym = fields.Char(
        string="Contract line",
        related="company_id.l10n_ir_insurance_contract_line",
        readonly=True,
    )

    state = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirm"), ("done", "Done")],
        string="Status",
        default="draft",
    )

    name = fields.Char(
        string="Name",
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        compute="_compute_name",
    )  #

    credit_id = fields.Many2one(
        "account.account", string="Creditor account", store=True, ondelete="set null"
    )
    debit_id = fields.Many2one(
        "account.account", string="Debtor account", store=True, ondelete="set null"
    )

    dsk_adrs = fields.Char(
        string="Workshop address",
        related="company_id.l10n_ir_workshop_address",
        size=40,
        readonly=True,
        help="Insurance workshop address limited to 40 characters.",
    )  # required=True

    dsk_bic = fields.Integer(
        string="Total unemployment share", store=True, readonly=True
    )

    dsk_bimh = fields.Integer(
        string="Hard and unprofitable job rates", store=True, readonly=True
    )

    dsk_disc = fields.Char(
        string="List description", size=100, store=True
    )  # required=True

    dsk_farm = fields.Char(
        string="Name of Employer",
        related="company_id.l10n_ir_employer_id.name",
        readonly=True,
    )  # required=True

    dsk_file = fields.Binary(string="Function file", store=True, readonly=True)

    dsk_filename = fields.Char(string="Workshop information", store=True)

    dsk_id = fields.Char(
        string="Workshop code",
        related="company_id.l10n_ir_insurance_workshop_code",
        readonly=True,
    )  # required=True

    dsk_kind = fields.Selection(
        [("1", "Monthly list"), ("2", "Periodic list"), ("3", "Change list")],
        default="1",
    )  # required=True

    dsk_listno = fields.Char(
        string="List number", default="01", size=12, store=True
    )  # required=True

    dsk_mm = fields.Integer(string="Month", compute="_compute_mm", readonly=True)

    dsk_name = fields.Char(
        string="Name of workshop", related="company_id.name", readonly=True
    )

    dsk_prate = fields.Integer(string="Percentage rate", readonly=True)

    dsk_rate = fields.Integer(
        string="Employer insurance share",
        related="company_id.l10n_ir_insurance_rate",
        readonly=True,
    )  # required=True

    dsk_tbime = fields.Integer(string="Total employee insurance share", readonly=True)

    dsk_tdd = fields.Integer(string="Total working days", readonly=True)

    dsk_tkoso = fields.Integer(string="Total employer insurance share", readonly=True)

    dsk_tmah = fields.Integer(string="Total monthly salary", readonly=True)

    dsk_tmash = fields.Integer(string="Total wages and benefits", readonly=True)

    dsk_tmaz = fields.Integer(string="Total monthly benefits", readonly=True)

    dsk_trooz = fields.Integer(string="Total daily wage", readonly=True)

    dsk_ttotl = fields.Integer(
        string="Total Wages and Benefits Includes and Excludes", readonly=True
    )

    dsk_yy = fields.Integer(string="Year", compute="_compute_yy", readonly=True)

    dsw_file = fields.Binary(string="Microfunction file", store=True, readonly=True)

    dsw_filename = fields.Char(string="Insured information", store=True)

    dsw_ids = fields.One2many(
        "l10n.ir.hr.insurance.disk.line",
        "insurance_disk_id",
        string="Disk Work Lines",
        store=True,
    )

    journal_id = fields.Many2one(
        "account.journal", string="journal insurance", store=True, ondelete="set null"
    )

    list_description = fields.Selection(
        selection=[
            (
                "main_included",
                "Main list of included unemployment insurance (current month)",
            ),
            (
                "main_not_included",
                "Main list of not included for unemployment insurance (current month)",
            ),
            (
                "main_included_delayed",
                "Main list of included unemployment insurance (monthly delayed)",
            ),
            (
                "complementary_non_commission_included",
                "Complementary list non-commission unemployment insurance",
            ),
            (
                "complementary_non_commission_not_included	",
                "Complementary list non-commission not included unemployment insurance",
            ),
            ("main_commission", "The main list of current commissions"),
            ("main_commission_delayed", "The main list of delayed commissions"),
            ("complementary_commission", "Complementary list of commissions"),
            ("devotee_25", "List of martyrs with 25% disability"),
            ("devotee_50", "List of martyrs with 50% disability"),
            ("custom", "Custom-made"),
        ],
        store=True,
        default="main_included",
    )

    def action_confirm(self):
        return self.write({"state": "confirm"})

    def compute_insurance(self):
        return True

    def action_done(self):
        return self.write({"state": "done"})

    def set_draft(self):
        return self.write({"state": "draft"})

    def _get_start_date(self):

        todayDate = fields.Datetime.now()
        todayDate = jdatetime.date(
            todayDate.year,
            todayDate.month,
            todayDate.day,
            locale=get_lang(self.env).code,
        )
        todayDate = jdatetime.date.fromgregorian(date=todayDate)
        todayDate = todayDate.replace(day=1)
        todayDate = todayDate.togregorian()
        return todayDate

    @api.depends("start_date")
    def _compute_mm(self):
        if self.start_date:
            todayDate = jdatetime.date.fromgregorian(
                date=self.start_date, locale=get_lang(self.env).code
            )
            self.dsk_mm = todayDate.month
        else:
            self.dsk_mm = 0

    @api.depends("start_date")
    def _compute_name(self):
        if self.start_date:
            todayDate = jdatetime.date.fromgregorian(
                date=self.start_date, locale=get_lang(self.env).code
            )
            self.name = _("Insurance List for %s") % (todayDate.strftime("%b %Y"))
        else:
            self.name = _("New")

    @api.depends("start_date")
    def _compute_yy(self):
        if self.start_date:
            todayDate = jdatetime.date.fromgregorian(
                date=self.start_date, locale=get_lang(self.env).code
            )
            self.dsk_yy = todayDate.strftime("%y")
        else:
            self.dsk_yy = 0
