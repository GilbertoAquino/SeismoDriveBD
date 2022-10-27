function loadJSON() {
    let test = $("#id_Nombre").val();
    $(".sismotabla").remove();
    $.ajax({
       url:"http://localhost:5000/consultarTodoSismos"+test,
       type: "GET",
       success: function (result){
          $("#dinamic_table").append("<thead class=sismotabla><tr><th scope=col>Fecha sismo</th><th scope=col >Magnitud</th><th scope=col >Latitud</th><th scope=col >Longitud</th><th scope=col >Registros</th></tr></thead>");
          $("#dinamic_table").append("<tbody class=sismotabla>");
          for (let i of result["Sismos"]){
             $("#dinamic_table").append(
                "<tr class=sismotabla id=sismotabla_id_"+i["id"]+"><td scope=row id=fecha_sismotabla_id_"+i["id"]+" value="+i["fecha"]+">"+i["fecha"]+
                   "</td><td>"+i["magnitud"]+"</td><td>"+i["latitud"]+"</td><td>"+i["longitud"]+
                      "</td><td class=buttons_comp><button onclick='check_registros_por_sismo(this)' value=V class='btn btn-primary' >V</button> <button class='btn btn-primary' onclick='check_registros_por_sismo(this)' value=N >N</button> <button class='btn btn-primary' onclick='check_registros_por_sismo(this)' value=E>E</button> <button class='btn btn-primary' onclick='check_registros_por_sismo(this)' value=all>Todos</button></td></tr>"
                );
          }
          $("#dinamic_table").append("</tbody>");
       },
       error: function(result){
        $("#ErrorAPI_1").text("Error en el servidor");
       }
    })
  }
 
  function check_registros_por_sismo(object){
    var comp = object.value;
    var parent_id = object.parentNode.parentNode.id;
    var element = document.getElementById("fecha_"+parent_id);
    var sismos = element.getAttribute("value");
    $.ajax({
       url:"http://localhost:5000/consultarRegistrosPorSismo",
       type:"POST",
       contentType:"application/json; charset=utf-8",
       dataType:"json",
       data:JSON.stringify({ sismo: sismos, componente: comp }),
       success:function(result){
        $(".registrotabla").remove();
        try{
            $("#sismotitulo").text(result[0]["sismo"]);
        }
        catch{
            $("#sismotitulo").text("No hay registros disponibles");
        }
        $("#registros_dinamic").append("<thead class=registrotabla><tr><th scope=col >Estacion</th><th scope=col >Componente</th><th scope=col >Registro</th></tr></thead>");
        var dum = null;
        $("#registros_dinamic").append("<tbody class=sismotabla>");
        for (let i of result){
          $("#registros_dinamic").append("<tr class=registrotabla><td scope=row >"+i["estacion"]+"</td><td>"+i["componente"]+"</td><td><a href="+i["link"]+">Descargar</a></td></tr>");
        }
        $("#registros_dinamic").append("</tbody>");
       }
    });
  }