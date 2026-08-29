import time
import math
import pygame
import random
from subprocess import call
from constants import *

WIN = pygame.display.set_mode((GAMEWITH, GAMEHEIGHT))
pygame.display.set_caption("Firework Animation")
pygame.init()


def generate_projectiles_number(min, max):
    projectiles = random.randint(a=min, b=max)
    return projectiles


# creates just one Object of a Projectile (more needs to be created in Firework)
class Projectile:  # don't need Projectile Number here
    PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 7, 13
    FADING_DECREMENT = 3  # the reason, that the projectiles fade in the distance

    def __init__(self, x, y, x_vel, y_vel, color):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.fading_alpha = 255

    def spread(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.fading_alpha = max(0, self.fading_alpha - self.FADING_DECREMENT)

    def draw_prjectile(self, win):
        # pygame.draw.rect(SURFACE, RGB_COLOR, (X, Y, WIDTH, HEIGHT))
        self.draw_rect_alpha(
            win,
            self.color + (self.fading_alpha,),
            (self.x, self.y, self.PROJECTILE_WIDTH, self.PROJECTILE_HEIGHT),
        )

    @staticmethod
    def draw_rect_alpha(surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)


class Firework:  # creates the Projectiles
    RADIUS = 10  # pixels
    MAX_PROJECTILE_NUMB = 50
    MIN_PROJECTILE_NUMB = 20
    PROJECTILE_VEL = 4

    def __init__(self, x, y, y_vel, expl_height, color):
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.expl_height = expl_height
        self.color = color
        self.is_exploded = False
        self.projectiles = []

    def get_projectiles_numb(self, min, max):
        return random.randrange(start=min, stop=max, step=1)

    def get_random_color(self):
        return random.choice(COLORS)

    def explode(self):
        self.is_exploded = True
        projectiles_numb = self.get_projectiles_numb(
            min=self.MIN_PROJECTILE_NUMB, max=self.MAX_PROJECTILE_NUMB
        )

        # choose exploding way
        # 50/50 chance, that you get a star or circular explosion
        if random.randrange(start=0, stop=2, step=1) == 0:
            self.make_circular_projectiles(projectiles_numb=projectiles_numb)
        else:
            self.make_star_projectiles()

    def make_circular_projectiles(self, projectiles_numb):
        # computers calculate with RAD (pi)
        angle_increment = math.pi * 2 / projectiles_numb
        current_angle = 0  # rad
        projectile_velocity = random.randint(
            self.PROJECTILE_VEL - 3, self.PROJECTILE_VEL + 3
        )  # create different projectile speeds

        for i in range(projectiles_numb):
            # need to pick a new color each iteration through `projectiles_numb`
            color = self.get_random_color()
            x_vel_proj = projectile_velocity * math.cos(current_angle)
            y_vel_proj = projectile_velocity * math.sin(current_angle)

            # create Projectiles (Object)
            projectile = Projectile(
                x=self.x, y=self.y, x_vel=x_vel_proj, y_vel=y_vel_proj, color=color
            )
            self.projectiles.append(projectile)
            current_angle += angle_increment

    def make_star_projectiles(self):
        projectiles_numb = 32
        current_angle = 0
        angle_increment = math.pi / 4  # 45°

        for i in range(int(projectiles_numb / 8)):
            projectile_velocity = random.randint(
                self.PROJECTILE_VEL - 3, self.PROJECTILE_VEL + 3
            )

            for j in range(int(projectiles_numb / 4)):
                color = self.get_random_color()
                x_vel_proj = projectile_velocity * math.cos(current_angle)
                y_vel_proj = projectile_velocity * math.sin(current_angle)
                self.projectiles.append(
                    Projectile(
                        x=self.x,
                        y=self.y,
                        x_vel=x_vel_proj,
                        y_vel=y_vel_proj,
                        color=color,
                    )
                )
                current_angle += angle_increment
            # current_angle = 0 is not necessary due to RAD (720° = 4*pi)

    def move_up(self):
        if not self.is_exploded:
            self.y -= self.y_vel  # (-, <=) due to coordinat system of pygame
            if self.y <= self.expl_height:
                self.explode()

        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.spread()

            if (projectile.x <= 0) or (projectile.x >= GAMEWITH):
                projectiles_to_remove.append(projectile)
            elif (projectile.y <= 0) or (projectile.y >= GAMEHEIGHT):
                projectiles_to_remove.append(projectile)

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

    def draw_firework(self, win):
        if not self.is_exploded:
            # circle(surface, color, center, radius)
            pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)

        for projectile in self.projectiles:
            projectile.draw_prjectile(win=win)


