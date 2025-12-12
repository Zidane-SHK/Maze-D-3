import pygame
import sys
import time

# Import configurations
# IMPORTANT: Added HUMAN_PATHS to the import
from config import GRAPH as ADJACENCY_LIST, COORDS as NODES, START_NODE, MISSION_CHECKPOINTS, HUMAN_PATHS, CANNON_NODES, FINISH_NODE
from vis import Visualizer
from algo import a_star_search

FPS = 60
MOVE_DELAY = 500

def solve_mission():
    full_path = []
    current_start = START_NODE
    cannons_loaded = [] 
    
    global_visited = set()
    global_visited.add(START_NODE)

    print(".....Starting Mission calculations.....")

    for target in MISSION_CHECKPOINTS:
        if target == FINISH_NODE and len(cannons_loaded) < 4:
            print(f"Wait! Only {len(cannons_loaded)}/4 cannons loaded.")

        print(f"Calculating segment: {current_start} -> {target}")

        # --- PATH LOOKUP LOGIC ---
        # Look up the allowed path in the dictionary using the start node
        allowed_segment = []
        
        if current_start in HUMAN_PATHS:
            allowed_segment = HUMAN_PATHS[current_start]
            print(f"   > Guided Path Active: {len(allowed_segment)} steps enforced.")
        else:
            print(f"   > Warning: No specific path defined for start node {current_start}.")

        # --- EXECUTE SEARCH ---
        segment_path = a_star_search(
            start_node=current_start, 
            goal_node=target, 
            graph=ADJACENCY_LIST, 
            coords=NODES, 
            human_path=allowed_segment, 
            forbidden_nodes=global_visited
        )

        if not segment_path:
            print(f"CRITICAL ERROR: No path to {target}. The pirate is stuck!")
            # Teleport to target to prevent crash, but this means game logic failed
            segment_path = [current_start, target]
        
        # --- UPDATE GAME STATE ---
        if target in CANNON_NODES:
            if target not in cannons_loaded:
                cannons_loaded.append(target)
                print(f"*** Cannon Loaded! Total: {len(cannons_loaded)}/4 ***")

        for node in segment_path:
            global_visited.add(node)

        if full_path:
            full_path.extend(segment_path[1:])
        else:
            full_path.extend(segment_path)

        current_start = target

    print(".....Mission calculated succesfully.....")
    return full_path

def main():
    pygame.init()
    viz = Visualizer()
    clock = pygame.time.Clock()

    calculated_path = solve_mission()

    path_index = 0
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    path_index = 0

        if calculated_path and path_index < len(calculated_path) - 1:
            if current_time - last_move_time > MOVE_DELAY:
                path_index += 1
                last_move_time = current_time

        current_node_id = calculated_path[path_index] if calculated_path else START_NODE

        viz.draw_background()
        viz.draw_graph(NODES, ADJACENCY_LIST)
        viz.draw_path_line(calculated_path, NODES)
        viz.draw_player(current_node_id, NODES)

        pygame.display.flip()
        clock.tick(FPS)

    viz.save_image("final_solution.png")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()