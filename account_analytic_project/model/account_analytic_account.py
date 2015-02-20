# -*- encoding: utf-8 -*-
"""Extend account.analytic.account."""
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV <http://therp.nl>
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields
from openerp.tools.translate import _


class AccountAnalyticAccount(orm.Model):
    """Extend account.analytic.account."""
    _inherit = 'account.analytic.account'

    def view_projects_for_account(self, cr, uid, ids, context=None):
        """View list or form for project(s) related to analytic account."""
        assert len(ids) == 1, (_(
            'This method is only valid for a single analytic account'))
        project_model = self.pool['project.project']
        project_ids = project_model.search(
            cr, uid, [('analytic_account_id', '=', ids[0])],
            context=context
        )
        assert project_ids, (_(
            'This method is only valid for an analytic account having projects'
        ))
        # Show form by default:
        view_id = 'edit_project'
        view_mode = 'form'
        action_name = _('Project')
        domain = False
        res_id = project_ids[0]
        if len(project_ids) > 1:
            # In the future there might be more projects per analytic account,
            # in that case we will show a tree:
            view_id = False  # Otherwise impossible to go from tree to form
            view_mode = 'tree,form'
            action_name = _('Projects')
            domain = [('id', 'in', project_ids)]
            res_id = False
        # Find view id to show in action
        if view_id:
            data_model = self.pool['ir.model.data']
            view_ref = data_model.get_object_reference(
                cr, uid, 'project', view_id)
            view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'name': action_name,
            'view_mode': view_mode,
            'view_type': 'form',
            'view_id': view_id,
            'res_model': 'project.project',
            'nodestroy': True,
            'res_id': res_id,
            'target': 'current',
            'domain': domain,
            'context': context,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
