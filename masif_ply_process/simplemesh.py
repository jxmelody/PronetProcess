"""
simple_mesh.py: Simple ply loading class.
I created this class to avoid the need to install pymesh if the only goal is to load ply files.
Use this only for the pymol plugin. Currently only supports ascii ply files.
Pablo Gainza - LPDI STI EPFL 2019
This file is part of MaSIF.
Released under an Apache License 2.0
"""
import numpy as np


class Simple_mesh:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.header = []
        self.colors = []
        # Read header
        self.attribute_names = []
        self.num_verts = 0
        
    def save_mesh(self, filename):
        self.header_str = 'ply\nformat ascii 1.0\ncomment author: Xiao Jin\nelement vertex {0}\n\
property float x\n\
property float y\n\
property float z\n\
property uchar red\n\
property uchar green\n\
property uchar blue\n\
element face {1}\n\
property list uchar int vertex_indices\nend_header\n'.format(self.num_verts, self.num_faces)
        # for x in self.header:
        #     self.header_str += x
        self.body = np.hstack((self.vertices, self.colors))
        face_first_col = np.full((len(self.faces),1), 3)
        with open(filename, 'w') as wf:
            wf.write(self.header_str)
            np.savetxt(wf, self.body, fmt="%.4f %.4f %.4f %d %d %d")
            np.savetxt(wf, np.hstack((face_first_col, self.faces)), fmt="%d %d %d %d")

    def load_mesh(self, filename):
        lines = open(filename, "r").readlines()
        
        line_ix = 0
        while "end_header" not in lines[line_ix]:
            line = lines[line_ix]
            if line.startswith("element vertex"):
                self.num_verts = int(line.split(" ")[2])
            if line.startswith("property float"):
                self.attribute_names.append("vertex_" + line.split(" ")[2].rstrip())
            if line.startswith("element face"):
                self.num_faces = int(line.split(" ")[2])
            line_ix += 1
        line_ix += 1
        header_lines = line_ix
        self.attributes = {}
        for at in self.attribute_names:
            self.attributes[at] = []
        self.vertices = []
        self.normals = []
        self.faces = []
        # Read vertex attributes.
        for i in range(header_lines, self.num_verts + header_lines):
            cur_line = lines[i].split(" ")
            vert_att = [float(x) for x in cur_line]
            # Organize by attributes
            for jj, att in enumerate(vert_att):
                self.attributes[self.attribute_names[jj]].append(att)
            line_ix += 1
        # Set up vertices
        for jj in range(len(self.attributes["vertex_x"])):
            self.vertices = np.vstack(
                [
                    self.attributes["vertex_x"],
                    self.attributes["vertex_y"],
                    self.attributes["vertex_z"],
                ]
            ).T
        # Read faces.
        face_line_start = line_ix
        for i in range(face_line_start, face_line_start + self.num_faces):
            try:
                fields = lines[i].split(" ")
            except:
                ipdb.set_trace()
            face = [int(x) for x in fields[1:]]
            self.faces.append(face)
        self.faces = np.array(self.faces)
        self.vertices = np.array(self.vertices)
        # Convert to numpy array all attributes.
        for key in self.attributes.keys():
            self.attributes[key] = np.array(self.attributes[key])

    def get_attribute_names(self):
        return list(self.attribute_names)

    def get_attribute(self, attribute_name):
        return np.copy(self.attributes[attribute_name])

    def set_colors(self, data):
        self.colors = data
