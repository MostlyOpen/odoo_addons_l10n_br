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

from openerp import api, fields, models


class ABCFarmaMedicamentListItem(models.Model):
    _name = 'myo.abcfarma.medicament.list.item'

    list_id = fields.Many2one('myo.abcfarma.medicament.list', string='ABCFarma List',
                              help='ABCFarma List', required=False)
    medicament_id = fields.Many2one('myo.abcfarma.medicament', string='Medicament',
                                    help='ABCFarma Medicament', required=False)
    notes = fields.Text(string='Notes')
    order = fields.Integer(string='Order',
                           default=10)

    name = fields.Char('Product Name', related='medicament_id.name')
    ean13 = fields.Char('EAN13 Barcode', related='medicament_id.ean13')
    code = fields.Char('Medicament Code', related='medicament_id.code')
    medicament_name = fields.Char('Medicament Name', related='medicament_id.medicament_name')
    concentration = fields.Char('Concentration', related='medicament_id.concentration')
    presentation = fields.Char('Presentation', related='medicament_id.presentation')
    pres_form = fields.Many2one('myo.medicament.form', string='Presentation Form',
                                related='medicament_id.pres_form')
    pres_quantity = fields.Float('Presentation Quantity', related='medicament_id.pres_quantity')
    pres_quantity_unit = fields.Many2one('myo.medicament.uom', string='Presentation Quantity Unit',
                                         related='medicament_id.pres_quantity_unit')
    notes = fields.Text('Notes', related='medicament_id.notes')
    date_inclusion = fields.Datetime("Inclusion Date", related='medicament_id.date_inclusion')
    is_product = fields.Boolean('Is a Product', related='medicament_id.is_product')
    is_fraction = fields.Boolean('Is a Fraction', related='medicament_id.is_fraction')
    for_hospital_use = fields.Boolean('For Hospital Use', related='medicament_id.for_hospital_use')

    active_component = fields.Many2one('myo.medicament.active_component', string='Active Component',
                                       related='medicament_id.active_component')
    manufacturer = fields.Many2one('myo.medicament.manufacturer', string='Manufacturer',
                                   related='medicament_id.manufacturer')

    med_abc = fields.Char('MED_ABC', related='medicament_id.med_abc')
    med_ctr = fields.Char('MED_CTR', related='medicament_id.med_ctr')
    med_lab = fields.Char('MED_LAB', related='medicament_id.med_lab')
    lab_nom = fields.Char('LAB_NOM', related='medicament_id.lab_nom')
    med_des = fields.Char('MED_DES', related='medicament_id.med_des')
    med_apr = fields.Char('MED_APR', related='medicament_id.med_apr')
    med_barra = fields.Char('MED_BARRA', related='medicament_id.med_barra')
    med_gene = fields.Char('MED_GENE', related='medicament_id.med_gene')
    med_negpos = fields.Char('MED_NEGPOS', related='medicament_id.med_negpos')
    med_princi = fields.Char('MED_PRINCI', related='medicament_id.med_princi')

    med_uni = fields.Float(string='MED_UNI')
    med_ipi = fields.Float(string='MED_IPI')
    med_dtvig = fields.Date('MED_DTVIG')
    exp_13 = fields.Boolean('EXP_13')
    med_regims = fields.Char(string='MED_REGIMS')
    med_varpre = fields.Char(string='MED_VARPRE')

    med_pco18 = fields.Float(string='MED_PCO18')
    med_pla18 = fields.Float(string='MED_PLA18')
    med_fra18 = fields.Float(string='MED_FRA18')
    med_pco17 = fields.Float(string='MED_PCO17')
    med_pla17 = fields.Float(string='MED_PLA17')
    med_fra17 = fields.Float(string='MED_FRA17')
    med_pco12 = fields.Float(string='MED_PCO12')
    med_pla12 = fields.Float(string='MED_PLA12')
    med_fra12 = fields.Float(string='MED_FRA12')
    med_pco19 = fields.Float(string='MED_PCO19')
    med_pla19 = fields.Float(string='MED_PLA19')
    med_fra19 = fields.Float(string='MED_FRA19')
    med_pcozfm = fields.Float(string='MED_PCOZFM')
    med_plazfm = fields.Float(string='MED_PLAZFM')
    med_frazfm = fields.Float(string='MED_FRAZFM')
    med_pco0 = fields.Float(string='MED_PCO0')
    med_pla0 = fields.Float(string='MED_PLA0')
    med_fra0 = fields.Float(string='MED_FRA0')
    active = fields.Boolean('Active',
                            help='The active field allows you to hide the list item without removing it.',
                            default=1)

    _order = 'list_id, order'


class ABCFarmaMedicamentList(models.Model):
    _inherit = 'myo.abcfarma.medicament.list'

    abcfarma_list_item_ids = fields.One2many('myo.abcfarma.medicament.list.item',
                                             'list_id',
                                             'ABCFarma List Itens')
    count_items = fields.Integer(
        'Number of Items',
        compute='_compute_count_items'
    )

    @api.depends('abcfarma_list_item_ids')
    def _compute_count_items(self):
        for r in self:
            r.count_items = len(r.abcfarma_list_item_ids)
