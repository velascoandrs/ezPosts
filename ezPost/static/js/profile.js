class ApiLoader{

    constructor(url,id_component){
        this.url = url;
        this.base_url = url;
        this.id_component = id_component;
        this.base_url=this.url;
        this.$contenido = $(`#${this.id_component}`).empty();
    }

    set_url(pagina=1,parametros=''){
        let nombre_parametros =Object.keys(parametros);
        let parametros_str = "";
        if (parametros){
                nombre_parametros.forEach(
            (llave)=>{
                        parametros_str=parametros_str+`?${llave}=${parametros[llave]}`
                    }
                );
        }
        this.url=this.base_url+`${parametros_str}`;
        console.log(this.url)
    }

    limpiarComponente(){
        this.$contenido.empty();
    }


    cargarDatos(pagina,renderFunction){
         let url=this.url+`&page=${pagina}`;
         console.log(url);
         $.get(url,
                (data)=> {
                    let html = "";
                    if (data) {
                        data.results.forEach(
                            (info)=>{
                                html = html +renderFunction(info);
                            }
                        );
                        this.$contenido.append(html);
                    }else {
                        this.$contenido.append('<h2>No existen datos</h2>')
                    }
                }
        );
    }


}


    let pagina=1;
    let url= `/post/api/post`;
    let postUsuario = new ApiLoader(url,'contenido');
    let id_user = document.currentScript.getAttribute('id_user');

    function inicio(){
        postUsuario.set_url(1,{'autor_id':`${id_user}`});
        postUsuario.cargarDatos(1,PostRender)
    }

    window.onload=inicio;

    $(window).scroll(
        ()=>{
            var scroll_position_for_post_load = $(window).height() + $(window).scrollTop()+1;
            if (scroll_position_for_post_load >= $(document).height()){
                pagina++;
                postUsuario.cargarDatos(pagina,PostRender);
            }
        }
    );


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
                    </div>`;
    return html
}