# ./bin/pymol -c script.pml

# load  /data/xiaojin/Human/
# multisave AF-A2P2R3-F1-model_v1_pymol.pdb

# dir="/home/xiaojin/ProteomicsNucleicServer/python-docker/python-docker/subsetofpymol/sub"
dir="/data/xiaojin/pymol/Human"
for subdir in  `ls ${dir}`
do
    for file in `ls $dir/${subdir}`
    do
        path="$dir/${subdir}/${file}"
        echo load ${path} >> batch_Human.pml
        echo multisave ${path/.pse/.pdb} >> batch_Human.pml
    done
done

./bin/pymol -c batch_Human.pml