#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.finished_goods_stock.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('finished_goods_stock.customer_report')
        active_wizard = self.env['finished.goods'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['finished.goods'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['finished.goods'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to

        category = self.env['product.category'].search([('finish_good','=',True)])



        sizes = []
        def get_size(attr):
            del sizes[:]
            prod_temp = self.env['product.template'].search([('categ_id.finish_good','=',True),('categ_id','=',attr)])
            for x in prod_temp:
                for y in x.attribute_line_ids:
                    if y.attribute_id.name == 'size':
                        if y.attribute_id.value_ids.name not in sizes:
                            sizes.append(y.attribute_id.value_ids.name)



        def get_value(attr,num):
            value = 0
            products = []
            prod_temp = self.env['product.template'].search([('categ_id.finish_good','=',True),('categ_id','=',attr)])
            for x in prod_temp:
                for y in x.attribute_line_ids:
                    if y.attribute_id.name == 'size':
                        if y.attribute_id.value_ids.name == num:
                            products.append(x)

            for z in products:
                daily = self.env['daily.production.tree'].search([('product.categ_id.finish_good','=',True),('product.categ_id','=',attr),('product.product_tmpl_id','=',z.id)])
                for y in daily:
                    value = value + y.qty_lit

            return value




        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'daily.production',
            'category':category,
            'sizes':sizes,
            'get_size':get_size,
            'get_value':get_value,

            }

        return report_obj.render('finished_goods_stock.customer_report', docargs)