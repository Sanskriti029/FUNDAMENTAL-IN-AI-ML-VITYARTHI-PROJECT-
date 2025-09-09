def load_map(file_path):
    grid = {}
    start = goal = None
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    rows, cols = len(lines), len(lines[0])
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == 'S':
                start = (r, c)
                grid[(r, c)] = 1
            elif ch == 'G':
                goal = (r, c)
                grid[(r, c)] = 1
            elif ch == '.':
                grid[(r, c)] = 1
            elif ch.isdigit():
                grid[(r, c)] = int(ch)
            # '#' = obstacle, skip
    return grid, start, goal, rows, cols

def neighbors(pos, rows, cols):
    r, c = pos
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield (nr, nc)
