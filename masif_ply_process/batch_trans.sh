dir="/data2/project/ProteinDB/masif/af2/Yeast"
dir_out="/data2/project/ProteinDB/masif/af2_color/Yeast"

for subdir in  `ls ${dir}`
do
    for file in `ls $dir/${subdir}`
    do
        path="$dir/${subdir}/${file}"
        color_path="$dir_out/${subdir}/${file}"
        color_path=${color_path/.ply/_color.ply}
        color_bin_path=${color_path/.ply/_bin.ply}
        if [ ! -d "$dir_out/${subdir}" ];then
            mkdir "$dir_out/${subdir}"
        fi
        if [ ! -f ${color_bin_path} ];then
            python process.py ${path} ${color_path}
        fi
        echo done_ ${color_path}
    done
done

