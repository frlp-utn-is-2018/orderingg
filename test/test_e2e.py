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

    def test_eliminación_fila_correspondiente(self):
        #Creo los productos
        prod = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(prod)
        prod2 = Product(id= 2, name= 'Calabaza', price= 30)
        db.session.add(prod)

        #Creo una orden
        order = Order(id= 1)
        db.session.add(order)

        #Añado los productos a la orden
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= prod)
        db.session.add(orderProduct)
        orderProduct = OrderProduct(order_id= 1, product_id= 2, quantity= 1, product= prod2)
        db.session.add(orderProduct)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)

        time.sleep(1)

        delete_product_button = driver.find_element_by_xpath('//*[@id="orders"]/table/tbody/tr/td[6]/button[2]')
        delete_product_button.click()
        
        time.sleep(1)

        op = OrderProduct.query.all()

        # Verifica que se haya borrado el producto de la lista de productos
        self.assertEqual(len(op), 1, "No se borró el producto")

        #Verifica que se haya borrado el producto correcto
        self.assertNotEqual(op[0].product, prod, "No se borró el producto correcto")

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


#---------------------------------------- Actividad 3 - Inciso 2.c ------------------------------------------------
	def test_negativa_quantity(self):
	    # Creo un producto para que aparezca en el scroll
	    p = Product(id=1, name="Vaso", price=50)
	    db.session.add(p)
	    o = Order(id=1)
	    db.session.add(o)
	    db.session.commit()
	    driver = self.driver
	    driver.get(self.baseURL)
	    # Clickeo en el botón 'Agregar'
	    add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
	    add_product_button.click()
	    # Clickeo en la selección de producto
	    select_product = driver.find_element_by_id('select-prod')
	    select_product.click()
	    # Clickeo en la opción 2 de la lista
	    opcion_seleccionada = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]')
	    opcion_seleccionada.click()
	    # Le ingreso una cantidad negativa
	    cantidad_product = driver.find_element_by_id('quantity')
	    cant = cantidad_product.send_keys("-3")
	    # Clickeo en el botón de guardado
	    save_button = driver.find_element_by_id('save-button')
	    save_button.click()
	    #--Verificar si el producto anterior aparece en el modal
	    time.sleep(2)
	    # Verifica que en la lista de productos no haya
	    p = Product.query.all()
	    self.assertEqual(len(p), 0, "Hay productos cargados")
#---------------------------------------- Fin actividad 3 - Inciso 2.c --------------------------------------------

if __name__ == "__main__":
    unittest.main()

