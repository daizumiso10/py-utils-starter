import numpy as np
from PIL import Image

from pyutils.image3d import depth_to_mesh, image_to_3d, write_obj


def test_depth_to_mesh_vertex_and_face_counts():
    depth = np.array([[0.0, 0.5], [1.0, 0.25]], dtype=np.float32)
    vertices, faces, colors = depth_to_mesh(depth, depth_scale=10.0)

    assert vertices.shape == (4, 3)
    assert faces.shape == (2, 3)
    assert colors is None


def test_depth_to_mesh_vertex_positions():
    depth = np.array([[0.0, 0.5], [1.0, 0.25]], dtype=np.float32)
    vertices, faces, colors = depth_to_mesh(depth, depth_scale=10.0)

    # vertex i is at grid position (x=i % width, y=i // width).
    np.testing.assert_allclose(vertices[0], [0, 0, 0.0])
    np.testing.assert_allclose(vertices[1], [1, 0, 5.0])
    np.testing.assert_allclose(vertices[2], [0, -1, 10.0])
    np.testing.assert_allclose(vertices[3], [1, -1, 2.5])


def test_depth_to_mesh_faces_reference_valid_vertices():
    depth = np.zeros((3, 4), dtype=np.float32)
    vertices, faces, _ = depth_to_mesh(depth)

    assert faces.min() >= 0
    assert faces.max() < len(vertices)
    assert faces.shape == (2 * 2 * 3, 3)


def test_depth_to_mesh_with_image_returns_colors():
    depth = np.zeros((2, 2), dtype=np.float32)
    image = Image.new("RGB", (2, 2), color=(255, 0, 0))
    _, _, colors = depth_to_mesh(depth, image=image)

    assert colors.shape == (4, 3)
    np.testing.assert_allclose(colors[0], [1.0, 0.0, 0.0])


def test_write_obj_without_colors(tmp_path):
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, -1, 1]], dtype=np.float32)
    faces = np.array([[0, 1, 2]], dtype=np.int64)
    out_path = tmp_path / "mesh.obj"

    write_obj(out_path, vertices, faces)
    lines = out_path.read_text().splitlines()

    assert lines[0] == "v 0.0000 0.0000 0.0000"
    assert lines[-1] == "f 1 2 3"


def test_write_obj_with_colors(tmp_path):
    vertices = np.array([[0, 0, 0]], dtype=np.float32)
    faces = np.array([[0, 0, 0]], dtype=np.int64)
    colors = np.array([[1.0, 0.5, 0.0]], dtype=np.float32)
    out_path = tmp_path / "mesh.obj"

    write_obj(out_path, vertices, faces, colors)
    lines = out_path.read_text().splitlines()

    assert lines[0] == "v 0.0000 0.0000 0.0000 1.0000 0.5000 0.0000"


def test_image_to_3d_writes_obj_file(tmp_path, monkeypatch):
    image_path = tmp_path / "input.png"
    Image.new("RGB", (4, 4), color=(0, 128, 255)).save(image_path)
    output_path = tmp_path / "output.obj"

    def fake_estimate_depth(image, model_name=None):
        width, height = image.size
        return np.zeros((height, width), dtype=np.float32)

    monkeypatch.setattr("pyutils.image3d.estimate_depth", fake_estimate_depth)

    result = image_to_3d(image_path, output_path, max_size=4)

    assert result == str(output_path)
    assert output_path.exists()
    lines = output_path.read_text().splitlines()
    vertex_lines = [line for line in lines if line.startswith("v ")]
    face_lines = [line for line in lines if line.startswith("f ")]
    assert len(vertex_lines) == 16
    assert len(face_lines) == 2 * 3 * 3
