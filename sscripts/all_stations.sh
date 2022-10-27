ruta_archivos="/home/gilberto/Desktop/temp/Registros_Sismicos_RACM_2010-2020/Formato_SAC/"
ruta_ASA="/home/gilberto/Desktop/temp/Registros_Sismicos_RACM_2010-2020/Formato_ASA2.0/"
directorio=$1
registros=`ls $ruta_archivos$directorio-sac/*.sac | awk -F"[/]" '{print $9}' | awk -F[.] 'BEGIN{a=$1; print $1}{if ($1 != a){print $1; a=$1}}'`
estaciones=`cat $ruta_ASA$(echo $directorio)Est.txt | awk 'NR>1{print $1}'`
for i in $estaciones; do
    clave=`awk -v r=$i '{if ($1==r)print $2}' $ruta_ASA$(echo $directorio)Est.txt`
    institucion=`awk -v r=$i '{if ($1==r)print $3}' $ruta_ASA$(echo $directorio)Est.txt`
    lat=`awk -v r=$i '{if ($1==r)print $4}' $ruta_ASA$(echo $directorio)Est.txt`
    lon=`awk -v r=$i '{if ($1==r)print $5}' $ruta_ASA$(echo $directorio)Est.txt`
    printf -v data '{"clave":"%s","latitud":"%f","longitud":"%f","instituto":"%s"}' $clave $lat $lon $institucion
    echo $data
    curl -X POST http://localhost:5000/agregarEstacion -H 'Content-Type: application/json' -d "$data"
    sleep 0.5
done