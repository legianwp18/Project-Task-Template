#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TaskTemplateMaster(models.Model):
    _name = "project.task.template.master"

    name = fields.Char(
        string='Name'
    )

    task_line_ids = fields.One2many(
        comodel_name='project.task.template', 
        inverse_name='master_id', 
        string='Tasks Line'
    )

class TaskTemplate(models.Model):
    _name = "project.task.template"
    _description = "Task Template"
    _order = "sequence,id"
    _inherit = [
        'mail.thread.cc', 
        'mail.activity.mixin', 
        'rating.mixin'
    ]

    PRIORITY_SELECTION = [
        ('0', 'Low'),
        ('1', 'High'),
    ]

    name = fields.Char(
        string='Title', 
        tracking=True, 
        required=True, 
        index='trigram'
    )

    master_id = fields.Many2one(
        comodel_name='project.task.template.master', 
        string='Header'
    )
    
    description = fields.Html(
        string='Description'
    )

    parent_id = fields.Many2one(
        comodel_name ='project.task.template', 
        string='Parent Task',  
        ondelete='cascade'
    )

    predecessors_id = fields.Many2one(
        comodel_name = 'project.task.template', 
        string='Predecessors', 
        index=True, 
        ondelete='cascade'
    )

    successors_id = fields.Many2one(
        comodel_name = 'project.task.template', 
        string='Successors', 
        index=True, 
        ondelete='cascade'
    )

    child_ids = fields.One2many(
        comodel_name = 'project.task.template', 
        inverse_name='parent_id', 
        string="Sub-tasks"
    )

    priority = fields.Selection(
        selection = PRIORITY_SELECTION, 
        default='0', 
        index=True, 
        string="Priority", 
        tracking=True
    )

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    user_ids = fields.Many2many(
        comodel_name = 'res.users', 
        relation='project_task_template_user_rel', 
        column1='task_id', 
        column2='user_id', 
        string='Assignees', 
        context={'active_test': False}, 
        tracking=True
    )

    work_days = fields.Integer(
        string = 'Work Days',
        default=1
    )

    work_days_line = fields.Integer(
        string = 'Work Days Line',
        compute='get_work_days',
        store=True,
    )

    @api.onchange('predecessors_id')
    def get_predecessors_id(self):
        if self.predecessors_id:
            self.sequence = self.predecessors_id.sequence + 1
            self.predecessors_id.successors_id = self._origin.id
    
    @api.onchange('successors_id')
    def get_successors_id(self):
        if self.successors_id:
            self.sequence = self.successors_id.sequence - 1
 

    @api.depends('work_days')
    def get_work_days(self):
        for rec in self:
            filter_child = [('parent_id','=',rec.parent_id.id)]
            work_days_obj = self.env['project.task.template']
            work_days_parent = work_days_obj.browse(rec.parent_id.id)
            sum_work_days_child = sum(work_days_obj.search(filter_child).mapped('work_days'))
            work_days_parent.write({'work_days': sum_work_days_child})
            rec.work_days_line = sum_work_days_child
