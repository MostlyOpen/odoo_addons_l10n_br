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


def validate_cpf(cpf):

    if not cpf.isdigit():
        cpf = re.sub('[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    cpf = map(int, cpf)
    new = cpf[:9]
    while len(new) < 11:
        r = sum([(len(new) + 1 - i) * v for i, v in enumerate(new)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        new.append(f)
    if new == cpf:
        return True
    return False


class PersonManagement(models.Model):
    _inherit = 'myo.person.mng'

    cpf = fields.Char('CPF', size=14)
    rg = fields.Char('RG', size=16)

    @api.one
    @api.constrains('cpf')
    def _check_cpf(self):
        if self.cpf:
            if not validate_cpf(self.cpf):
                raise Warning((u'CPF inválido!'))
        return True

    @api.onchange('cpf')
    def onchange_mask_cpf(self):
        if self.cpf:
            val = re.sub('[^0-9]', '', self.cpf)
            if len(val) == 11:
                cpf = "%s.%s.%s-%s" % (val[0:3], val[3:6], val[6:9], val[9:11])
                self.cpf = cpf
                if not validate_cpf(self.cpf):
                    raise Warning((u'CPF inválido!'))
            else:
                raise Warning((u'Verifique o CPF!'))
