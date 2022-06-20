from pyntcloud import PyntCloud
import numpy as np
from simplemesh import Simple_mesh
import sys

colorDict = {
    "sky": [ 0.0, 0.76, 1.0],
    "sea": [ 0.0, 0.90, 0.5],
    "yellowtint": [ 0.88, 0.97, 0.02],
    "hotpink": [ 0.90, 0.40, 0.70],
    "greentint": [ 0.50, 0.90, 0.40],
    "blue": [ 0.0, 0.0, 1.0],
    "green": [ 0.0, 1.0, 0.0],
    "yellow": [ 1.0, 1.0, 0.0],
    "orange": [ 1.0, 0.5, 0.0],
    "red": [ 1.0, 0.0, 0.0],
    "black": [ 0.0, 0.0, 0.0],
    "white": [ 1.0, 1.0, 1.0],
    "gray": [ 0.9, 0.9, 0.9],
}

def iface_color(iface):
    # max value is 1, min values is 0
    hp = iface.copy()
    hp = hp * 2 - 1
    mycolor = charge_color(-hp)
    return mycolor


# Returns the color of each vertex according to the charge.
# The most purple colors are the most hydrophilic values, and the most
# white colors are the most positive colors.
def hphob_color(hphob):
    # max value is 4.5, min values is -4.5
    hp = hphob.copy()
    # normalize
    hp = hp + 4.5
    hp = hp / 9.0
    # mycolor = [ [COLOR, 1.0, hp[i], 1.0]  for i in range(len(hp)) ]
    mycolor = [[ 1.0, 1.0 - hp[i], 1.0] for i in range(len(hp))]
    return mycolor


# Returns the color of each vertex according to the charge.
# The most red colors are the most negative values, and the most
# blue colors are the most positive colors.
def charge_color(charges):
    # Assume a std deviation equal for all proteins....
    max_val = 1.0
    min_val = -1.0

    norm_charges = charges
    blue_charges = np.array(norm_charges)
    red_charges = np.array(norm_charges)
    blue_charges[blue_charges < 0] = 0
    red_charges[red_charges > 0] = 0
    red_charges = abs(red_charges)
    red_charges[red_charges > max_val] = max_val
    blue_charges[blue_charges < min_val] = min_val
    red_charges = red_charges / max_val
    blue_charges = blue_charges / max_val
    # red_charges[red_charges>1.0] = 1.0
    # blue_charges[blue_charges>1.0] = 1.0
    green_color = np.array([0.0] * len(charges))
    mycolor = [
        [
            0.9999 - blue_charges[i],
            0.9999 - (blue_charges[i] + red_charges[i]),
            0.9999 - red_charges[i],
        ]
        for i in range(len(charges))
    ]
    for i in range(len(mycolor)):
        for k in range(1, 3):
            if mycolor[i][k] < 0:
                mycolor[i][k] = 0

    return np.array(mycolor)*255

def convert_color(filename, save_filename):
    mesh = Simple_mesh()
    mesh.load_mesh(filename)
    verts = mesh.vertices
    try:
        charge = mesh.get_attribute("vertex_charge")
        color_array = charge_color(charge)
    except:
            print("Could not load vertex charges.")
            color_array = [colorDict["green"]] * len(verts)
    mesh.set_colors(color_array)
    mesh.save_mesh(save_filename)

def convert_bin(filename, save_filename):
    # convert to binary file
    plyfile = PyntCloud.from_file(filename)
    plyfile.to_file(save_filename,also_save=["mesh"])

if __name__ == "__main__":
    # filename = './P15873_A.ply'
    # save_filename = './saved_ply.ply'
    # save_filename_bin = './saved_ply_bin.ply'
    filename = sys.argv[1]
    save_filename = sys.argv[2]
    save_filename_bin = save_filename.replace('.ply', '_bin.ply')
    convert_color(filename, save_filename)
    convert_bin(save_filename, save_filename_bin)
