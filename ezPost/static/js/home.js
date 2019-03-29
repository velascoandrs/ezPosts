    let pagina=1;
    let valor=null;
    let url= `/post/api/post?&page=`;
    let custom_url = '';

    function inicio(){
        $(document).ready(function() {cargarPosts(1);});
    }
    window.onload=inicio;
    function setPagina(valor) {
        pagina = valor;
    }

    function setUrl(pagina) {
        if(valor){
            url= `/post/api/post?titulo=${valor}&page=${pagina}`;
        }else {
            url= `/post/api/post?&page=${pagina}`;
        }
        if (custom_url){
            url=`${custom_url}&page=${pagina}`
        }

    }

    const promesaLimpiar = ()=>{
        return new Promise((resolve,reject)=>{
            $("#contenido").empty()
            resolve('Se ha limpiado');
        })
    };
    function limpiar() {
        valor=null;
        setPagina(0); //Antes era 1
        setUrl(1);
        $("#contenido").empty();
    }
    function cargarPosts(pagina,inicio=false){
        let $contenido = $("#contenido");
        if (inicio){
            $("#title").empty();
            $("#title").append('<h2 class="titulo text-white"><strong>Post más recientes</strong></h2>');
            limpiar();
        }else {
            setUrl(pagina);
        }
        mostrar_animacion_cargando();
        console.log(url);
        $.get(url,
                (data)=> {
                    let html = "";
                    if (data) {
                        console.log(data);
                        remover_animacion_cargando();
                        data.results.forEach(
                            (post)=>{
                                let portada_img="https://bitcoinist.com/wp-content/uploads/2018/10/shutterstock_597074750.jpg";
                                if(post.portada==null){
                                    post.portada=portada_img
                                }
                                html = html +PostRender(post);
                            }
                        );
                        $contenido.append(html);
                    }else {
                        $contenido.append('<h2>No existen datos</h2>')
                    }
                }
        );
    }
    $(window).scroll(
        ()=>{
            var scroll_position_for_post_load = $(window).height() + $(window).scrollTop()+1;
            if (scroll_position_for_post_load >= $(document).height()){
                pagina++;
                cargarPosts(pagina);
            }
        }
    );

    function mostrar_animacion_cargando() {
        if ($("#loader")){
            remover_animacion_cargando();
        }
        $("#contenido").append('<div id="loader" class="d-flex justify-content-center">'+
            '<div class="p-2">'+
            '<div  class="spinner-grow text-success" role="status">'+
            '<span class="sr-only">Loading...</span>'+
            '</div><div  class="spinner-grow text-warning" role="status">'+
            '<span class="sr-only">Loading...</span>'+
            '</div>' +
            '<div  class="spinner-grow text-danger" role="status">'+
            '<span class="sr-only">Loading...</span>'+
            '</div>' +
            '</div>' +
            '</div>');
    }

    function remover_animacion_cargando() {
        $("#loader").remove();
    }

    function buscarPost() {
        promesaLimpiar()
            .then(
                (resultado)=>{
                      console.log(resultado)
                      valor = document.getElementById('buscar').value;
                      setPagina(1);
                      $("#contenido").empty();
                      $("#title").empty();
                      $("#title").append('<h2 class="titulo text-white"><strong>Resultados de la busqueda</strong></h2>');
                      cargarPosts(1)
                }
            );
    }
    function PostRender(post){
	    let html =`<div  class="bg-dark" style="border-radius: 5px">
                    <div class="blog-card">
                    <div class="description">
                        <h1 class="titulo">${post.titulo}</h1>
                        <div class="d-flex bd-highlight mb-3">
                                <div class="mr-auto p-2">
                                    <p><strong>Categoría: </strong>${post.afinidad}</p>
                                    <p><strong>Visualizaciones: </strong>${post.visualizaciones}</p>
                                </div>
                                <div class="p-2 ">
                                     <a href="/post/ver/${post.pk}"><button class="btn btn-dark">Leer mas..</button></a>
                                </div>
                        </div>
                        
                    </div>
                        <div class="meta">
                         <div class="photo" style="background-image: url(${post.portada})">
                          </div>
                         </div>
                    
                    </div>  
                            <div class="container">
                            <div class="d-flex justify-content-center text-white">
                                <div class="p-2">
                                    <a  href="/usuario/perfil/${post.publicacion.autor.pk}">
                                    <image 
                                        src="${post.publicacion.autor.perfil.foto_perfil}" 
                                        class="img-responsive rounded-circle" style="width: 64px;height: 64px"/>
                                    </a>
                                </div>
                                <div class="p-2">
                                    <a href="/usuario/perfil/${post.publicacion.autor.pk}"><strong class="text-white">${post.publicacion.autor.username}</strong></a>
                                    <br>
                                    <span>${interpretar_fecha(post.publicacion.fecha_creacion)}</span>
                                </div>
                            </div>    
                        </div>

                    </div>`;
    return html
}