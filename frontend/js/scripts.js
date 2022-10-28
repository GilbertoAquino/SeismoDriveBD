var gsismo = "";
var gcomponente = "";
var gest="";

function loadJSON() {
    $("#descargarTodoSismo").addClass("d-none");
    $("#descargarTodoEst").addClass("d-none");
    $(".sismotabla").remove();
    $.ajax({
       url:"http://localhost:5000/consultarTodoSismos",
       type: "GET",
       success: function (result){
         $("#sismotitulo").text("");
         $("#ErrorAPI_2").text("");
          $("#dinamic_table").append("<thead class=sismotabla><tr><th scope=col>Fecha sismo</th><th scope=col >Magnitud</th><th scope=col >Latitud</th><th scope=col >Longitud</th><th scope=col >profundidad</th><th scope=col >Registros</th></tr></thead>");
          $("#dinamic_table").append("<tbody class=sismotabla>");
          for (let i of result["Sismos"]){
             $("#dinamic_table").append(
                "<tr class=sismotabla id=sismotabla_id_"+i["id"]+"><td scope=row id=fecha_sismotabla_id_"+i["id"]+" value="+i["fecha"]+">"+i["fecha"]+
                   "</td><td>"+i["magnitud"]+"</td><td>"+i["latitud"]+"</td><td>"+i["longitud"]+
                      "</td><td>"+i["profundidad"]+
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
  function busqueda_sismo() {
   $("#descargarTodoSismo").addClass("d-none");
   $("#descargarTodoEst").addClass("d-none");
   $(".sismotabla").remove();
   f1 = $("#finicio").val();
   f2 = $("#ffinal").val();
   m1 = $("#minicio").val();
   m2 = $("#mfinal").val();
   p1 = $("#pinicio").val();
   p2 = $("#pfinal").val();
   $.ajax({
      url:"http://localhost:5000/consultarSismosParametros",
      type: "POST",
      contentType:"application/json; charset=utf-8",
      dataType:"json",
      headers: {'Authorization': 'Bearer '+readCookie("access_token")},
      data:JSON.stringify({finicio: f1,ffinal: f2,minicio:m1,mfinal:m2,pinicio:p1,pfinal:p2 }),
      success: function (result){
        $("#sismotitulo").text("");
        $("#ErrorAPI_2").text("");
         $("#dinamic_table").append("<thead class=sismotabla><tr><th scope=col>Fecha sismo</th><th scope=col >Magnitud</th><th scope=col >Latitud</th><th scope=col >Longitud</th><th scope=col >profundidad</th><th scope=col >Registros</th></tr></thead>");
         $("#dinamic_table").append("<tbody class=sismotabla>");
         for (let i of result["Sismos"]){
            $("#dinamic_table").append(
               "<tr class=sismotabla id=sismotabla_id_"+i["id"]+"><td scope=row id=fecha_sismotabla_id_"+i["id"]+" value="+i["fecha"]+">"+i["fecha"]+
                  "</td><td>"+i["magnitud"]+"</td><td>"+i["latitud"]+"</td><td>"+i["longitud"]+
                     "</td><td>"+i["profundidad"]+
                     "</td><td class=buttons_comp><button onclick='check_registros_por_sismo(this)' value=V class='btn btn-primary' >V</button> <button class='btn btn-primary' onclick='check_registros_por_sismo(this)' value=N >N</button> <button class='btn btn-primary' onclick='check_registros_por_sismo(this)' value=E>E</button> <button class='btn btn-primary' onclick='check_registros_por_sismo(this)' value=all>Todos</button></td></tr>"
               );
         }
         $("#dinamic_table").append("</tbody>");
      },
      error: function(result){
       if (result.status == 401){
         window.location.replace("./login.html");
       }
       $("#ErrorAPI_1").text("Error en el servidor");
      }
   })
 }
 
  function check_registros_por_sismo(object){
   $("#descargarTodoSismo").removeClass("d-none");
   $("#descargarTodoEst").addClass("d-none");
    var comp = object.value;
    var parent_id = object.parentNode.parentNode.id;
    var element = document.getElementById("fecha_"+parent_id);
    var sismos = element.getAttribute("value");
    gsismo = sismos
    gcomponente = comp
    $.ajax({
       url:"http://localhost:5000/consultarRegistrosPorSismo",
       type:"POST",
       contentType:"application/json; charset=utf-8",
       dataType:"json",
       headers: {'Authorization': 'Bearer '+readCookie("access_token")},
       data:JSON.stringify({ sismo: sismos, componente: comp }),
       success:function(result){
        $(".registrotabla").remove();
        try{
            $("#sismotitulo").text(result[0]["sismo"]);
        }
        catch{
            $("#sismotitulo").text("No hay registros disponibles");
        }
        $("#registros_dinamic").append("<thead class='sismotabla registrotabla'><tr><th scope=col >Estacion</th><th scope=col >Componente</th><th scope=col >Registro</th></tr></thead>");
        var dum = null;
        $("#registros_dinamic").append("<tbody class=sismotabla>");
        for (let i of result){
          $("#registros_dinamic").append("<tr class='sismotabla registrotabla'><td scope=row >"+i["estacion"]+"</td><td>"+i["componente"]+"</td><td><a href="+i["link"]+">Descargar</a></td></tr>");
        }
        $("#registros_dinamic").append("</tbody>");
       }
    });
  }
  function check_registros_por_estacion(){
   $("#descargarTodoSismo").addClass("d-none");
   $("#descargarTodoEst").removeClass("d-none");
   var estacions = $("#id_estacion_search").val();
   gest = estacions;
   $.ajax({
      url:"http://localhost:5000/consultarRegistrosPorEstacion",
      type:"POST",
      contentType:"application/json; charset=utf-8",
      dataType:"json",
      headers: {'Authorization': 'Bearer '+readCookie("access_token")},
      data:JSON.stringify({ estacion: estacions}),
      success:function(result){
         $("#ErrorAPI_2").text(result[0]["estacion"]);
         $(".registrotabla").remove();
         $(".sismotabla").remove();
         $("#sismotitulo").text("");
        $("#dinamic_table_est").append("<thead class='sismotabla registrotabla'><tr><th scope=col >Fecha</th><th scope=col >Estacion</th><th scope=col >Componente</th><th scope=col >Registro</th></tr></thead>");
        var dum = null;
        $("#dinamic_table_est").append("<tbody class=sismotabla>");
        for (let i of result){
          $("#dinamic_table_est").append("<tr class='sismotabla registrotabla'><td scope=row >"+i["sismo"]+"</td><td scope=row >"+i["estacion"]+"</td><td>"+i["componente"]+"</td><td><a href="+i["link"]+">Descargar</a></td></tr>");
        }
        $("#dinamic_table_est").append("</tbody>");
      },
      error:function(result){
         $("#ErrorAPI_2").text("No se encontro la estacion ingresada");
      }
   })
}
function descargarTodoS(){
   $.ajax({
      url:"http://localhost:5000/descargaZip",
      type:"POST",
      contentType:"application/json; charset=utf-8",
      dataType:"json",
      headers: {'Authorization': 'Bearer '+readCookie("access_token")},
      data:JSON.stringify({ sismo: gsismo, componente: gcomponente }),
      success:function(result){
         $("#btnclosetache").removeClass("d-none");
         $("#btnclosenormal").removeClass("d-none");
         $("#textochidix").fadeOut(function(){$(this).text("")}).fadeIn();
         $("#staticBackdropLabel").fadeOut(function(){$(this).text("Se ha realizado la descarga")}).fadeIn();
         $("#spinner").fadeOut(function(){$(this).addClass("d-none")})
         $("#imgsuccess").fadeIn(function(){$(this).removeClass("d-none")})
         window.location.replace(result["link"]);
      }
   })
}
function descargarTodoE(){
   $.ajax({
      url:"http://localhost:5000/descargaZipEst",
      type:"POST",
      contentType:"application/json; charset=utf-8",
      dataType:"json",
      headers: {'Authorization': 'Bearer '+readCookie("access_token")},
      data:JSON.stringify({ estacion: gest}),
      success:function(result){
         $("#btnclosetache").removeClass("d-none");
         $("#btnclosenormal").removeClass("d-none");
         $("#textochidix").fadeOut(function(){$(this).text("")}).fadeIn();
         $("#staticBackdropLabel").fadeOut(function(){$(this).text("Se ha realizado la descarga")}).fadeIn();
         $("#spinner").fadeOut(function(){$(this).addClass("d-none")})
         $("#imgsuccess").fadeIn(function(){$(this).removeClass("d-none")})
         window.location.replace(result["link"]);
      }
   })
}
function addDnone(){
   $("#staticBackdropLabel").text("Descargando zip...");
   $("#textochidix").text("Puede tardar varios minutos...");
   $("#imgsuccess").addClass("d-none");
   $("#spinner").removeClass("d-none");
   $("#btnclosetache").addClass("d-none");
   $("#btnclosenormal").addClass("d-none");
}

function login(){
   user = $("#username_id").val();
   pass = $("#password_id").val();
   $.ajax({
      url:"http://localhost:5000/login",
      type:"POST",
      contentType:"application/json; charset=utf-8",
      dataType:"json",
      data:JSON.stringify({ username: user,password:pass}),
      success:function(result){
         document.cookie='access_token='+result["access_token"];
         window.location.replace("./index.html");
      },
      error:function(result){
         console.log("badrequest");
      }
   })
}

function readCookie(name) {
   var nameEQ = name + "=";
   var ca = document.cookie.split(';');
   for (var i = 0; i < ca.length; i++) {
       var c = ca[i];
       while (c.charAt(0) == ' ') c = c.substring(1, c.length);
       if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
   }
   return null;
}