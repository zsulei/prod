document.getElementById('materialSelect').addEventListener('change', loadSizes);
                                document.getElementById('colorSelect').addEventListener('change', loadSizes);

                                function loadSizes() {
                                    var materialSelect = document.getElementById('materialSelect');
                                    var colorSelect = document.getElementById('colorSelect');
                                    var materialName = materialSelect.options[materialSelect.selectedIndex].text;
                                    var colorName = colorSelect.options[colorSelect.selectedIndex].text;

                                    if(materialSelect.value !== "#" && colorSelect.value !== "#") {
                                        var xhr = new XMLHttpRequest();
                                        var materialNameEncoded = encodeURIComponent(materialName);
                                        var colorNameEncoded = encodeURIComponent(colorName);
                                        xhr.open('GET', `/products/get-sizes?materialName=${materialNameEncoded}&colorName=${colorNameEncoded}`, true);
                                        xhr.onload = function() {
                                            if (this.status === 200) {
                                                var sizes = JSON.parse(this.responseText);
                                                var sizeSelect = document.getElementById('sizeSelect');
                                                sizeSelect.innerHTML = '<option value="#" selected style="display:none">Выберите размер</option>';
                                                sizes.forEach(function(size) {
                                                    var option = document.createElement('option');
                                                    option.value = size.id;
                                                    option.text = size.value;
                                                    console.log(option)
                                                    sizeSelect.appendChild(option);
                                                });
                                            }
                                        };
                                        xhr.send();
                                    }
                                }

document.getElementById('add_to_cart_form_id').addEventListener('submit', function(e) {
    const sizeSelect = document.getElementById('sizeSelect');
    if (sizeSelect.value === "" || sizeSelect.value === "#") {
        alert('Пожалуйста, выберите размер.');
        e.preventDefault(); // Предотвратить отправку формы
    }
});


