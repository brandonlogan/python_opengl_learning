def load_ply(path):
    lines = [line.strip() for line in open(path)]
    lines = strip_header(lines)
    return get_data(lines)


def strip_header(lines):
    for index, line in enumerate(lines):
        if line == 'end_header':
            return lines[index + 1::]


def get_data(lines):
    vertices = []
    faces = []
    for line in lines:
        components = line.split(' ')
        if len(components) == 4:
            faces.append(components[1::])
        elif len(components) == 9:
            vertices.append(components)

    vertex_data = []
    for face in faces:
        for vert_index in face:
            vertex_data.append(vertices[int(vert_index)])

    positions = []
    colors = []
    normals = []
    for vertex in vertex_data:
        v_data = load_vertex_data(vertex)
        positions.extend(v_data[0])
        colors.extend(v_data[1])
        normals.extend(v_data[2])
    return {'vertices': positions, 'colors': colors, 'normals': normals}


def load_vertex_data(components):
    vert_pos = [float(components[index]) for index in range(3)]
    vert_pos.append(1.0)
    vert_norms = [float(components[index]) for index in range(3, 6)]
    vert_colors = [int(components[index]) for index in range(6, 9)]
    return vert_pos, vert_colors, vert_norms
