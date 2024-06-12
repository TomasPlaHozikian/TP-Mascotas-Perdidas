document.addEventListener('DOMContentLoaded', function () {
  centros_mascotas.forEach(centro => {
    let boton_centro = document.getElementById(`boton_centro_${centro.id}`);
    let mapa = document.querySelector('.centrosMap iframe');
    if (boton_centro !== null && mapa !== null) {
      boton_centro.addEventListener('click', function () {
        mapa.src = `https://maps.google.com/maps?q=${centro.direccion}&t=&z=13&ie=UTF8&iwloc=&output=embed`
      })
    }
  })
})