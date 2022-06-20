
# Debian/Ubuntu/Mint
# apt-get install git build-essential python3-dev libglew-dev \
#   libpng-dev libfreetype6-dev libxml2-dev \
#   libmsgpack-dev python3-pyqt5.qtopengl libglm-dev libnetcdf-dev

# CentOS
yum install gcc gcc-c++ kernel-devel python-devel tkinter python-pmw glew-devel \
  freeglut-devel libpng-devel freetype-devel libxml2-devel glm-devel \
  msgpack-devel netcdf-devel

mkdir pymol

git clone https://github.com/schrodinger/pymol-open-source.git
git clone https://github.com/rcsb/mmtf-cpp.git
mv mmtf-cpp/include/mmtf* pymol-open-source/include/
cd pymol-open-source

python setup.py install --prefix=$PWD/../pymol

# now you can use pymol by
cd ../pymol
./bin/pymol -c script.pml