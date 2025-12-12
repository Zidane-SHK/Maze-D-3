import math
import heapq

def get_euclidean_distance(node_a, node_b, coords):
    """
    Calculates the straight-line distance (in pixels) between two nodes.
    """
    if node_a not in coords or node_b not in coords:
        return float('inf')
    x1, y1 = coords[node_a]
    x2, y2 = coords[node_b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def get_distance_to_human_path(current_node, human_path_list, coords):
    """
    Returns 0 if the node is in the allowed path segment.
    Returns 5000 if it is a deviation, acting as a soft barrier.
    """
    if not human_path_list:
        return 0
    if current_node in human_path_list:
        return 0.0
    else:
        return 5000.0

def reconstruct_path(came_from, current):
    """
    Rebuilds the path from the 'came_from' dictionary.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def a_star_search(start_node, goal_node, graph, coords, human_path=None, forbidden_nodes=None):
    """
    Modified A* Search with Real Distance Costs and Safety Checks.
    """
    
    if forbidden_nodes is None:
        forbidden_nodes = set()

    open_set = []
    # Heap stores tuples of (f_score, node_id)
    heapq.heappush(open_set, (0, start_node))
    
    came_from = {}
    
    # Initialize scores to Infinity
    g_score = {node: float('inf') for node in coords}
    g_score[start_node] = 0
    
    f_score = {node: float('inf') for node in coords}
    
    # --- CONFIGURATION ---
    # Weight > 0 guides the pirate to follow the 'ideal' sequence 
    # to avoid burning bridges (like the 5->47 shortcut trap).
    HUMAN_BIAS_WEIGHT = 5.0
    
    # Initial Calculation
    h1 = 0 
    h2 = get_distance_to_human_path(start_node, human_path, coords)
    f_score[start_node] = h1 + (HUMAN_BIAS_WEIGHT * h2)

    open_set_hash = {start_node}

    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current not in open_set_hash:
            continue
        open_set_hash.remove(current)

        if current == goal_node:
            return reconstruct_path(came_from, current)

        if current in graph:
            for neighbor, weight in graph[current]:
                
                # --- CHECK 1: Prevent Immediate Backtracking ---
                # Do not immediately return to the node we just came from.
                if current in came_from and neighbor == came_from[current]:
                    continue

                # --- CHECK 2: Prevent Global Retracing (With Exception) ---
                # Check if this node is allowed by the current Human Path segment.
                is_in_human_segment = (human_path is not None) and (neighbor in human_path)
                
                # Block the node IF:
                # 1. It is in the forbidden list (visited previously).
                # 2. AND it is NOT the goal.
                # 3. AND it is NOT explicitly allowed by the current human segment.
                if neighbor in forbidden_nodes and neighbor != goal_node and not is_in_human_segment:
                    continue

                # --- 3. CALCULATE REAL DISTANCE COST (The Math Fix) ---
                # Instead of using the arbitrary graph weight (1), we calculate 
                # the actual pixel distance. This fixes the scaling issue where 
                # Heuristic (500px) overpowered Cost (1).
                dist_cost = get_euclidean_distance(current, neighbor, coords)
                
                # New G Score is current G + Actual Pixel Distance
                tentative_g_score = g_score[current] + dist_cost

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    
                    # --- 4. HEURISTIC TUNING ---
                    # H1: Euclidean Distance to Goal (in pixels)
                    h1_goal = get_euclidean_distance(neighbor, goal_node, coords)
                    
                    # H2: Human Bias (Soft Lock to path)
                    h2_human = get_distance_to_human_path(neighbor, human_path, coords)
                    
                    # Total Score
                    f_score[neighbor] = tentative_g_score + h1_goal + (HUMAN_BIAS_WEIGHT * h2_human)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

    print(f"No path found from {start_node} to {goal_node}")
    return []