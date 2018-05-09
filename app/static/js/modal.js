const Modal = (function () {

    /**
     * Abre el modal
     **/
    function open($modal, product) {
        const editTitle = document.getElementById('edit-title');
        const saveTitle = document.getElementById('save-title');
        const editButton = document.getElementById('edit-button');
        const saveButtonE = document.getElementById('save-buttonE');
        const saveButtonG = document.getElementById('save-buttonG');
        const editSelect = document.getElementById('select-prod');
        //Agrego dos botones de Guardar, uno para Editar y otro para Agregar 
        const selpro = document.getElementById('selpro');

        $modal.classList.add('is-active');
        
        /*Si NO le paso un producto, me abre para agregar y si no pasa
        para editar*/
        if (!product) { //no le paso un producto, entonces entra a Agregar    
            editTitle.classList.add('is-hidden'); //esconde "Editar producto"
            saveButtonE.classList.add('is-hidden'); //esconde el botón de guardar para Editar
            saveTitle.classList.remove('is-hidden');
            saveButtonG.classList.remove('is-hidden');
        }
        else{
            saveTitle.classList.add('is-hidden'); //esconde "Agregar Producto"
            saveButtonG.classList.add('is-hidden'); //esconde el botón de guardar para Agregar
            editTitle.classList.remove('is-hidden');
            saveButtonE.classList.remove('is-hidden');
            editSelect.value = product;
            editSelect.disabled = true;
        }
    }
    /**
     * Cierra el modal
     **/
    function close($modal) {
        $modal.classList.remove('is-active');
    }

    /**
     * Inicializa el modal de agregar producto
     **/
    function init(config) {
        const $modal = document.querySelector(config.el);

        // Inicializamos el select de productos
        Select.init({
            el: '#select',
            data: config.products,
            onSelect: config.onProductSelect
        });

        // Nos ponemos a escuchar cambios en el input de cantidad
        $modal.querySelector('#quantity')
            .addEventListener('input', function () {
                config.onChangeQunatity(this.value)
            });
                    
        $modal.querySelector('#save-buttonE')
            .addEventListener('click', config.onEditProduct);
        /*coloco el listener para Editar y que llame el method PUT.
          Para esto llamo al botón guardar de Editar*/
        $modal.querySelector('#save-buttonG')
            .addEventListener('click', config.onAddProduct);
        /*coloco el listener para Agregar y que llame el method GET.
          Para esto llamo al boton guardar de Agregar*/

        return {
            close: close.bind(null, $modal),
            open: open.bind(null, $modal)
        }
    }

    return {
        init
    }
})();

