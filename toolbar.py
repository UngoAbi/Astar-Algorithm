from enum import Enum
import pygame
from consts import TOOL_SIZE


class ToolType(Enum):
    START = pygame.transform.scale(pygame.image.load("assets/start.png"), (TOOL_SIZE, TOOL_SIZE))
    TARGET = pygame.transform.scale(pygame.image.load("assets/target.png"), (TOOL_SIZE, TOOL_SIZE))
    WALL = pygame.transform.scale(pygame.image.load("assets/wall.png"), (TOOL_SIZE, TOOL_SIZE))
    ERASE = pygame.transform.scale(pygame.image.load("assets/erase.png"), (TOOL_SIZE, TOOL_SIZE))
    RESET = pygame.transform.scale(pygame.image.load("assets/reset.png"), (TOOL_SIZE, TOOL_SIZE))
    CLEAR = pygame.transform.scale(pygame.image.load("assets/clear.png"), (TOOL_SIZE, TOOL_SIZE))
    PAUSE = pygame.transform.scale(pygame.image.load("assets/pause.png"), (TOOL_SIZE, TOOL_SIZE))
    PLAY = pygame.transform.scale(pygame.image.load("assets/play.png"), (TOOL_SIZE, TOOL_SIZE))


class Tool:
    def __init__(self, position: tuple[int, int], tool_type: ToolType) -> None:
        self.position = position
        self.type = tool_type
        self.rect = pygame.Rect(position, (TOOL_SIZE, TOOL_SIZE))


class ToolBar:
    def __init__(self) -> None:
        self.tools = [Tool((i * TOOL_SIZE, 800), tool_type) for i, tool_type in enumerate(ToolType)]
        self.current_tool = self.tools[3]
        self.frame = pygame.transform.scale(pygame.image.load("assets/frame.png"), (TOOL_SIZE, TOOL_SIZE))

    def get_clicked_tool(self, mouse_pos: tuple[int, int]) -> Tool | None:
        for tool in self.tools:
            if tool.rect.collidepoint(*mouse_pos):
                return tool
