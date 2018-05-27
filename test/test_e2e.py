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

    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

    #Moradillo --- Ejercicio 1b - Verificar que el modal "Editar" tenga datos

    def test_edit_content(self):
        #--Agrego un producto a la db
        p = Product(id=1, name="Silla", price=50)
        db.session.add(p)
        o = Order(id=1)
        db.session.add(o)
        op = OrderProduct(order_id=1, product_id=1, quantity=3, product=p)
        db.session.add(op)
        db.session.commit()
        #--Click en editar en el producto que acabo de agregar
        driver = self.driver
        driver.get(self.baseURL)
        time.sleep(5)
        edit_product_button = driver.find_element_by_xpath('//*[@id="orders"]/table/tbody/tr/td[6]/button[1]')
        edit_product_button.click()
        #--Verificar si el producto anterior aparece en el modal
        time.sleep(2)
        #--Verifico que el nombre sea el correcto
        content_name = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]').text
        assert (content_name == "Silla"), "El modal no tiene datos - Error en nombre"
        #--Verifico que la quantity sea la correcta
        content_quantity = driver.find_element_by_id('quantity').get_attribute('value')
        assert (content_quantity == "3"), "El modal no tiene datos - Error en cantidad"

if __name__ == "__main__":
    unittest.main()

