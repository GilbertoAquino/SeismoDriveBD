ruta_archivos="/home/gilberto/Desktop/temp/Registros_Sismicos_RACM_2010-2020/Formato_SAC/"
lista_sismos=`ls $ruta_archivos | awk '{if ($1 ~ /-sac/)print $1}'`
