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


class CMEDMedicament(models.Model):
    _name = 'myo.cmed.medicament'
    _inherit = 'myo.medicament.model'

    principio_ativo = fields.Char(string='Principio Ativo')
    cnpj = fields.Char(string='CNPJ')
    latoratorio = fields.Char(string='Laboratorio')
    codigo_ggrem = fields.Char(string='Codigo GGREM')
    registro = fields.Char(string='Registro')
    ean = fields.Char(string='EAN')
    produto = fields.Char(string='Produto')
    apresentacao = fields.Char(string='Apresentacao')
    classe_terapeutica = fields.Char(string='Classe Terapeutica')

    restr_hospitalar = fields.Char(string='RESTRICAO_HOSPITALAR')
    cap = fields.Char(string='CAP')
    confaz_87 = fields.Char(string='CONFAZ_87')
    analise_recursal = fields.Char(string='ANALISE_RECURSAL')
