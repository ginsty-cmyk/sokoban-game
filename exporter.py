import json
import random
import collections
import os

class LevelExporter:
    def __init__(self, size=7):
        self.size = size

    def is_deadlock(self, bx, by, walls, target_set):
        """核心修复：严格判定死锁，防止生成开局即死的关卡"""
        if (bx, by) in target_set: return False
        # 墙角检测
        u = walls[by-1][bx] == 1
        d = walls[by+1][bx] == 1
        l = walls[by][bx-1] == 1
        r = walls[by][bx+1] == 1
        if (u and l) or (u and r) or (d and l) or (d and r): return True
        return False

    def solve(self, p, b, w, t):
        """BFS 求解并验证路径"""
        start_state = (tuple(p), tuple(sorted(tuple(x) for x in b)))
        queue = collections.deque([(start_state, 0)])
        visited = {start_state}
        t_set = set(tuple(x) for x in t)

        while queue:
            (curr_p, curr_b), dist = queue.popleft()
            if set(curr_b) == t_set: return dist
            if dist > 60: continue

            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = curr_p[0]+dx, curr_p[1]+dy
                if w[ny][nx] == 1: continue
                if (nx, ny) in curr_b:
                    bx, by = nx+dx, ny+dy
                    if w[by][bx] == 0 and (bx, by) not in curr_b:
                        # 模拟推箱子时，如果推入死角则舍弃该路径
                        if not self.is_deadlock(bx, by, w, t_set):
                            nb = tuple(sorted([pos if pos != (nx, ny) else (bx, by) for pos in curr_b]))
                            if ((nx, ny), nb) not in visited:
                                visited.add(((nx, ny), nb)); queue.append((((nx, ny), nb), dist+1))
                else:
                    if ((nx, ny), curr_b) not in visited:
                        visited.add(((nx, ny), curr_b)); queue.append((((nx, ny), curr_b), dist+1))
        return None

    def run_export(self, count=300):
        levels = []
        seen = set()
        print(f"正在孵化 {count} 个精选关卡，请稍候...")
        
        while len(levels) < count:
            walls = [[1]*self.size for _ in range(self.size)]
            for y in range(1, self.size-1):
                for x in range(1, self.size-1):
                    if random.random() > 0.25: walls[y][x] = 0
            
            empty = [(x,y) for y in range(1, self.size-1) for x in range(1, self.size-1) if walls[y][x]==0]
            if len(empty) < 6: continue
            random.shuffle(empty)
            t, b, p = empty[:2], [list(x) for x in empty[2:4]], empty[4]

            # 初始状态就死锁的直接排除
            if any(self.is_deadlock(bx, by, walls, set(tuple(x) for x in t)) for bx, by in b): continue

            dist = self.solve(p, b, walls, t)
            if dist and dist >= 12:
                m_hash = hash(str(walls)+str(t))
                if m_hash not in seen:
                    levels.append({"walls": walls, "player": p, "boxes": b, "targets": t, "min": dist})
                    seen.add(m_hash)
                    if len(levels) % 10 == 0: print(f"进度: {len(levels)}/{count}")

        with open("levels.json", "w") as f:
            json.dump(levels, f)
        print("成功生成 levels.json！")

if __name__ == "__main__":
    LevelExporter().run_export(300)