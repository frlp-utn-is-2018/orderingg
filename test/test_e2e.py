import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

from werkzeug.serving import make_server

class Ordering(unittest.TestCase):
    # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.t = threading.Thread(target=self.app.run)
        self.t.start()

        time.sleep(1)

        self.driver = webdriver.Chrome()

    def test_title(self):
        driver = self.driver
        driver.get(self.baseURL)
        add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        add_product_button.click()
        modal = driver.find_element_by_id('modal')
        assert modal.is_displayed(), "El modal no esta visible"

    #--------Ejercicio 4-3 | Test de integración | verificar que se haya solucionado el bug no mostraba
    #--------el nombre del producto en la tabla
    def test_show_name_in_table(self):
        #Agrego Product
        p = Product(id=1, name="Guitarra", price=1000)
        db.session.add(p)
        
        #Agrego Order
        o = Order(id=1)
        db.session.add(o)
        
        #Agrego OrderProduct
        op = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        db.session.add(op)
        
        db.session.commit()
        
        driver = self.driver
        driver.get(self.baseURL)
        
        #Obtengo el path de la <td> donde va el nombre del primer producto agregado.
        producto_agregado = driver.find_element_by_xpath('//*[@id="orders"]/table/tbody/tr[1]/td[2]').text
        
        #Se supone que el nombre del producto en esa columna tiene que coincidir con el que agregué,
        #que es "Guitarra". De no serlo fallará el test, por lo tanto no se habría solucionado el bug.
        #Si no muestra el producto aparecería "" != "Guitarra" 
        assert producto_agregado == 'Guitarra', 'No muestra el producto en la tabla'

    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()

