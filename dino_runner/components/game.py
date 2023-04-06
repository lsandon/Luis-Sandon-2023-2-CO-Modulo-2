import pygame
import os

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, BG_DINO, HEART, AUDIO_DIR
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import Obstacle_Manager
from dino_runner.components.powerups.power_up_manager import Power_Up_Manager
from dino_runner.utils.text_utils import draw_message_component

FONT_COLOR = (0,0,0)
FONT_SIZE = 22
FONT_STYLE = "freesansbold.ttf"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.record = 0
        self.player = Dinosaur()
        self.obstacle_manager = Obstacle_Manager()
        self.power_up_manager = Power_Up_Manager()
        self.musica = pygame.mixer.music.load(os.path.join(AUDIO_DIR,'audios/mainMusic.wav'))
        self.sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'audios/score500.wav'))
        pygame.mixer.music.play(-1)
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
               

    def run(self):
        self.playing = True        
        self.power_up_manager.reset_powerups()
        self.obstacle_manager.reset_obstacles()
        self.game_speed = 20
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        self.update_game_speed()
        if self.score % 500 == 0:
            self.sound.play()

    def update_game_speed(self):
        if self.score % 100 == 0:
            self.game_speed += 1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) # "#FFFFFF"
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        self.draw_life()      
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed        

    def draw_score(self):
        draw_message_component(
            f"Score: {self.score}",self.screen,font_color=(0,100,0), pos_y_center = 50,pos_x_center=SCREEN_WIDTH - 140)
        draw_message_component(
            f"Record: {self.record}",self.screen,font_color=(0,100,0), pos_y_center = 20,pos_x_center=SCREEN_WIDTH - 140)

    def draw_life(self):
        if self.death_count == 0:
            draw_message_component("[Remaining Lives]", self.screen, 
            font_color=(0,0,0),font_size= 18, pos_x_center= 200, pos_y_center= 41)
            self.screen.blit(HEART, (30,30))   
            self.screen.blit(HEART, (60,30))
            self.screen.blit(HEART, (90,30))
        elif self.death_count == 1:
            draw_message_component("[Remaining Lives]", self.screen, 
            font_color=(0,0,0),font_size= 18, pos_x_center= 220, pos_y_center= 41)           
            self.screen.blit(HEART, (30,30))   
            self.screen.blit(HEART, (60,30))
        elif self.death_count == 2:
            draw_message_component("[Remaining Lives]", self.screen, 
            font_color=(0,0,0),font_size= 18, pos_x_center= 220, pos_y_center= 41)
            self.screen.blit(HEART, (30,30))              
   
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.shield_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.image_type.capitalize()} enabled for {time_to_show} seconds",
                    self.screen,
                    font_color= (165,42,42),
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            else:
                self.player.has_power_up = False
                self.player.image_type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.input = pygame.key.get_pressed()
            elif event.type == pygame.KEYDOWN:
                self.run()

    def bg_menu(self):
            BG_DINO.get_width()
            self.screen.blit(BG_DINO, (0, 0))
        

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:            
            self.bg_menu()        
            draw_message_component("Welcome to Dino Runner", self.screen, font_color=(255,255,255), 
            pos_y_center= half_screen_height -100,font_size= 55)            
            draw_message_component("Press any key to start", self.screen, font_color=(255,255,255))

        elif self.death_count == 1:
            self.bg_menu()
            self.record = self.score
            draw_message_component(f"Your personal record is:{self.record}", 
            self.screen,font_color=(255,255,255), pos_y_center=half_screen_height -125)  
            draw_message_component("Press any key to restart", self.screen,font_color=(255,255,255), 
            pos_y_center=half_screen_height + 140)
            draw_message_component("You have 2 more lives", self.screen,font_size= 35, font_color=(165,42,42), 
            pos_y_center=half_screen_height + 180)
            draw_message_component(
                f"Your Score:, {self.score}",
                self.screen,
                font_color=(255,255,255),
                pos_y_center=half_screen_height - 150
            )            
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                font_color=(255,255,255),
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))

        elif self.death_count == 2:
            self.bg_menu()
            if self.score > self.record:
                self.record = self.score
            draw_message_component(f"Your personal record is:{self.record}", self.screen,
            font_color=(255,255,255), pos_y_center=half_screen_height -125)      
            draw_message_component("Press any key to restart", self.screen,
            font_color=(255,255,255), pos_y_center=half_screen_height + 140)
            draw_message_component("You have 1 more life", self.screen,font_size= 35,
            font_color=(165,42,42), pos_y_center=half_screen_height + 180)
            draw_message_component(
                f"Your Score:, {self.score}",
                self.screen,
                font_color=(255,255,255),
                pos_y_center=half_screen_height - 150
            )            
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                font_color=(255,255,255),
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))

        elif self.death_count == 3:
            self.bg_menu()
            if self.score > self.record:
                self.record = self.score
            draw_message_component("Press any key to QUIT GAME", self.screen,font_color=(255,255,255), 
            pos_y_center=half_screen_height + 140)                
            draw_message_component(f"Your personal record is:{self.record}", self.screen,
            font_color=(255,255,255), pos_y_center=half_screen_height -125)                
            draw_message_component("You're dead", self.screen,font_size= 35,
            font_color=(165,42,42), pos_y_center=half_screen_height + 180)
            draw_message_component(
                f"Your Score:, {self.score}",
                self.screen,
                font_color=(255,255,255),
                pos_y_center=half_screen_height - 150
            )            
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                font_color=(255,255,255),
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))

            self.playing = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.running = False

        pygame.display.flip()
        self.handle_events_on_menu()