class Launcher:  # creates the Fireworks
    LAUNCHER_WIDTH, LAUNCHER_HEIGHT = 20, 20

    def __init__(self, x, freq):
        self.x = x
        self.y = GAMEHEIGHT - self.LAUNCHER_HEIGHT
        self.freq = freq  # [ms]
        self.starting_time = time.time()
        self.fireworks = []

    def launch_firework(self):
        color = random.choice(COLORS)
        explode_height = random.randrange(
            start=MIN_EXPLODE_HEIGHT,
            stop=(GAMEHEIGHT // 2) - MIN_EXPLODE_HEIGHT,
            step=5,
        )

        # creating a Firekwork (Object)
        firework = Firework(
            x=self.x + self.LAUNCHER_WIDTH // 2,
            y=self.y,
            y_vel=Y_VELOCITY,
            expl_height=explode_height,
            color=color,
        )
        self.fireworks.append(firework)

    def manage_Launchers(self):
        current_time = time.time()
        time_elapsed = current_time - self.starting_time

        # check, whether you can launch another Firework or not
        # only allow to launch, if last Firework disappeared
        if time_elapsed * 1000 >= self.freq:  # [ms]
            self.starting_time = current_time
            self.launch_firework()

        """ Move Fireworks """
        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move_up()

            if firework.is_exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework)

        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)

    def draw_Launcher_and_firework(self, win):
        # pygame.draw.rect(SURFACE, RGB_COLOR, (X, Y, WIDTH, HEIGHT))
        pygame.draw.rect(
            win, GREY, (self.x, self.y, self.LAUNCHER_WIDTH, self.LAUNCHER_HEIGHT)
        )

        for firework in self.fireworks:
            firework.draw_firework(win=win)


def call_countdown(countdownnumber):
    font = pygame.font.SysFont(None, 500)

    for number in range(countdownnumber, -1, -1):
        WIN.fill(BLACK)
        # centering the Text
        numb = font.render(str(number), True, WHITE)
        text_centered = numb.get_rect(center=(GAMEWITH / 2, GAMEHEIGHT / 2))
        WIN.blit(numb, text_centered)

        pygame.display.update()
        time.sleep(1)

    font = pygame.font.SysFont("Somic Sans MS", 150)
    WIN.fill(BLACK)
    message = font.render("Happy New Year!", True, WHITE)
    text_centered = message.get_rect(center=(GAMEWITH / 2, GAMEHEIGHT / 2))
    WIN.blit(message, text_centered)
    pygame.display.update()
    time.sleep(2)


def main():
    call_countdown(countdownnumber=10)
    run = True
    clock = pygame.time.Clock()

    launchers = [
        Launcher(x=100, freq=3000),
        Launcher(x=300, freq=4000),
        Launcher(x=500, freq=8000),
        Launcher(x=700, freq=5000),
        Launcher(x=900, freq=2000),
    ]

    while run:
        WIN.fill(BLACK)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for launcher in launchers:
            # in manage_Launchers, I can replace max_screen_width and max_screen_height mit globals
            launcher.manage_Launchers()

            launcher.draw_Launcher_and_firework(win=WIN)
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
