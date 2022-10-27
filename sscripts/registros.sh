ruta_archivos="/home/gilberto/Desktop/temp/Registros_Sismicos_RACM_2010-2020/Formato_SAC/"
#lista_sismos=`ls $ruta_archivos | awk '{if ($1 ~ /-sac/)print $1}'`
lista_sismos="2017-09-08-sac 2017-09-19-sac"
for i in $lista_sismos; do
    datos=`ls $ruta_archivos$i/*.[VNE].sac | awk -F"[/]" '{print $9}'`
    fechasismo=`echo $i | awk -F[-] '{print $1"-"$2"-"$3}'`
    for registro in $datos;do
        componente=`echo $registro | awk -F[.] '{print $2}'`
        clave=`echo $registro | awk -F[.] '{print $1}'`
        printf -v data '{"archivo":"%s%s/%s","fechaSismo":"%s","estacion":"%s","componente":"%s"}' $ruta_archivos $i $registro $fechasismo $clave $componente
        echo $data
        curl -X POST http://localhost:5000/agregarRegistro -H 'Content-Type: application/json' -d "$data"
        sleep 2
    done
done