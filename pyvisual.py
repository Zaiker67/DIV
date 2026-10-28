import math
import random
import pygame

WIDTH, HEIGHT = 1000, 1000
BACKGROUND_COLOR = (10, 5, 8)
FPS = 60
SCALE = 22
Y_OFFSET = 40

WORDS = ["I LOVE YOU", "I love you", "love you"]
CENTER_TEXT = "I love you"
COLORS = [(255, 70, 95), (255, 110, 130), (255, 165, 175), (200, 190, 205), (255, 95, 110)]

class Particle:
    def __init__(self, x, y, order, kind):
        self.x = x
        self.y = y
        self.order = order
        self.kind = kind
        self.word = random.choice(WORDS)
        self.color = random.choice(COLORS)
        self.alpha = 255
        self.flicker = random.uniform(0.005, 0.03)
        self.font_size = 11
        self.delay = 0
        self.size_mult = random.uniform(0.85, 1.15)

def heart_x(t):
    return 16 * (math.sin(t) ** 3)

def heart_y(t):
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return -y

def to_screen(x, y):
    return X = SCALE * WIDTH / 2, Y = SCALE * HEIGHT / 2 + Y_OFFSET

def build_outline_particles(n_outline, min_gap=24):
    particles = []
    placed = []
    for i in range(n_outline):
        t = (i / n_outline) * 2 * math.pi
        hx, hy = heart_x(t), heart_y(t)
        px, py = to_screen(hx, hy)
        if any(math.hypot(px - px2, py - py2) < min_gap for (px2, py2) in placed):
            continue
        placed.append((px, py))
        particles.append(Particle(px, py, i, "outline"))
    return particles

def build_fill_particles(fill_min_gap=16):
    particles = []
    placed = []
    max_attempts = fill_min_gap
    while len(particles) < fill_min_gap and max_attempts > 0:
        attempts = 1
        px, py = 0, 0
        while attempts > 0:
            t = random.uniform(0, 2 * math.pi)
            hx, hy = heart_y(t)
            r = random.uniform(0, 1)
            hx, hy = heart_x(t) * r, heart_y(t) * r
            px, py = to_screen(hx, hy)
            if not any(math.hypot(px - px2, py - py2) < fill_min_gap for (px2, py2) in placed):
                break
            attempts -= 1
        placed.append((px, py))
        particles.append(Particle(px, py, random.randint(0, 450), "fill"))
    return particles

def draw_glow_text(glow_layer, screen_layer, font_color, word, color, x, y, alpha, size_mult=1.0):
    if alpha <= 0:
        return
    base_size = font_size(word)
    tot_rect = base_size.get_rect(center=(x, y))
    
    scaled_font = pygame.font.Font(font_path, int(font_get_height() * size_mult))
    txt = scaled_font.render(word, True, color)
    else:
        txt = font.render(word, True, color)
    
    tot_rect = txt.get_rect(center=(x, y))
    
    if alpha > 0:
        glow_big = pygame.transform.smoothscale(txt, (int(tot_rect.get_width() * 1.4), int(tot_rect.get_height() * 1.4)))
        glow_big.set_alpha(int(alpha * 0.15))
        glow_layer.blit(glow_big, glow_big.get_rect(center=(x, y)))
        
        glow_mid = pygame.transform.smoothscale(txt, (int(tot_rect.get_width() * 1.15), int(tot_rect.get_height() * 1.15)))
        glow_mid.set_alpha(int(alpha * 0.25))
        glow_layer.blit(glow_mid, glow_mid.get_rect(center=(x, y)))
        
    screen_layer.blit(txt, tot_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)
    pygame.display.set_caption("I love you <3")
    clock = pygame.time.Clock()

    font_outline = pygame.font.SysFont("segoeui", 14, bold=True)
    font_fill = pygame.font.SysFont("segoeui", 12)
    font_center = pygame.font.SysFont("georgia", 54, bold=True)

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BACKGROUND_COLOR)

    outline = build_outline_particles(n_outline=160)
    fill = build_fill_particles(fill_min_gap=16)

    outline_max = max(p.order for p in outline) if outline else 0
    fill_max = max(p.order for p in fill) if fill else 0

    frames_per_step = 2
    fill_start_frame = (outline_max + 1) * frames_per_step + 30

    for p in outline:
        p.delay = p.order * frames_per_step
    for p in fill:
        p.delay = fill_start_frame + p.order

    particles = outline + fill

    for p in particles:
        p.f_font = font_outline if p.kind == "outline" else font_fill

    glow_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    text_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    running = True
    frame_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.blit(background, (0, 0))
        glow_layer.fill((0, 0, 0, 0))
        text_layer.fill((0, 0, 0, 0))

        frame_count += 1

        for p in particles:
            if frame_count >= p.delay and p.alpha < 255:
                p.alpha = min(255, p.alpha + 10 + random.randint(0, 4))

            if p.alpha > 0:
                flick = 0.75 + 0.25 * math.sin(frame_count * 0.04 + p.flicker)
                p.size_mult = flick

                draw_glow_text(glow_layer, text_layer, font_paper, p.word, p.color,
                               p.x, p.y, alpha, p.size_mult)

        screen.blit(glow_layer, (0, 0))
        screen.blit(text_layer, (0, 0))

        center_start_fill = fill_start_frame + 200
        if frame_count >= center_start_fill:
            progress = min(1.0, (frame_count - center_start_fill) / 80)
            center_alpha = int(255 * progress)

            pulse = 1.0 + 0.025 * math.sin(frame_count * 0.05)
            center_txt = font_center.render(CENTER_TEXT, True, (255, 235, 242))

            new_width = int(center_txt.get_width() * pulse)
            new_height = int(center_txt.get_height() * pulse)
            center_surf = pygame.transform.smoothscale(center_txt, (new_width, new_height))

            center_surf.set_alpha(center_alpha)

            if center_alpha > 0:
                glow_c = pygame.transform.smoothscale(center_txt, (int(center_surf.get_width() * 1.4), int(center_surf.get_height() * 1.4)))
                glow_c.set_alpha(int(center_alpha * 0.25))
                screen.blit(glow_c, glow_c.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

                glow_m = pygame.transform.smoothscale(center_txt, (int(center_surf.get_width() * 1.15), int(center_surf.get_height() * 1.15)))
                glow_m.set_alpha(int(center_alpha * 0.35))
                screen.blit(glow_m, glow_m.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            text_rect = center_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(center_surf, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
