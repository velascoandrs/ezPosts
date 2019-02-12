// Al cargar la pagina y cada 5 segundos
// 1 consultar notificaciones
let $status = $("#status");
let $lista_avisos = $("#avisos");
setInterval("obtener_notificaciones();",5000);
function obtener_notificaciones(){
      let url = '';
      $.get(
          url,
          (data)=>{
              $lista_avisos.empty();
              buscar_nuevos_avisos(data);
              llenar_lista(data);
          }
      );
}

$lista_avisos.click(
    $.get(
        '',
        (data)=>{
            if(data == 'OK'){
                console.log("Avisos revisados")
            }else {
                console.log("Error del servidor")
            }
        }
    )
);
// 2 si existen notificaciones sin revisar -> marcar icono
function buscar_nuevos_avisos(avisos) {
    let esta_revisado = avisos.results.some(
        (aviso)=>{
            return aviso.esta_revisado === false
        }
    );
    if (!esta_revisado){
        $status.removeClass("far fa-bel");
        $status.addClass("fa fa-bel rojo")
    }
}
function llenar_lista(datos) {
        datos.results.forEach(
                (dato) => {
                    const html = $(`<li  value=${dato.id}><a id="aviso" class="dropdown-item" href="#">${dato.contenido}</a></li>`);
                    $lista_avisos.append(html);
                }
            );
}
// Al hacer click en las notificaciones
// 1. Marcar como revisadas las no revisadas -> hace una solicitud a una url
// En el backend
// 1.1 La vista debe requerir que este auntentificado
// 1.2 usar el id del usuario que realiza la peticion sacar este id de la session
// 1.3 filtrar los avisos no revisados
// 1.4 Actualizar cada aviso filtrado por aviso revisado

// Solucion a la parte 1.2, 1.3, 1.4
// Aviso.objects.filter(post__autor__pk=request.user.id).filter(esta_revisado=False).update(esta_revisado=True)
