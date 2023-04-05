import unittest
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSupplier(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestSupplier, self).setUp(*args, **kwargs)
        self.supplier = self.env['supplier'].create({
            'name': 'Supplier A',
        })
        self.material = self.env['material'].create({
            'code': 'M001',
            'name': 'Material 1',
            'type': 'fabric',
            'buy_price': 200,
            'supplier_id': self.supplier.id,
        })

    def test_supplier_name(self):
        self.assertEqual(self.supplier.name, 'Supplier A')

    def test_material_name(self):
        self.assertEqual(self.material.name, 'Material 1')

    def test_material_type(self):
        self.assertEqual(self.material.type, 'fabric')

    def test_material_buy_price(self):
        self.assertEqual(self.material.buy_price, 200)

        # Test validation when buy price is less than 100
        with self.assertRaises(ValidationError):
            self.material.write({'buy_price': 50})

    def test_material_supplier(self):
        self.assertEqual(self.material.supplier_id, self.supplier)


class TestMaterialController(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestMaterialController, self).setUp(*args, **kwargs)
        self.supplier = self.env['supplier'].create({
            'name': 'Supplier A',
        })

    def test_material_index(self):
        request = self.env['http.request'].sudo().with_user(self.env.user)
        response = self.env['material.controller'].index(request)
        self.assertTrue(response)

    def test_material_create(self):
        request = self.env['http.request'].sudo().with_user(self.env.user)
        response = self.env['material.controller'].create(request)
        self.assertTrue(response)

    def test_material_store(self):
        request = self.env['http.request'].sudo().with_user(self.env.user)
        post = {
            'name': 'Material 1',
            'code': 'M001',
            'type': 'fabric',
            'buy_price': 200,
            'supplier_id': self.supplier.id,
        }
        response = self.env['material.controller'].store(request, **post)
        self.assertTrue(response)

    def test_material_edit(self):
        request = self.env['http.request'].sudo().with_user(self.env.user)
        response = self.env['material.controller'].edit(request, self.supplier.id)
        self.assertTrue(response)

    def test_material_update(self):
        material = self.env['material'].create({
            'code': 'M001',
            'name': 'Material 1',
            'type': 'fabric',
            'buy_price': 200,
            'supplier_id': self.supplier.id,
        })
        request = self.env['http.request'].sudo().with_user(self.env.user)
        post = {
            'name': 'Material 2',
            'buy_price': 300,
        }
        response = self.env['material.controller'].update(request, material.id, **post)
        self.assertTrue(response)

    def test_material_delete(self):
        material = self.env['material'].create({
            'code': 'M001',
            'name': 'Material 1',
            'type': 'fabric',
            'buy_price': 200,
            'supplier_id': self.supplier.id,
        })
        request = self.env['http.request'].sudo().with_user(self.env.user)
        response = self.env['material.controller'].delete(request, material.id)
        self.assertTrue(response)
