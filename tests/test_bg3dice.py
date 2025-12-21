import pytest
from PIL import Image
from bg3dice.bg3dice import SpriteSheet, SpriteRenderer, SpriteRendererMove, StaticSpriteRenderer, RotatedSpriteRenderer, render_animation, save_animation
from pathlib import Path

DATADIR = Path(__file__).parent / "../src/bg3dice/assets"

@pytest.fixture
def sprite_sheet():
    return SpriteSheet(DATADIR / "d20.png", 5, 5)

def test_sprite_sheet_initialization(sprite_sheet):
    assert sprite_sheet.rows == 5
    assert sprite_sheet.cols == 5
    assert len(sprite_sheet.frames) == 25

def test_get_frame(sprite_sheet):
    frame = sprite_sheet.get_frame(0)
    assert isinstance(frame, Image.Image)

def test_sprite_renderer_render_frame(sprite_sheet):
    renderer = SpriteRenderer(sprite_sheet, start=0, end=10)
    canvas = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    frame = renderer.render_frame(0, canvas)
    assert isinstance(frame, Image.Image)

def test_sprite_renderer_move_render_frame(sprite_sheet):
    renderer = SpriteRendererMove(sprite_sheet, start=0, rel_points=[(0, 0), (1, 1)], frames_bw_points=[5])
    canvas = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    frame = renderer.render_frame(0, canvas)
    assert isinstance(frame, Image.Image)

def test_static_sprite_renderer_render_frame(sprite_sheet):
    renderer = StaticSpriteRenderer(sprite_sheet, start=0, end=10, frame_index=2)
    canvas = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    frame = renderer.render_frame(0, canvas, (0.5, 0.5))
    assert isinstance(frame, Image.Image)

def test_rotated_sprite_renderer_render_frame(sprite_sheet):
    renderer = RotatedSpriteRenderer(sprite_sheet, start=0, end=10, angle=45, flip=True)
    canvas = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    frame = renderer.render_frame(0, canvas, (0.5, 0.5))
    assert isinstance(frame, Image.Image)

def test_render_animation():
    frames, n = render_animation(5)
    assert len(frames) == 128
    assert isinstance(frames[0], Image.Image)
    assert 0 <= n <= 19

def test_save_animation(tmp_path):
    frames, _ = render_animation(5)
    output_gif = tmp_path / "output.gif"
    save_animation(frames, output_gif)
    assert output_gif.exists()