from odoo import fields, models


class HrInsuranceDiskLine(models.Model):
    _name = "l10n.ir.hr.insurance.disk.line"
    _description = "Insurance Disk Line"

    insurance_disk_id = fields.Many2one(
        "l10n.ir.hr.insurance.disk", string="Insurance disk", ondelete="set null"
    )
    company_id = fields.Many2one(
        "res.company",
        related="insurance_disk_id.company_id",
        string="Company",
        readonly=True,
        ondelete="set null",
    )

    payslip_id = fields.Many2one(
        "hr.payslip", string="Payslip", store=True, ondelete="set null"
    )

    employee_id = fields.Many2one(
        "hr.employee",
        related="payslip_id.employee_id",
        string="Employee",
        readonly=True,
        ondelete="set null",
    )

    job_id = fields.Many2one(
        "hr.job",
        related="employee_id.job_id",
        string="Job",
        readonly=True,
        ondelete="set null",
    )  # required=True

    birthday = fields.Date(string="Birthday", related="employee_id.birthday")
    recruitment_date = fields.Date(
        string="Date of the first contract", related="employee_id.first_contract_date"
    )

    dsw_bdate = fields.Char(string="Date of birth", size=8, readonly=True)

    dsw_bime = fields.Integer(
        string="Employer insurance share", store=True, readonly=True
    )

    dsw_dd = fields.Integer(string="Working days", store=True, readonly=True)

    dsw_dname = fields.Char(
        string="Father name", related="employee_id.l10n_ir_father_name", size=60
    )  # required=True

    dsw_edate = fields.Char(string="End date", size=8, readonly=True)

    dsw_fname = fields.Char(
        string="First name", size=60, readonly=True
    )  # required=True

    dsw_id = fields.Char(
        string="Workshop code",
        related="insurance_disk_id.dsk_id",
        size=10,
        readonly=True,
    )

    dsw_id1 = fields.Char(
        string="insurance number",
        related="employee_id.l10n_ir_insurance_id",
        size=10,
        readonly=True,
        help="The insurance ID that will be on the insurance list.",
    )  # required=True

    dsw_idate = fields.Char(string="creation date", size=8, readonly=True)

    dsw_idno = fields.Char(
        string="identification id", related="employee_id.identification_id", size=15
    )  # required=True

    dsw_idplc = fields.Char(
        string="place_of_birth", related="employee_id.place_of_birth", size=30
    )

    dsw_job = fields.Char(
        string="Job Code",
        related="job_id.l10n_ir_insurance_code",
        readonly=True,
        help="A code for the job from list given by insurance company.",
    )  # required=True

    dsw_listno = fields.Char(
        string="List number",
        related="insurance_disk_id.dsk_listno",
        size=12,
        readonly=True,
    )

    dsw_lname = fields.Char(
        string="Last Name", related="employee_id.l10n_ir_last_name", size=60
    )  # required=True

    dsw_mah = fields.Integer(string="Monthly wage", store=True, readonly=True)

    dsw_mash = fields.Integer(
        string="Wages and benefits included", store=True, readonly=True
    )

    dsw_maz = fields.Integer(string="Monthly benefits", store=True, readonly=True)

    dsw_mm = fields.Integer(
        string="Month", related="insurance_disk_id.dsk_mm", readonly=True
    )

    dsw_nat = fields.Char(
        string="Nationality",
        related="employee_id.country_id.name",
        translate=True,
        size=10,
        readonly=True,
    )  # required=True

    dsw_ocp = fields.Char(
        string="job description",
        related="job_id.name",
        translate=True,
        size=50,
        readonly=True,
    )  # required=True

    dsw_prate = fields.Integer(string="Percentage rate", store=True, readonly=True)

    dsw_rooz = fields.Integer(string="Daily wage", store=True, readonly=True)

    dsw_sdate = fields.Char(string="start date", size=8, readonly=True)

    dsw_sex = fields.Char(string="Gender", size=3, readonly=True)

    dsw_totl = fields.Integer(string="Wages and benefits", store=True, readonly=True)

    dsw_yy = fields.Integer(
        string="Year", related="insurance_disk_id.dsk_yy", readonly=True
    )

    end_date = fields.Date(
        string="End date of the contract",
        related="employee_id.l10n_ir_contract_end_date",
    )

    gender = fields.Selection(related="employee_id.gender")

    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], default="male"
    )  # required=True

    # id = fields.Integer(string="Id", store=True, readonly=True)

    per_natcod = fields.Char(
        string="National Code", related="employee_id.l10n_ir_national_id", size=10
    )
