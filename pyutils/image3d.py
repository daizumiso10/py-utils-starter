"""Convert a 2D image into a 3D mesh using AI monocular depth estimation."""

from __future__ import annotations

import os
from typing import Optional, Tuple

import numpy as np
from PIL import Image

DEFAULT_MODEL = "Intel/dpt-hybrid-midas"


def estimate_depth(image: Image.Image, model_name: str = DEFAULT_MODEL) -> np.ndarray:
    """Estimate a per-pixel depth map for image using a MiDaS depth-estimation model.

    Returns a (height, width) float32 array normalized to the range [0, 1],
    where higher values mean closer to the camera.
    """
    from transformers import pipeline

    depth_pipe = pipeline("depth-estimation", model=model_name)
    result = depth_pipe(image)
    depth = np.array(result["depth"], dtype=np.float32)

    d_min, d_max = float(depth.min()), float(depth.max())
    if d_max > d_min:
        depth = (depth - d_min) / (d_max - d_min)
    else:
        depth = np.zeros_like(depth)
    return depth


def depth_to_mesh(
    depth: np.ndarray,
    image: Optional[Image.Image] = None,
    depth_scale: float = 50.0,
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """Build a triangle grid mesh from a depth map.

    Each pixel becomes a vertex at (x, -y, depth * depth_scale); adjacent
    pixels are connected into two triangles per grid cell. If image is
    given, its RGB values (0-1) are returned as per-vertex colors aligned
    with vertices.

    Returns (vertices, faces, colors), where colors is None if image is
    not provided.
    """
    height, width = depth.shape
    xs, ys = np.meshgrid(np.arange(width), np.arange(height))
    zs = depth * depth_scale

    # Flip y so the mesh reads right-side-up in most 3D viewers.
    vertices = np.stack([xs, -ys, zs], axis=-1).reshape(-1, 3).astype(np.float32)

    colors = None
    if image is not None:
        rgb = np.array(image.convert("RGB"), dtype=np.float32) / 255.0
        colors = rgb.reshape(-1, 3)

    row_idx = np.arange(height - 1)[:, None] * width + np.arange(width - 1)[None, :]
    v0 = row_idx.ravel()
    v1 = v0 + 1
    v2 = v0 + width
    v3 = v0 + width + 1
    faces = np.stack(
        [np.stack([v0, v2, v1], axis=-1), np.stack([v1, v2, v3], axis=-1)],
        axis=1,
    ).reshape(-1, 3).astype(np.int64)

    return vertices, faces, colors


def write_obj(
    path: "os.PathLike[str] | str",
    vertices: np.ndarray,
    faces: np.ndarray,
    colors: Optional[np.ndarray] = None,
) -> None:
    """Write vertices/faces (and optional per-vertex colors) to a Wavefront .obj file."""
    with open(path, "w") as f:
        for i, v in enumerate(vertices):
            if colors is not None:
                r, g, b = colors[i]
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f} {r:.4f} {g:.4f} {b:.4f}\n")
            else:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for face in faces:
            # OBJ face indices are 1-based.
            f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")


def image_to_3d(
    image_path: "os.PathLike[str] | str",
    output_path: "os.PathLike[str] | str",
    model_name: str = DEFAULT_MODEL,
    depth_scale: float = 50.0,
    max_size: int = 256,
) -> str:
    """Convert a 2D image at image_path into a 3D mesh saved as an .obj file.

    Downscales the image to at most max_size on its longest side (a
    pixel-per-vertex grid mesh grows quadratically with resolution),
    estimates depth with an AI model, and writes a colored triangle mesh.
    Returns output_path as a string.
    """
    image = Image.open(image_path)
    image.thumbnail((max_size, max_size))
    image = image.convert("RGB")

    depth = estimate_depth(image, model_name=model_name)
    vertices, faces, colors = depth_to_mesh(depth, image=image, depth_scale=depth_scale)
    write_obj(output_path, vertices, faces, colors)
    return str(output_path)
