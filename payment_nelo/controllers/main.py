# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import requests
import werkzeug

from odoo import http, _
from odoo.http import request

from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class NeloController(http.Controller):
    _confirm_url = '/payment/nelo/confirm'
    _cancel_url = '/payment/nelo/cancel'

    def _nelo_auth_payment(self, **params):
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'nelo')])

        reference = params['reference']
        orderUuid = params['orderUuid']

        headers = {
            'Authorization': 'Bearer %s' % (acquirer.nelo_merchant_secret),
            'Content-Type': 'application/json',
            'x-device-platform': 'web',
            'x-app-version-code': '1'
        }
        try:
            url = '%s/payments/%s' % (acquirer._get_nelo_urls()['rest_url'], orderUuid)
            getPaymentResponse = requests.request("GET", url, headers=headers)
            _logger.info('Nelo - url requested %s' % url)
            _logger.info('Nelo - response: %s' % getPaymentResponse)

            getPaymentResponse.raise_for_status()
            getPaymentJsonResponse = getPaymentResponse.json()

            if getPaymentJsonResponse['reference'] != reference:
                raise ValidationError(_('Nelo: received data with incorrect reference (%s)') % (reference))

            url = '%s/payments/%s/capture' % (acquirer._get_nelo_urls()['rest_url'], orderUuid)
            captureResponse = requests.request("POST", url, headers=headers)
            _logger.info('Nelo - url requested %s' % url)
            _logger.info('Nelo - response: %s' % captureResponse)
            captureResponse.raise_for_status()
        except:
            request.env['payment.transaction'].sudo().search(
                [('reference', '=', reference)]
            )._set_transaction_error(_('Request rejected by Nelo.'))
            return False
        
        data = {
            'reference': reference
        }
        return request.env['payment.transaction'].sudo().form_feedback(data, 'nelo')

    @http.route('/payment/nelo/confirm', type='http', auth="public", methods=['GET'], csrf=False)
    def nelo_return(self, **query_params):
        if query_params and query_params['orderUuid'] and query_params['reference']:
            self._nelo_auth_payment(**query_params)
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/payment/nelo/cancel', type='http', auth='public', methods=['GET'], csrf=False)
    def nelo_notify(self, **query_params):
        return werkzeug.utils.redirect('/shop/checkout')
