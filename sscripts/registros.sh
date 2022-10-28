ruta_archivos="/home/gilberto/Desktop/temp/Registros_Sismicos_RACM_2010-2020/Formato_SAC/"
#lista_sismos=`ls $ruta_archivos | awk '{if ($1 ~ /-sac/)print $1}'`
lista_sismos="2014-05-08-sac 2014-04-18-sac 2013-08-21-sac 2012-11-15-sac 2012-04-11-sac 2012-04-02-sac 2012-03-20-sac 2011-12-11-sac 2010-06-30-sac 2020-06-23-sac"
for i in $lista_sismos; do
    datos=`ls $ruta_archivos$i/*.[VNE].sac | awk -F"[/]" '{print $9}'`
    fechasismo=`echo $i | awk -F[-] '{print $1"-"$2"-"$3}'`
    for registro in $datos;do
        componente=`echo $registro | awk -F[.] '{print $2}'`
        clave=`echo $registro | awk -F[.] '{print $1}'`
        printf -v data '{"archivo":"%s%s/%s","fechaSismo":"%s","estacion":"%s","componente":"%s"}' $ruta_archivos $i $registro $fechasismo $clave $componente
        echo $data
        curl -X POST http://localhost:5000/agregarRegistro -H 'Content-Type: application/json' -d "$data"
        sleep 0.1
    done
done