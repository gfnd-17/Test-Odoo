from odoo import http
from odoo.http import request

class MaterialController(http.Controller):

    @http.route('/material', auth='user', website=True)
    def index(self, **kw):
        materials = request.env['material'].sudo().search([])
        return http.request.render('material.material_list', {'materials': materials})

    @http.route('/material/create', auth='user', website=True)
    def create(self, **kw):
        suppliers = request.env['supplier'].sudo().search([])
        return http.request.render('material.material_form', {'suppliers': suppliers})

    @http.route('/material/store', auth='user', type='http', website=True, method=['POST'])
    def store(self, **kw):
        material = request.env['material'].sudo().create(kw)
        return request.redirect('/material')

    @http.route('/material/<int:id>/edit', auth='user', website=True)
    def edit(self, id, **kw):
        material = request.env['material'].sudo().search([('id', '=', id)])
        suppliers = request.env['supplier'].sudo().search([])
        return http.request.render('material.material_form', {'material': material, 'suppliers': suppliers})

    @http.route('/material/<int:id>/update', auth='user', type='http', website=True, method=['POST'])
    def update(self, id, **kw):
        material = request.env['material'].sudo().search([('id', '=', id)])
        material.write(kw)
        return request.redirect('/material')

    @http.route('/material/<int:id>/delete', auth='user', website=True)
    def delete(self, id, **kw):
        material = request.env['material'].sudo().search([('id', '=', id)])
        material.unlink()
        return request.redirect('/material')
    
    @http.route('/material', type='http', auth='user', website=True)
    def material_list(self):
        materials = request.env['material'].search([])
        return http.request.render('material.material_list', {
            'materials': materials,
        })
    
    @http.route('/material/<int:id>/edit', type='http', auth='user', website=True)
    def material_edit(self, id):
        material = request.env['material'].sudo().search([('id', '=', id)])
        suppliers = request.env['supplier'].search([])
        return http.request.render('material.material_form', {
            'material': material,
            'suppliers': suppliers,
        })
    
    @http.route('/material/<int:id>/delete', type='http', auth='user', website=True)
    def material_delete(self, id):
        material = request.env['material'].sudo().search([('id', '=', id)])
        material.sudo().unlink()
        return http.request.redirect('/material')
    
    @http.route('/material/create', type='http', auth='user', website=True)
    def material_create(self):
        suppliers = request.env['supplier'].search([])
        return http.request.render('material.material_form', {
            'suppliers': suppliers,
        })
    
    @http.route('/material/store', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def material_store(self, **post):
        if post.get('id'):
            material = request.env['material'].sudo().search([('id', '=', post.get('id'))])
            material.sudo().write(post)
        else:
            request.env['material'].sudo().create(post)
        return http.request.redirect('/material')
