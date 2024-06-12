document.addEventListener('DOMContentLoaded', function () {
  centros_mascotas.forEach(centro => {
    let centro_direccion = document.getElementById(`dir_centro_${centro.id}`);
    let boton_centro = document.getElementById(`boton_centro_${centro.id}`);
    let mapa = document.querySelector('.centrosMap iframe');
    
    let direccion = centro.calle + ' ' + centro.numero_de_calle + ', ' + centro.localidad + ', ' + centro.provincia;

    if (centro_direccion !== null) {
      centro_direccion.innerText = `Dirección: ${direccion}`;
    }
    
    if (boton_centro !== null && mapa !== null) {
      boton_centro.addEventListener('click', function () {
        mapa.src = `https://maps.google.com/maps?q=${direccion}&t=&z=13&ie=UTF8&iwloc=&output=embed`
      })
    }
  })
})