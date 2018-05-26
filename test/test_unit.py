import os
import unittest

from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"

    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Falló el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")

     #Ejercicio 1a - Probar el metodo PUT

    def test_put_method(self):
        #Creo un producto y lo inserto a la db
        
        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()

        #Modifico la quantity del producto con un PUT

        data = {
            'quantity': 5
        }
        resp = self.client.put('order/1/product/1', data=json.dumps(data), content_type='application/json')
        self.assert200(resp, "Fallo el PUT")

    #Ejercicio 1c - Verificar OrderProduct.TotalPrice

    def test_totalPrice(self):
        #Creo dos productos y los inserto a la db
        
        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(p)
        
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 3, product= p)
        db.session.add(orderProduct)

        db.session.commit()

        #Obtengo la orden, obtengo su TotalPrice y lo chequeo

        orden= Order.query.get(1)
        total= sum([
            product.price * product.quantity for product in orden.products
        ])
        self.assertEqual(150, total, "El precio total no se calcula bien")
    
         
#--------------------------- Actividad 3 - Inciso 2.b ------------------------------------
    def test_funcionamiento_get(self):
        # Creo la orden
        o = Order(id=1)
        db.session.add(o)

        # Creo el producto
        p = Product(id=1, name='Cuchillo', price=60)
        db.session.add(p)

        # Creo la relación entre producto y orden
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        db.session.add(orderProduct)
        db.session.commit()

        # Comparo viendo si me devuelve un 200
        resp = self.client.get('order/1/product/1')
        self.assert200(resp,"Fallo el GET")
#---------------------------- Fin actividad 3 - Inciso 2.b -------------------------------

#--------------------------- Actividad 3 - Inciso 2.a ------------------------------------
    def test_cargar_negativo(self):
        # Creo la orden
        o = Order(id=1)
        db.session.add(o)

        # Creo el producto
        p = Product(id=1, name='Cuchillo', price=60)
        db.session.add(p)

        # Creo la relación entre producto y orden
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=-1, product= p)
        db.session.add(orderProduct)
        db.session.commit()

        # Comparo con el comando 'len' para ver si se agregó o no
        op = OrderProduct.query.all()
        self.assertEqual(len(op),0,"Se creo el producto")
#---------------------------- Fin actividad 3 - Inciso 2.a -------------------------------


if __name__ == '__main__':
    unittest.main()

