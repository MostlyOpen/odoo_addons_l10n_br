# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import re

from openerp import api, fields, models
from openerp.exceptions import Warning


class Address(models.Model):
    _inherit = 'myo.address'

    l10n_br_city_id = fields.Many2one(
        'l10n_br_base.city', u'City',
        domain="[('state_id','=',state_id)]")
    district = fields.Char('District', size=32)
    number = fields.Char(u'Number', size=10)

    @api.model
    def _display_address(self, address, without_company=False):

        if address.country_id and address.country_id.code != 'BR':
            # this ensure other localizations could do what they want
            return super(Address, self)._display_address(
                address,
                without_company=False)
        else:
            address_format = (
                address.country_id and
                address.country_id.address_format or
                "%(street)s\n%(street2)s\n%(city)s %(state_code)s"
                "%(zip)s\n%(country_name)s")
            args = {
                'state_code': address.state_id and address.state_id.code or '',
                'state_name': address.state_id and address.state_id.name or '',
                'country_code': address.country_id and
                address.country_id.code or '',
                'country_name': address.country_id and
                address.country_id.name or '',
                # 'company_name': address.parent_id and
                # address.parent_id.name or '',
                'l10n_br_city_name': address.l10n_br_city_id and
                address.l10n_br_city_id.name or '',
            }
            address_field = ['title', 'street', 'street2', 'zip', 'city',
                             'number', 'district']
            for field in address_field:
                args[field] = getattr(address, field) or ''
            if without_company:
                args['company_name'] = ''
            # elif address.parent_id:
            #     address_format = '%(company_name)s\n' + address_format
            return address_format % args

    @api.onchange('l10n_br_city_id')
    def onchange_l10n_br_city_id(self):
        """ Ao alterar o campo l10n_br_city_id que é um campo relacional
        com o l10n_br_base.city que são os municípios do IBGE, copia o nome
        do município para o campo city que é o campo nativo do módulo base
        para manter a compatibilidade entre os demais módulos que usam o
        campo city.

        param int l10n_br_city_id: id do l10n_br_city_id digitado.

        return: dicionário com o nome e id do município.
        """
        if self.l10n_br_city_id:
            self.city = self.l10n_br_city_id.name
            self.l10n_br_city_id = self.l10n_br_city_id

    @api.onchange('zip')
    def onchange_mask_zip(self):
        if self.zip:
            val = re.sub('[^0-9]', '', self.zip)
            if len(val) == 8:
                zip = "%s-%s" % (val[0:5], val[5:8])
                self.zip = zip

    @api.model
    def _address_fields(self):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set.
        Extenção para os novos campos do endereço """
        address_fields = super(Address, self)._address_fields()
        return list(address_fields + ['l10n_br_city_id', 'number', 'district'])


class Address_2(models.Model):
    _inherit = 'myo.address'

    @api.multi
    def zip_search(self):
        self.ensure_one()
        obj_zip = self.env['l10n_br.zip']

        zip_ids = obj_zip.zip_search_multi(
            country_id=self.country_id.id,
            state_id=self.state_id.id,
            l10n_br_city_id=self.l10n_br_city_id.id,
            district=self.district,
            street=self.street,
            zip_code=self.zip,
        )

        if len(zip_ids) == 1:
            result = obj_zip.set_result(zip_ids[0])
            self.write(result)
            return True
        else:
            if len(zip_ids) > 1:
                obj_zip_result = self.env['l10n_br.zip.result']
                zip_ids = obj_zip_result.map_to_zip_result(
                    zip_ids, self._name, self.id)

                return obj_zip.create_wizard(
                    self._name,
                    self.id,
                    country_id=self.country_id.id,
                    state_id=self.state_id.id,
                    l10n_br_city_id=self.l10n_br_city_id.id,
                    district=self.district,
                    street=self.street,
                    zip_code=self.zip,
                    zip_ids=[zip.id for zip in zip_ids]
                )
            else:
                raise Warning(('Warning. No records found!'))


class Address_3(models.Model):
    _inherit = 'myo.address'

    @api.depends('street', 'number', 'street2')
    def _get_suggested_name(self):
        if self.street:
            self.suggested_name = self.street
            if self.number:
                self.suggested_name = self.suggested_name + ', ' + self.number
                if self.street2:
                    self.suggested_name = self.suggested_name + ' - ' + self.street2
            else:
                if self.street2:
                    self.suggested_name = self.suggested_name + ' - ' + self.street2
        else:
            if not self.suggested_name:
                if self.code:
                    self.suggested_name = self.code
