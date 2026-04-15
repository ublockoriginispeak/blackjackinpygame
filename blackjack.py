import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1600, 900))
running = True
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()
delta_time = 0
screen_colour = (133, 181, 112)

cursor_image_scale_multiplier = 5
cursor_image = pygame.image.load('blackjack/resources/player_hand.png').convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (16 * cursor_image_scale_multiplier, 16 * cursor_image_scale_multiplier))
pygame.mouse.set_visible(False)
cursor_image_rect = cursor_image.get_rect()
mouse_pos = pygame.mouse.get_pos()

pygame.font.init()
cantarell_extrabold = pygame.font.SysFont('Cantarell Extrabold', 75)
clear_sans_bold = pygame.font.SysFont('Clear Sans Bold', 50)
bgm_toggle_hover_text = clear_sans_bold.render('Mute music', True, (0, 0, 0))
bgm_toggle_hover_text_outline = clear_sans_bold.render('Mute music', True, (255, 255, 0))

background_music_0 = pygame.mixer.Sound('blackjack/resources/sounds/bgm0.mp3')
background_music_0.play(-1)
bgm_playing = True
bgm_icon_scale_multiplier = 5
bgm_icon_position = (1500, 25)
bgm_off = pygame.image.load('blackjack/resources/bgm_off.png').convert_alpha()
bgm_on_full = pygame.image.load('blackjack/resources/bgm_on_full.png').convert_alpha()
bgm_off = pygame.transform.scale(bgm_off, (16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier))
bgm_on_full = pygame.transform.scale(bgm_on_full, (16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier))

player_hand = pygame.sprite.Group()
bot_hand = pygame.sprite.Group()

header_position = (800, 150)
header_image = pygame.image.load('blackjack/resources/header.jpg').convert()

play_button_position = (800, 700)
play_button_image = pygame.image.load('blackjack/resources/play_button.jpg').convert()

on_main_menu = True

card_scale_multiplier = 3

card_names = {
    1 : "Ace (1)",
    2 : "Two",
    3 : "Three",
    4 : "Four",
    5 : "Five",
    6 : "Six",
    7 : "Seven",
    8 : "Eight",
    9 : "Nine",
    10 : "Ten",
    11 : "Jack (10)",
    12 : "Queen (10)",
    13 : "King (10)"
}

suits = {
    "hearts" : " of Hearts",
    "diamonds" : " of Diamonds",
    "spades" : " of Spades",
    "clubs" : " of Clubs"
}

class Card(pygame.sprite.Sprite):
    def __init__(self, number, suit, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.local_scale_multiplier = card_scale_multiplier
        self.back_image = pygame.image.load('blackjack/resources/cards/card-back.png').convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (36 * self.local_scale_multiplier, 54 * self.local_scale_multiplier))
        self.front_image = pygame.image.load(f'blackjack/resources/cards/{suit}-{number}.png').convert_alpha()
        self.front_image = pygame.transform.scale(self.front_image, (36 * self.local_scale_multiplier, 54 * self.local_scale_multiplier))
        self.rect = self.front_image.get_rect()
        self.rect.center = (x, y)
        self.decorative_suit_name = suits[suit]
        self.card_name = card_names[number]
        self.active_image = self.back_image
        self.being_flipped_around = False
        self.being_dragged = False
        self.index_in_deck = 0

header_rect = pygame.Rect(header_position[0], header_position[1], header_image.get_width(), header_image.get_height())
header_rect.center = header_position

play_button_rect = pygame.Rect(play_button_position[0], play_button_position[1], play_button_image.get_width(), play_button_image.get_height())
play_button_rect.center = play_button_position

play_button_hover_text = clear_sans_bold.render('Click to play', True, (0, 0, 0)).convert_alpha()
play_button_hover_text_outline = clear_sans_bold.render('Click to play', True, (255, 255, 0)).convert_alpha()

player_hand_area = pygame.Rect(0, 675, 1600, 225)

while running:

    if not on_main_menu:
        if len(player_hand.sprites()) < 2:
            player_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], mouse_pos[0], mouse_pos[1]))
            player_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], mouse_pos[0], mouse_pos[1] + 10))


    mouse_pos = pygame.mouse.get_pos()
    cursor_image_rect.center = mouse_pos
    bgm_toggle = pygame.Rect(bgm_icon_position[0], bgm_icon_position[1], 16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier)
    mouse_delta = pygame.mouse.get_rel()

    for card in player_hand:
        if card.being_dragged:
            card.x += mouse_delta[0]
            card.y += mouse_delta[1]
        card.rect.center = (card.x, card.y)
    #event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if bgm_toggle.collidepoint(mouse_pos):
                    if bgm_playing == True:
                        bgm_playing = False
                        background_music_0.set_volume(0)
                    elif bgm_playing == False:
                        bgm_playing = True
                        background_music_0.set_volume(1)
                for card in player_hand:
                    if card.rect.collidepoint(mouse_pos):
                        card.being_dragged = True
                if play_button_rect.collidepoint(mouse_pos):
                    on_main_menu = False
            elif event.button == 3:
                for card in player_hand:
                    if card.rect.collidepoint(mouse_pos):
                        if card.active_image == card.front_image:
                            card.active_image = card.back_image
                        else:
                            card.active_image = card.front_image
                        flip_sound = pygame.mixer.Sound(f'blackjack/resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                        flip_sound.play()

                for card in bot_hand:
                    if card.rect.collidepoint(mouse_pos):
                        print("You cannot see the other player's cards!")

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for card in player_hand:
                    card.being_dragged = False
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #spawn new random card at mouse position
                new_card = Card(random.randint(1, 13), random.choice(list(suits.items()))[0], mouse_pos[0], mouse_pos[1])"""
                
    #rendering
    screen.fill(screen_colour)

    if on_main_menu:
        screen.blit(header_image, header_rect)
        screen.blit(play_button_image, play_button_rect)

        if play_button_rect.collidepoint(mouse_pos):
            screen.blit(play_button_hover_text_outline, (mouse_pos[0], mouse_pos[1] - 50))
            screen.blit(play_button_hover_text, (mouse_pos[0] - 2, mouse_pos[1] - 53))
    else:
        pygame.draw.rect(screen, (176, 128, 58), player_hand_area)
    
    if bgm_playing == True:
        screen.blit(bgm_on_full, bgm_icon_position)
    else:
        screen.blit(bgm_off, bgm_icon_position)

    for card in player_hand:
        screen.blit(card.active_image, card.rect)

    if bgm_toggle.collidepoint(mouse_pos):
        screen.blit(bgm_toggle_hover_text_outline, (mouse_pos[0] - 153, mouse_pos[1] + 38))
        screen.blit(bgm_toggle_hover_text, (mouse_pos[0] - 150, mouse_pos[1] + 35))

    cursor_image_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image, cursor_image_rect) # cursor should be the last thing blitted 
    
    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()

