# -*- coding: utf-8 -*-
# from odoo import http


# class Autorisation(http.Controller):
#     @http.route('/autorisation/autorisation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/autorisation/autorisation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('autorisation.listing', {
#             'root': '/autorisation/autorisation',
#             'objects': http.request.env['autorisation.autorisation'].search([]),
#         })

#     @http.route('/autorisation/autorisation/objects/<model("autorisation.autorisation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('autorisation.object', {
#             'object': obj
#         })
