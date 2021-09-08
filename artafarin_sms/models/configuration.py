from odoo import fields, models, api, _


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sms_line_number = fields.Char('شماره خط ارسال پیامک')
    sms_user_api_key = fields.Char('UserApiKey')
    sms_secret_key = fields.Char('SecretKey')
    twilio_overwrite_odoo_sms = fields.Boolean('بازنویسی سرویس ارسال پیامک')

    @api.model
    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        param_obj = self.env['ir.config_parameter']
        res.update({
            'sms_line_number': param_obj.sudo().get_param('ql_scheduler_reminder.sms_line_number'),
            'sms_user_api_key': param_obj.sudo().get_param('ql_scheduler_reminder.sms_user_api_key'),
            'sms_secret_key': param_obj.sudo().get_param('ql_scheduler_reminder.sms_secret_key'),
            'twilio_overwrite_odoo_sms': param_obj.sudo().get_param('ql_scheduler_reminder.twilio_overrwrite_odoo_sms'),
        })
        return res

    @api.model
    def set_values(self):
        super(ResConfigSetting, self).set_values()
        param_obj = self.env['ir.config_parameter']
        param_obj.sudo().set_param('ql_scheduler_reminder.sms_line_number', self.sms_line_number)
        param_obj.sudo().set_param('ql_scheduler_reminder.sms_user_api_key', self.sms_user_api_key)
        param_obj.sudo().set_param('ql_scheduler_reminder.sms_secret_key', self.sms_secret_key)
        param_obj.sudo().set_param('ql_scheduler_reminder.twilio_overrwrite_odoo_sms', self.twilio_overwrite_odoo_sms)
