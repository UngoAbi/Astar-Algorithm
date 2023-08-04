import sys
import pygame
from consts import *
from grid import GridState, Grid, NodeType
from toolbar import ToolBar, ToolType


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("A* Pathfinding Algorithm")
pygame.display.set_icon(ToolType.TARGET.value)


def main() -> None:
    grid = Grid()
    toolbar = ToolBar()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                use_tool(toolbar, grid)
            if pygame.mouse.get_pressed()[0]:
                update_grid(toolbar, grid)

        if grid.path:
            grid.reveal_path()
        elif grid.state is GridState.RUNNING:
            grid.find_path()

        draw_grid(grid)
        draw_toolbar(toolbar)

        pygame.display.update()
        clock.tick(FPS)


def use_tool(toolbar: ToolBar, grid: Grid) -> None:
    mouse_position = pygame.mouse.get_pos()
    if (clicked_tool := toolbar.get_clicked_tool(mouse_position)) is None:
        return

    toolbar.current_tool = clicked_tool
    match toolbar.current_tool.type:
        case ToolType.RESET:
            grid.reset()
        case ToolType.CLEAR:
            grid.clear()
        case ToolType.PAUSE:
            grid.state = GridState.IDLE
        case ToolType.PLAY:
            grid.state = GridState.RUNNING


def update_grid(toolbar: ToolBar, grid: Grid) -> None:
    mouse_pos = pygame.mouse.get_pos()
    if (clicked_cell := grid.get_clicked_cell(mouse_pos)) is None:
        return

    match toolbar.current_tool.type:
        case ToolType.ERASE:
            if clicked_cell.type == NodeType.WALL:
                clicked_cell.type = NodeType.DEFAULT
        case ToolType.WALL:
            if clicked_cell.type == NodeType.DEFAULT:
                clicked_cell.type = NodeType.WALL

        case ToolType.START:
            if clicked_cell.type in [NodeType.DEFAULT, NodeType.WALL]:
                grid.start_node.type = NodeType.DEFAULT
                grid.start_node = clicked_cell
                grid.start_node.type = NodeType.START
        case ToolType.TARGET:
            if clicked_cell.type in [NodeType.DEFAULT, NodeType.WALL]:
                grid.target_node.type = NodeType.DEFAULT
                grid.target_node = clicked_cell
                grid.target_node.type = NodeType.TARGET


def draw_grid(grid: Grid) -> None:
    for y, row in enumerate(grid.matrix):
        for x, node in enumerate(row):
            screen.blit(node.type.value, (x * NODE_SIZE, y * NODE_SIZE))



def draw_toolbar(toolbar: ToolBar) -> None:
    for tool in toolbar.tools:
        screen.blit(tool.type.value, tool.position)
    screen.blit(toolbar.frame, toolbar.current_tool.position)


if __name__ == "__main__":
    main()
