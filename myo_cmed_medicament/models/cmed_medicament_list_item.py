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

from openerp import fields, models


class CMEDMedicamentListItem(models.Model):
    _name = 'myo.cmed.medicament.list.item'

    list_id = fields.Many2one('myo.cmed.medicament.list', string='CMED List',
                              help='CMED List', required=False)
    medicament_id = fields.Many2one('myo.cmed.medicament', string='Medicament',
                                    help='CMED Medicament', required=False)
    notes = fields.Text(string='Notes')
    order = fields.Integer(string='Order',
                           default=10)

    pf_0 = fields.Float(string='PF 0%')
    pf_12 = fields.Float(string='PF 12%')
    pf_17 = fields.Float(string='PF 17%')
    pf_18 = fields.Float(string='PF 18%')
    pf_19 = fields.Float(string='PF 19%')
    pf_17_zfm = fields.Float(string='PF 17% ZONA FRANCA DE MANAUS')
    pmc_0 = fields.Float(string='PMC 0%')
    pmc_12 = fields.Float(string='PMC 12%')
    pmc_17 = fields.Float(string='PMC 17%')
    pmc_18 = fields.Float(string='PMC 18%')
    pmc_19 = fields.Float(string='PMC 19%')
    pmc_17_zfm = fields.Float(string='PMC 17% ZONA FRANCA DE MANAUS')
    ultima_alteracao = fields.Char(size=256, string='ULTIMA ALTERACAO')

    active = fields.Boolean('Active',
                            help='The active field allows you to hide the list item without removing it.',
                            default=1)

    _order = 'order'


class CMEDMedicamentList(models.Model):
    _inherit = 'myo.cmed.medicament.list'

    cmed_list_item_ids = fields.One2many('myo.cmed.medicament.list.item',
                                         'list_id',
                                         'CMED List Itens')
