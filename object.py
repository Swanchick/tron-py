import pygame
import math
from utils import RegisterManager, Vector
from settings import *


class GameObject:
    def __init__(self, game, classname=""):
        self.game = game
        self.x = 0
        self.y = 0
        self.classname = classname
    
    def start(self): ...
    def update(self): ...
    def draw(self, display): ...


class RoundManager(GameObject):
    def start(self):
        self.round_state = "menu"
        
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.game_text = self.font.render("Press space to start a game", True, WHITE)
        
        self.player_score = [0, 0]
        
        self.player1_score_text = self.font.render("Player 1: 0", True, COLOR_PLAYER_1)
        self.player2_score_text = self.font.render("Player 2: 0", True, COLOR_PLAYER_2)
        
    
    def find_players(self):
        objects = self.game.get_objects()
        players = []
        
        for object in objects:
            if issubclass(object.__class__, BasePlayer):
                players.append(object)

        return players
    
    def update(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_SPACE] and self.round_state != "game":
            self.round_state = "game"
            self.players = self.find_players()
            self.start_round()
        
    def start_round(self):
        for player in self.players:
            player.start_round(self)
        
    def draw(self, display):
        if self.round_state == "menu" or self.round_state == "end":
            display.blit(self.game_text, (WIDTH / 2 - 150, HEGIHT / 2 - 12, 100, 24))
        
        display.blit(self.player1_score_text, (0, 0, 150, 24))
        display.blit(self.player2_score_text, (WIDTH - 140, 0, 130, 24))
    
    def update_score(self):
        player1_score = self.player_score[0]
        player2_score = self.player_score[1]
        
        self.player1_score_text = self.font.render(f"Player 1: {player1_score}", True, COLOR_PLAYER_1)
        self.player2_score_text = self.font.render(f"Player 2: {player2_score}", True, COLOR_PLAYER_2)
    
    def end_round(self, who_win, color, player1, player2):
        if self.round_state != "game":
            return
         
        self.round_state = "end"
        
        self.game_text = self.font.render(who_win, True, color)
        
        for player in self.players:
            player.can_move = False
            player.restart()
        
        self.player_score[0] += player1
        self.player_score[1] += player2
        
        self.update_score()

RegisterManager.regist("RoundManager", RoundManager)


class BasePlayer(GameObject):
    def start(self):
        self.radius = 5
        self.speed = 5
        
        self.angle = 0
        self.angular_speed = 30
        
        self.x = 50
        self.y = 50
        self.old_x = self.x
        self.old_y = self.y
        
        self.tail = []
        self.tail_length = 100
        self.collision_handicap = 1.5
        self.tail_ignore = 2
        
        self.delay = 0
        self.delay_max = 0.2
        
        self.color = WHITE
        
        self.can_move = False
        self.enemy_player = None
        
        self.round_manager = None

    def set_start_pos(self):
        self.start_pos = (self.x, self.y)
        self.start_angle = self.angle
    
    def update(self):
        if not self.can_move: return
        
        self.controls()
        self.move()
        self.collision(self.tail, True)
        self.boundary_collision()
    
    def controls(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_RIGHT]:
            self.angle += math.pi / self.angular_speed
        if key[pygame.K_LEFT]:
            self.angle -= math.pi / self.angular_speed
    
    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        self.delay += 0.1

        if self.delay >= self.delay_max:
            self.tail.append(((self.old_x, self.old_y), (self.x, self.y)))
            self.delay = 0
            
            self.old_x = self.x
            self.old_y = self.y
        
        if len(self.tail) > self.tail_length:
            self.tail.pop(0)
    
    def collision(self, tail, ignore_part_of_tail):
        for index, pos in enumerate(tail):
            if index > len(tail) - self.tail_ignore and ignore_part_of_tail:
                continue
            
            point_pos = (self.x, self.y)
            
            line_dist = Vector.dist(pos[0], pos[1])
            dist1 = Vector.dist(point_pos, pos[0])
            dist2 = Vector.dist(point_pos, pos[1])
            
            if dist1 + dist2 <= line_dist + self.collision_handicap:
                self.on_hit()
    
    def boundary_collision(self):
        if self.x < 0 or self.x > WIDTH:
            self.on_hit()
        
        if self.y < 0 or self.y > HEGIHT:
            self.on_hit()
    
    def get_tail(self):
        return self.tail
    
    def start_round(self, round_manager):
        self.restart()
        
        self.setup_enemy_tail()
        
        self.round_manager = round_manager
        self.can_move = True
    
    def setup_enemy_tail(self):
        pass
    
    def on_hit(self):
        ...
    
    def clear_tail(self):
        self.tail = []
    
    def restart(self):
        self.clear_tail()
        
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.old_x = self.x
        self.old_y = self.y
        
        self.angle = self.start_angle
    
    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)
        self.draw_tail(display)

    def draw_tail(self, display):
        for index, pos in enumerate(self.tail):
            pygame.draw.line(display, self.color, pos[0], pos[1])


class Player1(BasePlayer):
    def start(self):
        super().start()
        
        self.color = COLOR_PLAYER_1
        
        self.set_start_pos()
    
    def update(self):
        super().update()
        
        if not self.enemy_player: return
        self.collision(self.enemy_player.get_tail(), False)
    
    def controls(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_d]:
            self.angle += math.pi / self.angular_speed
        if key[pygame.K_a]:
            self.angle -= math.pi / self.angular_speed
    
    def on_hit(self):
        self.round_manager.end_round("Player 2 Win!", COLOR_PLAYER_2, 0, 1)
    
    def setup_enemy_tail(self):
        self.enemy_player = self.game.find_objects_by_name("Player2")[0]
        
RegisterManager.regist("Player1", Player1)


class Player2(BasePlayer):
    def start(self):
        super().start()
        
        self.angle = math.pi
                
        self.x = WIDTH - 50
        self.y = HEGIHT - 50
        self.old_x = self.x
        self.old_y = self.y
        
        self.color = COLOR_PLAYER_2
        
        self.set_start_pos()
    
    def update(self):
        super().update()
        
        if not self.enemy_player: return
        self.collision(self.enemy_player.get_tail(), False)
    
    def on_hit(self):
        self.round_manager.end_round("Player 1 Win!", COLOR_PLAYER_1, 1, 0)
            
    def setup_enemy_tail(self):
        self.enemy_player = self.game.find_objects_by_name("Player1")[0]

RegisterManager.regist("Player2", Player2)
