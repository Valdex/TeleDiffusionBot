import dataclasses


@dataclasses.dataclass
class Prompt:
    prompt: str
    negative_prompt: str = "blurry, ugly, low details, low quality, off-center character, out of frame"
    steps: int = 25
    cfg_scale: int = 3
    width: int = 512
    height: int = 512
    restore_faces: bool = False
    sampler: str = "Euler a"
    creator: int = None


@dataclasses.dataclass
class Generated:
    prompt: Prompt
    seed: int
    model: str
