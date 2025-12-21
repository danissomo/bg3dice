from PIL import Image
import random
from pathlib import Path
from typing import List, Tuple
import time
from argparse import ArgumentParser
from os.path import dirname, join as joinpath
DATADIR = Path(dirname(__file__))
def _gen_between_points(start, end, num_points):
    """Генерирует список точек между start и end."""
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x = start[0] + t * (end[0] - start[0])
        y = start[1] + t * (end[1] - start[1])
        points.append((x, y))
    return points


class SpriteSheet:
    def __init__(self, image_path: str | Path, rows: int, cols: int):
        self.image = Image.open(image_path)
        self.rows = rows
        self.cols = cols
        self.frame_width = self.image.width // cols
        self.frame_height = self.image.height // rows
        self.frames = []
        for r in range(rows):
            for c in range(cols):
                frame = self.image.crop((
                    c * self.frame_width,
                    r * self.frame_height,
                    (c + 1) * self.frame_width,
                    (r + 1) * self.frame_height
                ))
                self.frames.append(frame)

    def get_frame(self, index: int) -> Image.Image:
        return self.frames[index % len(self.frames)]


class SpriteRenderer:
    def __init__(self, sprite: SpriteSheet, start: int, end: int | None = None):
        self.sprite = sprite
        self.start = start
        if end is None:
            self.end = start + len(sprite.frames) - 1
        else:
            self.end = end

    def render_frame(self, iframe: int, canvas: Image.Image, position: Tuple[float, float] = (0, 0)) -> Image.Image:
        canvas = canvas.copy()
        if self.start <= iframe < self.end:
            cur = self.sprite.get_frame(iframe - self.start)
            p_pixel = (int(position[0] * canvas.width) - cur.width //
                       2, int(position[1] * canvas.height) - cur.height // 2)
            canvas.paste(cur, p_pixel, cur)
        return canvas


class SpriteRendererMove(SpriteRenderer):
    def __init__(self, sprite: SpriteSheet, start, rel_points: List[Tuple[int, int]], frames_bw_points: List[int] = []):
        end = start + sum(frames_bw_points) - len(rel_points) + 1
        super().__init__(sprite, start, end)
        self.points = []
        for i, count in enumerate(frames_bw_points):
            p_start = rel_points[i]
            p_end = rel_points[i + 1]
            between_points = _gen_between_points(p_start, p_end, count)
            # исключаем последнюю точку, чтобы не дублировать
            self.points += between_points[:-1]
        self.points.append(rel_points[-1])  # добавляем последнюю точку

    def render_frame(self, iframe, canvas, position=(0, 0)):
        canvas = canvas.copy()
        if self.start <= iframe < self.end:
            p = self.points[iframe - self.start]
            return super().render_frame(iframe, canvas, p)
        return canvas


class StaticSpriteRenderer(SpriteRenderer):
    def __init__(self, sprite: SpriteSheet, start, end, frame_index):
        super().__init__(sprite, start, end)
        self.frame_index = frame_index

    def render_frame(self, iframe, canvas, position):
        if self.start <= iframe < self.end:
            return super().render_frame(self.start + self.frame_index, canvas, position)
        return canvas


class RotatedSpriteRenderer(SpriteRenderer):
    def __init__(self, sprite: SpriteSheet, start: int, end: int | None = None, angle=0, flip=False):
        super().__init__(sprite, start, end)
        self.angle = angle
        self.flip = flip

    def render_frame(self, iframe: int, canvas: Image.Image, position) -> Image.Image:
        canvas = canvas.copy()
        if self.start <= iframe < self.end:
            cur = self.sprite.get_frame(iframe - self.start)
            if self.flip:
                cur = cur.transpose(Image.FLIP_TOP_BOTTOM)
            cur = cur.rotate(self.angle, expand=True)
            p_pixel = (int(position[0] * canvas.width) - cur.width //
                       2, int(position[1] * canvas.height) - cur.height // 2)
            canvas.paste(cur, p_pixel, cur)
        return canvas


def render_animation(n : int | None = None) -> Tuple[List[Image.Image], int]:
    """
    Generates an animation sequence for a dice roll, including various visual effects.
    Args:
        n (int | None, optional): The result of the dice roll. If None, a random value 
            between 0 and 19 is generated. Defaults to None.
    Returns:
        Tuple[List[Image.Image], int]: A tuple containing:
            - A list of PIL Image objects representing the frames of the animation.
            - The dice roll result (either the provided `n` or the randomly generated value).
    Notes:
        - The function uses several sprite sheets to render different visual effects, 
          such as dice rolling, explosions, and shines.
        - The animation consists of 128 frames.
        - The background image is loaded from the "roll_frame.png" asset.
        - The function relies on external classes like `SpriteSheet`, `SpriteRendererMove`, 
          `StaticSpriteRenderer`, `SpriteRenderer`, and `RotatedSpriteRenderer` for rendering.
    """
    
    if n is None:
        random.seed(time.time())
        n = random.randint(0, 19)
    s_dice_roll = SpriteSheet(DATADIR/ "assets/single_roll.png", 8, 8)
    s_dice = SpriteSheet(DATADIR/ "assets/d20.png", 5, 5)
    s_dice_explosion = SpriteSheet(DATADIR/ "assets/popExplosion.png", 4, 4)
    s_dice_shine = SpriteSheet(DATADIR/ "assets/d20Shine.png", 5, 6)
    s_dice_hit = SpriteSheet(DATADIR/ "assets/d20Explosion.png", 6, 6)
    s_dice_roll_renderer = SpriteRendererMove(s_dice_roll, 0,
                                              [
                                                  (0.5, 0.5),
                                                  (0.2, 0.7),
                                                  (0.3, 0.8),
                                                  (0.8, 0.5),
                                                  (0.3, 0.2),
                                                  (0.2, 0.3),
                                                  (0.5, 0.5)
                                              ],
                                              [7, 5, 14, 15, 8, 14]
                                              )
    s_dice_renderer = StaticSpriteRenderer(
        s_dice, s_dice_roll_renderer.end, 128, n)
    s_dice_explosion_renderer = SpriteRenderer(
        s_dice_explosion, s_dice_roll_renderer.end - 1)
    s_dice_shine_renderer = SpriteRenderer(
        s_dice_shine, s_dice_roll_renderer.end)

    s_dice_hit_left_renderer = RotatedSpriteRenderer(
        s_dice_hit, 7-1, None, angle=0, flip=True)
    s_dice_hit_right_renderer = RotatedSpriteRenderer(
        s_dice_hit, 7+5+14-1, None, angle=180-45, flip=True)
    s_dice_hit_top_renderer = RotatedSpriteRenderer(
        s_dice_hit, 7+5+14+15-1, None, angle=-90, flip=True)

    bg = Image.open(DATADIR/ "assets/roll_frame.png")

    result_frames = []
    for i in range(128):
        frame = bg.copy()
        frame = s_dice_hit_left_renderer.render_frame(i, frame, (0.15, 0.85))
        frame = s_dice_hit_right_renderer.render_frame(i, frame, (0.83, 0.48))
        frame = s_dice_hit_top_renderer.render_frame(i, frame, (0.15, 0.17))
        frame = s_dice_roll_renderer.render_frame(i, frame)
        frame = s_dice_renderer.render_frame(i, frame, (0.5, 0.5))
        frame = s_dice_explosion_renderer.render_frame(i, frame, (0.5, 0.45))
        frame = s_dice_shine_renderer.render_frame(i, frame, (0.5, 0.5))
        result_frames.append(frame)
    return (result_frames, n)


def save_animation(result_frames: List[Image.Image], output_gif: str):
    """
    Saves a sequence of image frames as an animated GIF.
    Args:
        result_frames (List[Image.Image]): A list of PIL Image objects representing the frames of the animation.
        output_gif (str): The file path where the animated GIF will be saved.
    The first frame in the `result_frames` list is used as the base frame, and the remaining frames are appended to it.
    The animation loops infinitely and each frame is displayed for 32 milliseconds.
    """
    
    result_frames[0].save(
        output_gif,
        save_all=True,
        append_images=result_frames[1:],
        loop=0,
        duration=32
    )

def _parse_args():
    parser = ArgumentParser(description="Render a BG3 dice roll animation.")
    parser.add_argument(
        "-n", "--number",
        type=int,
        choices=range(0, 20),
        help="The dice number to roll (0-19). If not provided, a random number will be chosen."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.gif",
        help="The output GIF file name. Default is 'output.gif'."
    )
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="If set, suppresses console output.",
        default=False
    )
    return parser.parse_args()

def main():
    args = _parse_args()
    frames, n = render_animation(args.number)
    save_animation(frames, args.output)
    if not args.silent:
        print(f"Dice roll animation saved to {args.output} with number {n + 1}.")
    
if __name__ == "__main__":
    main()