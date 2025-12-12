import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        pygame.display.set_caption("Cannon Challenge Visualization")
        
        self.WHITE = (255, 255, 255)
        self.GREY = (200, 200, 200)
        
        self.PATH_COLORS = [
            (0, 0, 0),       # Black
            (0, 0, 255),     # Blue
            (255, 20, 147),  # Deep Pink
            (50, 205, 50)    # Lime Green
        ]
        
        # Switch colors at the end of each path segment (The Cannons)
        self.SWITCH_NODES = {'16', '24', '8'}
        
        # Load Background
        self.bg_image = None
        image_path = r'/Users/zidanekhan/Downloads/Maze D-3/bg.jpeg'
        try:
            raw_image = pygame.image.load(image_path)
            self.bg_image = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print(f"ERROR: Image not found at {image_path}.")
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill(self.WHITE)

        # Load Icon
        self.player_icon = None
        icon_path = r'/Users/zidanekhan/Downloads/Maze D-3/icon.png'  
        try:
            raw_icon = pygame.image.load(icon_path)
            # Resize icon for new screen size
            self.player_icon = pygame.transform.scale(raw_icon, (60, 60))
        except FileNotFoundError:
            print(f"ERROR: Pirate icon not found at {icon_path}.")
            self.player_icon = None

    def draw_background(self):
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))

    def draw_graph(self, nodes, adjacency_list):
        for node_id, neighbors in adjacency_list.items():
            if node_id in nodes:
                start_pos = nodes[node_id]
                for neighbor_info in neighbors:
                    neighbor_id = neighbor_info[0]
                    if neighbor_id in nodes:
                        end_pos = nodes[neighbor_id]
                        pygame.draw.line(self.screen, self.GREY, start_pos, end_pos, 2)
                        
        for pos in nodes.values():
            pygame.draw.circle(self.screen, self.WHITE, pos, 3)

    def draw_path_line(self, full_path, nodes_dict):
        if not full_path or len(full_path) < 2:
            return

        current_color_idx = 0
        for i in range(len(full_path) - 1):
            node_a = full_path[i]
            node_b = full_path[i+1]

            if node_a in nodes_dict and node_b in nodes_dict:
                p1 = nodes_dict[node_a]
                p2 = nodes_dict[node_b]

                color = self.PATH_COLORS[current_color_idx % len(self.PATH_COLORS)]

                pygame.draw.line(self.screen, color, p1, p2, width=6)
                pygame.draw.circle(self.screen, color, p1, 3)

                if node_b in self.SWITCH_NODES:
                    current_color_idx += 1

    def draw_player(self, current_node_id, nodes):
        if current_node_id in nodes:
            x, y = nodes[current_node_id]
            
            if self.player_icon:
                icon_rect = self.player_icon.get_rect(center=(x, y))
                self.screen.blit(self.player_icon, icon_rect)
            else:
                pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 14, 0)
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 8, 0)
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 8, 2)

    def save_image(self, filename="saved.png"):
        pygame.image.save(self.screen, filename)
        print(f"Image saved to {filename}")