    let pagina=1;
    let valor=null;
    let url= `/post/api/post?&page=`;
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

    }
    function cargarPosts(pagina,inicio=false){
        let $contenido = $("#contenido");
        if (inicio){
             valor=null;
             $contenido.empty();
             setPagina(0); //Antes era 1
             setUrl(1)
        }else {
            setUrl(pagina);
        }
        console.log(url);
        $.get(url,
                (data)=> {
                    let html = "";
                    if (data) {
                        data.results.forEach(
                            (post)=>{
                                let portada_img="https://bitcoinist.com/wp-content/uploads/2018/10/shutterstock_597074750.jpg";
                                if(post.portada==null){
                                    post.portada=portada_img
                                }
                                html = html +generarVista(post);
                            }
                        );
                        $contenido.append(html);
                    }else {
                        $contenido.append('<h2>No existen datos</h2>')
                    }
                    $('#loader').empty();
                }
        );
    }
    $(window).scroll(function(){
                            var scroll_position_for_post_load = $(window).height() + $(window).scrollTop() + 100;
                            if (scroll_position_for_post_load >= $(document).height()){
                                pagina++;
                                cargarPosts(pagina);
                            }

                        }
    );
    function buscarPost() {
                valor = document.getElementById('buscar').value;
                setPagina(1);
                $("#contenido").empty();
                cargarPosts(1)
    }

    function generarVista(post){
	    let html =`<div class="blog-card">
                        <div class="meta">
                         <div class="photo" style="background-image: url(${post.portada})">
                          </div>
                           <ul class="details">
                             <li><a href="/usuario/perfil/${post.autor.pk}">${post.autor.username}</a></li>
                             <li >${post.fecha_creacion}</li>
                            </ul>
                         </div>
                    <div class="description">
                    <h1>${post.titulo}</h1>
                    <p><strong>Categoría: </strong>${post.afinidad}</p>
                    <p class="read-more">
                    <a href="/post/ver/${post.pk}">Leer mas..</a>
                    </p>
                    </div>
                    </div>`;
    return html
}