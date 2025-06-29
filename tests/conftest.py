"""Shared pytest fixtures and configuration for testing BlenderToolbox."""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files.
    
    Yields:
        Path: Path to the temporary directory.
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup after test
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def mock_blend_file(temp_dir: Path) -> Path:
    """Create a mock .blend file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the mock .blend file.
    """
    blend_file = temp_dir / "test.blend"
    blend_file.write_bytes(b"BLENDER")  # Mock Blender file header
    return blend_file


@pytest.fixture
def mock_obj_file(temp_dir: Path) -> Path:
    """Create a mock .obj file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the mock .obj file.
    """
    obj_file = temp_dir / "test.obj"
    obj_content = """# Mock OBJ file
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.0 1.0 0.0
f 1 2 3
"""
    obj_file.write_text(obj_content)
    return obj_file


@pytest.fixture
def mock_ply_file(temp_dir: Path) -> Path:
    """Create a mock .ply file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the mock .ply file.
    """
    ply_file = temp_dir / "test.ply"
    ply_content = """ply
format ascii 1.0
element vertex 3
property float x
property float y
property float z
element face 1
property list uchar int vertex_indices
end_header
0.0 0.0 0.0
1.0 0.0 0.0
0.0 1.0 0.0
3 0 1 2
"""
    ply_file.write_text(ply_content)
    return ply_file


@pytest.fixture
def mock_stl_file(temp_dir: Path) -> Path:
    """Create a mock .stl file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the mock .stl file.
    """
    stl_file = temp_dir / "test.stl"
    stl_content = """solid test
  facet normal 0 0 0
    outer loop
      vertex 0 0 0
      vertex 1 0 0
      vertex 0 1 0
    endloop
  endfacet
endsolid test
"""
    stl_file.write_text(stl_content)
    return stl_file


@pytest.fixture
def mock_image_file(temp_dir: Path) -> Path:
    """Create a mock image file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the mock image file.
    """
    image_file = temp_dir / "test.png"
    # Create a minimal PNG header
    png_header = b'\x89PNG\r\n\x1a\n'
    image_file.write_bytes(png_header)
    return image_file


@pytest.fixture
def mock_numpy_data(temp_dir: Path) -> Path:
    """Create a mock numpy data file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the mock numpy file.
    """
    try:
        import numpy as np
        npy_file = temp_dir / "test_data.npy"
        data = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
        np.save(npy_file, data)
        return npy_file
    except ImportError:
        # Create a dummy file if numpy is not available
        npy_file = temp_dir / "test_data.npy"
        npy_file.write_bytes(b"NUMPY")
        return npy_file


@pytest.fixture
def mock_config() -> dict:
    """Provide mock configuration for testing.
    
    Returns:
        dict: Mock configuration dictionary.
    """
    return {
        "camera": {
            "location": (7.36, -6.93, 4.96),
            "rotation": (63.6, 0, 46.7),
            "fov": 50
        },
        "light": {
            "type": "sun",
            "location": (5, 5, 5),
            "energy": 1.0
        },
        "render": {
            "resolution_x": 1920,
            "resolution_y": 1080,
            "samples": 128
        }
    }


@pytest.fixture(autouse=True)
def isolate_environment(monkeypatch):
    """Isolate test environment from system environment.
    
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    # Clear potentially interfering environment variables
    env_vars_to_clear = [
        "BLENDER_PATH",
        "BLENDER_VERSION",
        "BLENDERTOOLBOX_CONFIG"
    ]
    for var in env_vars_to_clear:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def capture_logs(caplog):
    """Capture and provide access to log messages during tests.
    
    Args:
        caplog: pytest caplog fixture.
        
    Returns:
        caplog: The caplog fixture for log inspection.
    """
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog


# Add markers for test organization
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions and methods"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for module interactions"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take significant time to run"
    )
    config.addinivalue_line(
        "markers", "requires_blender: Tests that require Blender to be installed"
    )