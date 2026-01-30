import pygame
import sys
import time
import json

# 配置同前，增加动画逻辑
TILE = 80
ANIM_SPEED = 0.2 # 越小越丝滑

class SokobanGame:
    def __init__(self):
        pygame.init()
        # 预加载关卡（若无json则报错）
        with open("levels.json", "r") as f: self.level_pool = json.load(f)
        self.queue = random.sample(self.level_pool, 12)
        
        self.screen = pygame.display.set_mode((TILE*7, TILE*7 + 100))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.lv_idx = 0
        self.total_resets = 0
        self.start_time = time.time()
        self.load_current_level()

    def load_current_level(self):
        data = self.queue[self.lv_idx]
        self.walls = data['walls']
        self.targets = data['targets']
        self.init_p = data['player']
        self.init_b = data['boxes']
        self.reset_level(False)

    def reset_level(self, manual=True):
        self.p_pos = list(self.init_p)
        self.p_real = [self.p_pos[0]*TILE, self.p_pos[1]*TILE]
        self.b_list = [{"grid": list(b), "real": [b[0]*TILE, b[1]*TILE]} for b in self.init_b]
        if manual: self.total_resets += 1

    def draw(self):
        self.screen.fill((240, 240, 240))
        # 绘制墙体、目标、平滑移动的玩家和箱子... (逻辑参考前述 Lerp 算法)
        # 底部显示: Time + (Resets * 10)
        penalty_time = int(time.time() - self.start_time) + self.total_resets * 10
        txt = self.font.render(f"Level: {self.lv_idx+1}/12  Score Time: {penalty_time}s", True, (50,50,50))
        self.screen.blit(txt, (20, 7*TILE + 20))

    # ... 此处包含 move 逻辑 ...