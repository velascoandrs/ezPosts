// Al cargar la pagina y cada 5 segundos
// 1 consultar notificaciones
let $status = $("#status");
let $lista_avisos = $("#contenedor_avisos");
setInterval("obtener_notificaciones();",5000);
function obtener_notificaciones(){

    console.log("CARGANDO..");
      let url = '/post/api/avisos';
      $.get(
          url,
          (data)=>{
              console.log(data);
              $lista_avisos.empty();
              buscar_nuevos_avisos(data);
              llenar_lista(data);
          }
      );
}
obtener_notificaciones();

$status.click(()=>
{
    $.post(
        '/post/avisos/marcar-revisado',
        (data)=>{
            if(data === 'OK'){
                console.log("Avisos revisados")
                console.log("CLICK DETECTADO");
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
        $lista_avisos.css({"height":"100px"})
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
                    const post = post_detail_render(dato.post);
                    const html = $(`<a id="aviso" class="dropdown-item" href="/post/ver/${dato.post.pk}">
                                        <p class="text-white">${dato.contenido}</p>
                                        <span class="text-success">${dato.fecha_creacion}</span>
                                        ${post}
                                    </a>`);
                    $lista_avisos.append(html);
                    ajustar_menu();
                }
            );
        return 1
}

function post_detail_render(post){
	    let html =`<div class="blog-card">
                    <div class="description">
                        <h1 class="titulo">${post.titulo}</h1>  
                    </div>
                        <div class="meta">
                         <div class="photo" style="background-image: url(${post.portada})">
                          </div>
                         </div>
                    
                    </div>`;
    return html
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
