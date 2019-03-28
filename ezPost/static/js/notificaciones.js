// Al cargar la pagina y cada 5 segundos
// 1 consultar notificaciones
let $status = $("#status");
let $lista_avisos = $("#contenedor_avisos");
let url_inicial = '/post/api/avisos?page=';
let altura = 1662;
let lista_esta_clickeada = false;
setInterval("obtener_notificaciones();",5000);


function obtener_notificaciones(){
    if(!lista_esta_clickeada){
        console.log("CARGANDO..");
        altura = 1662;
      let url = '/post/api/avisos?page=1';
      cargarDatos(url)
    }else {
        console.log("ESPERANDO..");
    }

}


$(window).click(
    ()=>{
        console.log("Se oculto");
        lista_esta_clickeada = false;
    }
);
function cargarDatos(url,limpiar=true) {
    console.log(url);
    $.get(
          url,
          (data)=>{
              console.log(data);
              if (limpiar){
                  $lista_avisos.empty();
              }
              buscar_nuevos_avisos(data);
              llenar_lista(data);
          }
      );
}

$lista_avisos.scroll(
    ()=>{
            var scroll_position_for_post_load = $lista_avisos.height() + $lista_avisos.scrollTop()+1;
            console.log(scroll_position_for_post_load,altura,$lista_avisos.height());
            if (scroll_position_for_post_load >= altura ){
                pagina++;
                altura = scroll_position_for_post_load+$lista_avisos.height()-1;
                let url = url_inicial+pagina;
                cargarDatos(url,false);
            }
        }
);

obtener_notificaciones();

$status.click(()=>
{
    lista_esta_clickeada = false === lista_esta_clickeada;
    $.post(
        '/post/avisos/marcar-revisado',
        (data)=>{
            if(data === 'OK'){
                pintar_campana_notificaiones(false);
            }else {
                console.log("Error del servidor")
            }
        }
    );
});

function ajustar_menu() {
    var count = $lista_avisos.children().length;
    console.log(count);
    if(count>3){
        console.log("Se ajusto");
        $lista_avisos.css({"height":"350px","position":"relative"})
    }
}
// 2 si existen notificaciones sin revisar -> marcar icono
function buscar_nuevos_avisos(avisos) {
    let no_esta_revisado = avisos.results.some(
        (aviso)=>{
            return aviso.esta_revisado == false
        }

    );
    console.log(no_esta_revisado);
    // Si no esta revisado el aviso pintar el icono de la campana
    if (no_esta_revisado){
        pintar_campana_notificaiones()
    }
}

function pintar_campana_notificaiones(estado=true) {
        console.log("Pintando");
        if(estado){
            $status.removeClass("far fa-bel");
            $status.addClass("fa fa-bel rojo")
        }else {
            $status.removeClass("fa fa-bel rojo");
            $status.addClass("far fa-bel")
        }
}

function llenar_lista(datos) {
        // Si no existen avisos
        if(!datos.count){
            console.log("Estoy aqui");
            let html = `<a id="aviso" class="dropdown-item" href="#">Sin Notificaciones</a>`;
            $lista_avisos.empty();
            $lista_avisos.append(html);
            return 0
        }
        datos.results.forEach(
                (dato) => {
                    console.log("Llenando");
                    const publicacion = post_detail_render(dato);
                    const html = $(`<a id="aviso" class="dropdown-item" href="/post/ver/${0}">
                                        <p class="text-white">${dato.contenido}</p>
                                        <span class="text-success">${"interpretar_fecha(dato.fecha_creacion)"}</span>
                                        ${publicacion}
                                    </a>`);
                    $lista_avisos.append(html);
                    ajustar_menu();
                }
            );
        return 1
}

function interpretar_fecha(fecha) {
    const fecha_ = moment(fecha, "YYYY-MM-DD");
    const fecha_actual = moment(new Date().toISOString().split('T')[0]);
    return 'hace '+fecha_actual.diff(fecha_, 'days')+' dias'
}

function post_detail_render(aviso){
        console.log("aviso ", aviso);
	    return `<div class="blog-card">
                    <div class="description">
                        <h2 class="titulo text-dark"><strong>${aviso.publicacion.post.titulo}</strong></h2>  
                    </div>
                        <div class="meta">
                         <div class="photo" style="background-image: url(${aviso.publicacion.post.portada})">
                          </div>
                         </div>
                </div>`;
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
