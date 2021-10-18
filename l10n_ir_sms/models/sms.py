import json
import logging
import threading

import requests

from odoo import fields, models

# sms api
urlGetToken = "https://RestfulSms.com/api/Token"
urlSendSms = "https://RestfulSms.com/api/MessageSend"
urlUltraFastSend = "https://RestfulSms.com/api/UltraFastSend"
header_getToken = {"Content-Type": "application/json"}

logger = logging.getLogger(__name__)


class SMS(models.Model):
    _inherit = "sms.sms"

    error_message = fields.Text("Error Message", copy=False, readonly=1)

    def send(self, delete_all=False, auto_commit=False, raise_exception=False):
        """Main API method to send SMS.

        :param delete_all: delete all SMS (sent or not); otherwise delete only
          sent SMS;
        :param auto_commit: commit after each batch of SMS;
        :param raise_exception: raise if there is an issue contacting IAP;
        """
        is_message_overwrite = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ql_scheduler_reminder.twilio_overrwrite_odoo_sms")
        )
        for batch_ids in self._split_batch():
            if not is_message_overwrite:
                self.browse(batch_ids)._send(
                    delete_all=delete_all, raise_exception=raise_exception
                )
            else:
                self.browse(batch_ids).sms_body()
            # auto-commit if asked except in testing mode

            if auto_commit is True and not getattr(
                threading.currentThread(), "testing", False
            ):
                pass
                # self._cr.commit()

    def sms_body(self, delete_all=False, raise_exception=False):
        # TODO: fix send sms option
        param_obj = self.env["ir.config_parameter"]
        # get sms data
        sms_line_number = param_obj.sudo().get_param(
            "ql_scheduler_reminder.sms_line_number"
        )
        sms_user_api_key = param_obj.sudo().get_param(
            "ql_scheduler_reminder.sms_user_api_key"
        )
        sms_secret_key = param_obj.sudo().get_param(
            "ql_scheduler_reminder.sms_secret_key"
        )

        body_getToken = {
            "UserApiKey": "{}".format(sms_user_api_key),
            "SecretKey": "{}".format(sms_secret_key),
        }

        response = requests.post(
            urlGetToken, json=body_getToken, headers=header_getToken
        )
        json_data = json.loads(response.text)

        if json_data["IsSuccessful"]:
            token = json_data["TokenKey"]
        else:
            logger.error("Get Token Error !!")

        for rec_id in self:
            phone = rec_id.number
            try:
                response = self.send_sms(token, phone, rec_id.body, sms_line_number)
                if response["IsSuccessful"]:
                    state = "sent"
                    error_message = "sent sms success"
                else:
                    state = "error"
                    error_message = None
            except Exception as e:
                state = "error"
                error_message = e.msg or e.__str__()
            rec_id.write({"error_message": error_message, "state": state})

    def send_sms(self, token, phone_number, message, line_number):
        header_sendSms = {
            "Content-Type": "application/json",
            "x-sms-ir-secure-token": "{}".format(token),
        }

        Body = {
            "Messages": ["{}".format(message)],
            "MobileNumbers": ["{}".format(phone_number)],
            "LineNumber": "{}".format(line_number),
            "SendDateTime": "",
            "CanContinueInCaseOfError": "false",
        }

        response = requests.post(urlSendSms, json=Body, headers=header_sendSms)
        json_data = json.loads(response.text)
        return json_data
