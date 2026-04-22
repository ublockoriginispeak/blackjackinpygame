"""I'm aware that the below code is a mess, but I don't really care enough to overhaul it. 
The logic looked kind of messy without using any custom functions, but I added some comments to 
header the different sections, and now it looks okay-ish. The rendering is kind of a mess too but 
if you just take a minute to look at it it makes sense, and rendering bugs are basically just 
'if something isn't rendering properly, check the rendering section and make sure it's being 
blitted in the right order compared to everything else.' The messiest part is definitely the 
custom text rendering. I have an outline text and a main text for each text I want to render, and I 
have to set them both. I use a variety of different fonts I have set, some of which are the same fonts 
already loaded in memory but which I just created again anyway, and their names are confusing. I 
have the fonts declared up before the game loop, the text rendered in conditional statements in the 
game loop, and then the (two) different texts blitted to the screen down at the bottom, for 
every single piece of text in the game. Amazing."""

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
cursor_image = pygame.image.load('resources/player_hand.png').convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (16 * cursor_image_scale_multiplier, 16 * cursor_image_scale_multiplier))
pygame.mouse.set_visible(False)
cursor_image_rect = cursor_image.get_rect()
mouse_pos = pygame.mouse.get_pos()

outline_colour = (0, 0, 0)
text_colour = (255, 255, 255)

pygame.font.init()
cantarell_extrabold = pygame.font.SysFont('Cantarell Extrabold', 75)
clear_sans_bold_size_1 = pygame.font.SysFont('Clear Sans Bold', 50)
clear_sans_bold_size_2 = pygame.font.SysFont('Clear Sans Bold', 60)
bgm_toggle_hover_text = clear_sans_bold_size_1.render('Mute music', True, text_colour)
bgm_toggle_hover_text_outline = clear_sans_bold_size_1.render('Mute music', True, outline_colour)

background_music_0 = pygame.mixer.Sound('resources/sounds/bgm0.mp3')
background_music_0.play(-1)
bgm_playing = True
bgm_icon_scale_multiplier = 5
bgm_icon_position = (1500, 25)
bgm_off = pygame.image.load('resources/bgm_off.png').convert_alpha()
bgm_on_full = pygame.image.load('resources/bgm_on_full.png').convert_alpha()
bgm_off = pygame.transform.scale(bgm_off, (16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier))
bgm_on_full = pygame.transform.scale(bgm_on_full, (16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier))

restart_image = pygame.image.load('resources/restart.png').convert_alpha()
restart_image = pygame.transform.scale(restart_image, (16 * 7, 16 * 7))
restart_rect = pygame.Rect(800, 600, restart_image.get_width(), restart_image.get_height())
restart_rect.center = (800, 600)
restart_hover_text_outline = clear_sans_bold_size_1.render('Restart', True, outline_colour)
restart_hover_text = clear_sans_bold_size_1.render('Restart', True, text_colour)

player_prompt_font = pygame.font.SysFont('Clear Sans Bold', 50)
player_prompt_rect = pygame.Rect(500, 640, 1, 1)
bot_prompt_font = pygame.font.SysFont('Clear Sans Bold', 50)
hand_value_font = pygame.font.SysFont('Clear Sans Bold', 50)

player_hand = pygame.sprite.Group()
player_hand_area = pygame.Rect(0, 675, 1600, 225)
player_number_of_cards_spawned = 0
player_number_of_cards_touching_table = 0
player_hand_value = 0
player_prompt_text = "Waiting for you to turn over your cards..."
player_hand_value_indicator_position = (1200, 640)
player_hand_value_indicator = hand_value_font.render(f'Your hand: ', True, text_colour)
player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: ', True, outline_colour)
player_stood = False

bot_hand = pygame.sprite.Group()
bot_hand_area = pygame.Rect(0, 0, 1600, 225)
bot_number_of_cards_spawned = 0
bot_hand_value = 0
bot_think_timer = random.randint(100, 150)
bot_prompt_text = ""
bot_prompt_rect = pygame.Rect(500, 230, 1, 1)
bot_stood = False
bot_hand_value_text = ""
bot_hand_value_indicator_position = (1200, 230)
bot_hand_value_indicator = hand_value_font.render(f'Bot hand: {bot_hand_value_text}', True, text_colour)
bot_hand_value_indicator_outline = hand_value_font.render(f'Bot hand: {bot_hand_value_text}', True, outline_colour)

card_scale_multiplier = 3

deck_coords = (38, 350)
deck_image = pygame.image.load('resources/cards/card-back.png').convert_alpha()
deck_image = pygame.transform.scale(deck_image, (36 * card_scale_multiplier, 54 * card_scale_multiplier))
deck_rect = pygame.Rect(deck_coords[0], deck_coords[1], 36 * card_scale_multiplier, 54 * card_scale_multiplier)
deck_hover_text = clear_sans_bold_size_1.render('Left click to hit from deck', True, text_colour)
deck_hover_text_outline = clear_sans_bold_size_1.render('Left click to hit from deck', True, outline_colour)

header_position = (800, 150)
header_image = pygame.image.load('resources/header.png').convert_alpha()
header_rect = pygame.Rect(header_position[0], header_position[1], header_image.get_width(), header_image.get_height())
header_rect.center = header_position

play_button_position = (800, 500)
play_button_image_1 = pygame.image.load('resources/play_1.png').convert_alpha()
play_button_image_2 = pygame.image.load('resources/play_2.png').convert_alpha()
play_button_rect = pygame.Rect(play_button_position[0], play_button_position[1], play_button_image_1.get_width(), play_button_image_1.get_height())
play_button_rect.center = play_button_position
player_card_back_hover_text = clear_sans_bold_size_1.render('Right click to turn over', True, text_colour).convert_alpha()
player_card_back_hover_text_outline = clear_sans_bold_size_1.render('Right click to turn over', True, outline_colour).convert_alpha()

stand_button_position = (20, 550)
stand_button_scale_multiplier = 0.75
stand_button_image_1 = pygame.image.load('resources/stand_1.png').convert_alpha()
stand_button_image_2 = pygame.image.load('resources/stand_2.png').convert_alpha()
stand_button_image_1 = pygame.transform.scale(stand_button_image_1, (200 * stand_button_scale_multiplier, 100 * stand_button_scale_multiplier))
stand_button_image_2 = pygame.transform.scale(stand_button_image_2, (200 * stand_button_scale_multiplier, 100 * stand_button_scale_multiplier))
stand_button_rect = pygame.Rect(stand_button_position[0], stand_button_position[1], stand_button_image_1.get_width(), play_button_image_1.get_height())

ready_menu_scale_multiplier = 0.75
ready_menu_image = pygame.image.load('resources/ready.png').convert_alpha()
ready_menu_image = pygame.transform.scale(ready_menu_image, (400 * ready_menu_scale_multiplier, 200 * ready_menu_scale_multiplier))
ready_menu_rect = pygame.Rect(0, 0, ready_menu_image.get_width(), ready_menu_image.get_height())
ready_menu_rect.center = (800, 350)

yes_1_button_image = pygame.image.load('resources/yes_1.png').convert_alpha()
yes_2_button_image = pygame.image.load('resources/yes_2.png').convert_alpha()
yes_1_button_image = pygame.transform.scale(yes_1_button_image, (200 * ready_menu_scale_multiplier, 100 * ready_menu_scale_multiplier))
yes_2_button_image = pygame.transform.scale(yes_2_button_image, (200 * ready_menu_scale_multiplier, 100 * ready_menu_scale_multiplier))
yes_button_rect = pygame.Rect(0, 0, yes_1_button_image.get_width(), yes_1_button_image.get_height())
yes_button_rect.center = (600, 500)

no_1_button_image = pygame.image.load('resources/no_1.png').convert_alpha()
no_2_button_image = pygame.image.load('resources/no_2.png').convert_alpha()
no_1_button_image = pygame.transform.scale(no_1_button_image, (200 * ready_menu_scale_multiplier, 100 * ready_menu_scale_multiplier))
no_2_button_image = pygame.transform.scale(no_2_button_image, (200 * ready_menu_scale_multiplier, 100 * ready_menu_scale_multiplier))
no_button_rect = pygame.Rect(0, 0, no_1_button_image.get_width(), no_1_button_image.get_height())
no_button_rect.center = (1000, 500)

home_button_image = pygame.image.load('resources/home.png').convert_alpha()
home_button_image = pygame.transform.scale(home_button_image, (16 * 6, 16 * 6))
home_button_rect = pygame.Rect(25, 25, home_button_image.get_width(), home_button_image.get_height())
home_button_hover_text_outline = clear_sans_bold_size_1.render('Main menu', True, outline_colour)
home_button_hover_text = clear_sans_bold_size_1.render('Main menu', True, text_colour)

on_main_menu = True
player_can_hit = False
game_over = False
result_image = pygame.image.load('resources/draw.png').convert_alpha()
result_rect = pygame.Rect(0, 0, result_image.get_width(), result_image.get_height())
result_rect.center = (800, 450)
winner = ""
display_ready = False
player_bust = False
bot_bust = False
player_number_of_cards_spawned = 0
bot_number_of_cards_spawned = 0
player_card_position_gap = 0
bot_card_position_gap = 0
current_turn = "player"
player_stood = False
bot_stood = False
waiting_for_player = True

sfx_lets_go_gambling = pygame.mixer.Sound('resources/sounds/lets_go_gambling.mp3')

credit_font = pygame.font.SysFont('Clear Sans Bold', 30)
music_credit_text = credit_font.render('Music credit: https://www.youtube.com/watch?v=ichpZqbRtwM', True, (0, 0, 0), (255, 255, 255))
art_credit_text = credit_font.render('Featuring art from opengameart.org', True, (0, 0, 0), (255, 255, 255))
ace_hover_text = clear_sans_bold_size_1.render('', True, text_colour)
ace_hover_text_outline = clear_sans_bold_size_1.render('', True, outline_colour)
rule_explanation_text = credit_font.render('Aces can be either 1 or 11 depending on user choice, click them in your hand!', True, outline_colour, text_colour)

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
    def __init__(self, number, suit, x, y, identifer_number):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.number = number
        self.suit = suit
        self.local_scale_multiplier = card_scale_multiplier
        self.back_image = pygame.image.load('resources/cards/card-back.png').convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (36 * self.local_scale_multiplier, 54 * self.local_scale_multiplier))
        self.front_image = pygame.image.load(f'resources/cards/{suit}-{number}.png').convert_alpha()
        self.front_image = pygame.transform.scale(self.front_image, (36 * self.local_scale_multiplier, 54 * self.local_scale_multiplier))
        self.rect = self.front_image.get_rect()
        self.rect.center = (x, y)
        self.decorative_suit_name = suits[suit]
        self.card_name = card_names[number]
        self.active_image = self.back_image
        self.being_dragged = False
        self.identifier_number = identifer_number
        self.on_table = False
        if self.number == 1:
            self.is_ace = True
        else:
            self.is_ace = False
        print(f"card {self.identifier_number} spawned")

def reveal_hands():
    for card in bot_hand:
        card.active_image = card.front_image

def reset_game():
    global winner, game_over, display_ready, player_bust, bot_bust, player_number_of_cards_spawned, bot_number_of_cards_spawned, player_card_position_gap, bot_card_position_gap, current_turn,player_stood, bot_stood, waiting_for_player
    for card in player_hand:
        player_hand.remove(card)
    for card in bot_hand:
        bot_hand.remove(card)
    winner = ""
    game_over = False
    display_ready = False
    player_bust = False
    bot_bust = False
    player_number_of_cards_spawned = 0
    bot_number_of_cards_spawned = 0
    player_card_position_gap = 0
    bot_card_position_gap = 0
    current_turn = "player"
    player_stood = False
    bot_stood = False
    waiting_for_player = True

while running:

    mouse_pos = pygame.mouse.get_pos()
    mouse_delta = pygame.mouse.get_rel()
    cursor_image_rect.center = mouse_pos
    bgm_toggle = pygame.Rect(bgm_icon_position[0], bgm_icon_position[1], 16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier)
    player_number_of_cards_touching_table = 0
    number_of_cards_not_flipped_over = 0
    player_prompt_text = ""
    bot_prompt_text = ""
    waiting_for_player = False
    player_number_of_cards_touching_table = 0
    player_number_of_cards_spawned = 0
    player_hand_value = 0
    bot_hand_value = 0
    decorative_player_hand_value = 0
    player_hand_value_text = ""
    bot_hand_value_text = ""
    display_ready = False
    bot_number_of_aces = 0
    bot_bust = False
    player_bust = False
    winner = ""
    game_over = False
    display_ready = False

    if bot_think_timer <= 0:
        bot_think_timer = random.randint(100, 150)

    if not on_main_menu:
        #spawning default cards
        if len(player_hand.sprites()) < 2:
            player_number_of_cards_spawned += 1
            player_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], 533, 788, player_number_of_cards_spawned))
            player_number_of_cards_spawned += 1
            player_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], 1067, 788, player_number_of_cards_spawned))
        if len(bot_hand.sprites()) < 2:
            bot_number_of_cards_spawned += 1
            bot_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], 533, 112, bot_number_of_cards_spawned))
            bot_number_of_cards_spawned += 1
            bot_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], 1067, 112, bot_number_of_cards_spawned))
        # player hand statistics
        for card in player_hand: 
            if player_hand_area.colliderect(card):
                player_number_of_cards_touching_table += 1
            player_number_of_cards_spawned += 1

            if card.active_image == card.front_image and card.on_table:
                if card.number <= 10:
                    decorative_player_hand_value += card.number
                elif card.number > 10 and not card.is_ace:
                    decorative_player_hand_value += 10
                elif card.number == 11 and card.is_ace:
                    decorative_player_hand_value += 11
            if card.number <= 10:
                player_hand_value += card.number
            elif card.number > 10 and not card.is_ace:
                player_hand_value += 10
            elif card.number == 11 and card.is_ace:
                player_hand_value += card.number
            player_hand_value_indicator = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, text_colour)
            player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, outline_colour)
        # bot hand statistics
        for card in bot_hand:
            if card.number <= 10:
                bot_hand_value += card.number
            elif card.number > 10 and not card.is_ace:
                bot_hand_value += 10
            elif card.number > 10 and card.is_ace:
                bot_hand_value += card.number
            if card.is_ace:
                bot_number_of_aces += 1
            
            if card.active_image == card.back_image:
                bot_hand_value_text = "???"
            elif card.active_image == card.front_image:
                bot_hand_value_text = f"{bot_hand_value}"
            bot_hand_value_indicator = hand_value_font.render(f'Bot hand: {bot_hand_value_text}', True, text_colour)
            bot_hand_value_indicator_outline = hand_value_font.render(f'Bot hand: {bot_hand_value_text}', True, outline_colour)

            if player_hand_value > 21:
                player_bust = True
            if bot_hand_value > 21:
                bot_bust = True
        # all player card logic
        for card in player_hand: 
            card.rect.center = (card.x, card.y)
            if not card.on_table and not card.being_dragged and player_hand_area.colliderect(card):
                card.on_table = True
                flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                flip_sound.play()

            if card.being_dragged and not card.on_table:
                card.x += mouse_delta[0]
                card.y += mouse_delta[1]
                card.rect.center = (card.x, card.y)

            if card.on_table:
                if card.identifier_number == 1:
                    player_card_position_gap = 1600 / (player_number_of_cards_touching_table + 1) # set this to number of cards spawned or to number of cards on table to change the time at which the cards adjust their position, either immediately after a card is spawned or only when it is dropped onto a table, not sure which one looks nicer
                    card.x = player_card_position_gap # locks the first card into the left position on the hand area
                    card.y = 788
                else:
                    card.x = player_card_position_gap * card.identifier_number
                    card.y = 788

            if not card.on_table and not player_hand_area.colliderect(card) and not card.being_dragged:
                player_hand.remove(card)
                current_turn = "player"
                waiting_for_player = True
            
            if card.active_image != card.front_image:
                waiting_for_player = True
                number_of_cards_not_flipped_over += 1
                player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: {decorative_player_hand_value} + ???', True, outline_colour)
                player_hand_value_indicator = hand_value_font.render(f'Your hand: {decorative_player_hand_value} + ???', True, text_colour)

            if card.active_image == card.front_image and card.is_ace and card.rect.collidepoint(mouse_pos):
                if card.number == 1:
                    ace_hover_text = clear_sans_bold_size_1.render('Right click to change to 11', True, text_colour)
                    ace_hover_text_outline = clear_sans_bold_size_1.render('Right click to change to 11', True, outline_colour)
                elif card.number == 11:
                    ace_hover_text = clear_sans_bold_size_1.render('Right click to change to 1', True, text_colour)
                    ace_hover_text_outline = clear_sans_bold_size_1.render('Right click to change to 1', True, outline_colour)
        # all bot card logic
        for card in bot_hand:
            card.rect.center = (card.x, card.y)
            if card.identifier_number == 1:
                bot_card_position_gap = 1600 / (len(bot_hand) + 1) # set this to number of cards spawned or to number of cards on table to change the time at which the cards adjust their position, either immediately after a card is spawned or only when it is dropped onto a table, not sure which one looks nicer
                card.x = bot_card_position_gap # locks the first card into the left position on the hand area
                card.y = 112
            else:
                card.x = bot_card_position_gap * card.identifier_number
                card.y = 112
        # generic logic 
        if number_of_cards_not_flipped_over == 1:
            player_prompt_text = "Waiting for you to turn over your card..."
            waiting_for_player = True
        elif number_of_cards_not_flipped_over > 1:
            player_prompt_text = "Waiting for you to turn over your cards..."
            waiting_for_player = True
        elif number_of_cards_not_flipped_over == 0:
            waiting_for_player = False
        
        if bot_stood and player_stood:
            for card in bot_hand:
                if card.active_image == card.front_image:
                    display_ready = False
                else:
                    display_ready = True
        
        for card in bot_hand:
            if card.active_image == card.front_image:
                game_over = True

        if current_turn == "bot" and not waiting_for_player and not game_over:
            player_prompt_text = "Bot's turn"
        elif current_turn == "player" and not waiting_for_player and not game_over:
            player_prompt_text = "Your turn"

        if game_over:
            if player_bust and not bot_bust:
                winner = "bot"
            elif not player_bust and not bot_bust and bot_hand_value > player_hand_value:
                winner = "bot"
            elif not player_bust and bot_bust:
                winner = "player"
            elif not player_bust and not bot_bust and player_hand_value > bot_hand_value:
                winner = "player"
            elif player_bust and bot_bust:
                winner = "draw"
            elif not player_bust and not bot_bust and player_hand_value == bot_hand_value:
                winner = "draw"
        # bot decision making
        if bot_number_of_aces == 1:
            for card in bot_hand:
                if card.is_ace:
                    if card.number == 1 and (bot_hand_value + 10) <= 21:
                        card.number = 11
                    if card.number == 11 and bot_hand_value > 21:
                        card.number = 1
        elif bot_number_of_aces >= 2:
            for card in bot_hand:
                if card.is_ace:
                    if card.identifier_number == 1:
                        card.number = 11
                    elif card.identifier_number:
                        card.number = 1
        if current_turn == "bot" and not waiting_for_player and not display_ready and not game_over:
            bot_stood = False
            if bot_think_timer > 0:
                if bot_hand_value + 6.8 > 21:
                    bot_think_timer -= 4
                else:
                    bot_think_timer -= 1
                bot_prompt_text = "Bot is thinking"
            if bot_think_timer <= 0:
                if bot_hand_value + 6.8 > 21: # 6.8 is like roughly the average card value
                    current_turn = "player"
                    bot_stood = True
                elif bot_hand_value + 6.8 <= 21:
                    bot_number_of_cards_spawned += 1
                    bot_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], bot_card_position_gap, 112, bot_number_of_cards_spawned))
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                    current_turn = "player"
                    bot_stood = False
        
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
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                if home_button_rect.collidepoint(mouse_pos) and not on_main_menu:
                    on_main_menu = True
                    reset_game()
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                if restart_rect.collidepoint(mouse_pos) and game_over:
                    reset_game()
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                for card in player_hand:
                    if card.rect.collidepoint(mouse_pos):
                        card.being_dragged = True
                        flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                if play_button_rect.collidepoint(mouse_pos):
                    if on_main_menu:
                        sfx_lets_go_gambling.set_volume(0.2)
                        sfx_lets_go_gambling.play()
                    on_main_menu = False
                if not on_main_menu and not game_over and not display_ready and deck_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player:
                    player_number_of_cards_spawned += 1
                    new_card = Card(random.randint(1, 13), random.choice(list(suits.items()))[0], mouse_pos[0], mouse_pos[1], player_number_of_cards_spawned)
                    new_card.being_dragged = True
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                    player_hand.add(new_card)
                    waiting_for_player = True
                    current_turn = "bot"
                    player_stood = False
                if not on_main_menu and not game_over and not display_ready and stand_button_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player:
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                    current_turn = "bot"
                    waiting_for_player = False
                    player_stood = True
                if not on_main_menu and not game_over and display_ready == True and yes_button_rect.collidepoint(mouse_pos):
                    reveal_hands()
                    display_ready = False
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                elif not on_main_menu and display_ready == True and no_button_rect.collidepoint(mouse_pos):
                    current_turn == "player"
                    waiting_for_player = False
                    player_stood = False
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
            elif event.button == 3:
                for card in player_hand:
                    if card.rect.collidepoint(mouse_pos):
                        if card.on_table:
                            flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                            if card.active_image == card.back_image:
                                flip_sound.play()
                                card.active_image = card.front_image
                        if card.active_image == card.front_image and card.number == 1 and card.is_ace:
                            card.number = 11
                            flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                            flip_sound.play()
                        elif card.active_image == card.front_image and card.number == 11 and card.is_ace:
                            card.number = 1
                            flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                            flip_sound.play()

                for card in bot_hand:
                    if card.rect.collidepoint(mouse_pos):
                        print("You cannot see the other player's cards!")

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for card in player_hand:
                    card.being_dragged = False

    #rendering
    screen.fill(screen_colour)

    if on_main_menu:
        screen.blit(header_image, header_rect)

        if play_button_rect.collidepoint(mouse_pos):
            screen.blit(play_button_image_2, play_button_rect)
        else:
            screen.blit(play_button_image_1, play_button_rect)
        screen.blit(music_credit_text, (20, 850))
        screen.blit(art_credit_text, (1220, 850))
        screen.blit(rule_explanation_text, (460, 670))
    else:
        pygame.draw.rect(screen, (176, 128, 58), player_hand_area)
        pygame.draw.rect(screen, (176, 128, 58), bot_hand_area)
        screen.blit(deck_image, deck_rect)

        screen.blit(home_button_image, home_button_rect)

        bot_prompt_outline = bot_prompt_font.render(f'{bot_prompt_text}', True, outline_colour)
        bot_prompt = bot_prompt_font.render(f'{bot_prompt_text}', True, text_colour)
        screen.blit(bot_prompt_outline, (bot_prompt_rect[0] + 2, bot_prompt_rect[1] + 2))
        screen.blit(bot_prompt, bot_prompt_rect)

        player_prompt = player_prompt_font.render(f'{player_prompt_text}', True, text_colour)
        player_prompt_outline = player_prompt_font.render(f"{player_prompt_text}", True, outline_colour)
        screen.blit(player_prompt_outline, (player_prompt_rect[0] + 2, player_prompt_rect[1] + 2))
        screen.blit(player_prompt, player_prompt_rect)

        screen.blit(player_hand_value_indicator_outline, (player_hand_value_indicator_position[0] + 2, player_hand_value_indicator_position[1] + 2))
        screen.blit(player_hand_value_indicator, player_hand_value_indicator_position)
        
        player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, outline_colour)
        if player_bust:
            player_hand_value_indicator = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, (255, 0, 0))
        else:
            player_hand_value_indicator = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, text_colour)

        screen.blit(bot_hand_value_indicator_outline, (bot_hand_value_indicator_position[0] + 2, bot_hand_value_indicator_position[1] + 2))
        screen.blit(bot_hand_value_indicator, bot_hand_value_indicator_position)
        
        if stand_button_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player and not game_over and not display_ready:
            screen.blit(stand_button_image_2, stand_button_rect)
        else:
            screen.blit(stand_button_image_1, stand_button_rect)
        
        if home_button_rect.collidepoint(mouse_pos):
            screen.blit(home_button_hover_text_outline, (mouse_pos[0] + 27, mouse_pos[1] + 27))
            screen.blit(home_button_hover_text, (mouse_pos[0] + 25, mouse_pos[1] + 25))

        if deck_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player and not game_over and not display_ready:
            screen.blit(deck_hover_text_outline, (mouse_pos[0] + 52, mouse_pos[1] + 12))
            screen.blit(deck_hover_text, (mouse_pos[0] + 50, mouse_pos[1] + 10))

        if display_ready:
            screen.blit(ready_menu_image, ready_menu_rect)
            if yes_button_rect.collidepoint(mouse_pos):
                screen.blit(yes_2_button_image, yes_button_rect)
            else:
                screen.blit(yes_1_button_image, yes_button_rect)
            
            if no_button_rect.collidepoint(mouse_pos):
                screen.blit(no_2_button_image, no_button_rect)
            else:
                screen.blit(no_1_button_image, no_button_rect)
        
        if game_over:
            if winner == "player":
                result_image = pygame.image.load('resources/win.png').convert_alpha()
            elif winner == "bot":
                result_image = pygame.image.load('resources/lose.png').convert_alpha()
            elif winner == "draw":
                result_image = pygame.image.load('resources/draw.png').convert_alpha()
            
            screen.blit(result_image, result_rect)
            screen.blit(restart_image, restart_rect)

            if restart_rect.collidepoint(mouse_pos):
                screen.blit(restart_hover_text_outline, (mouse_pos[0] + 2, mouse_pos[1] + 22))
                screen.blit(restart_hover_text, (mouse_pos[0], mouse_pos[1] + 20))

        for card in player_hand:
            screen.blit(card.active_image, card.rect)

        for card in bot_hand:
            screen.blit(card.active_image, card.rect)

        for card in player_hand:
            if card.on_table and card.active_image == card.back_image and card.rect.collidepoint(mouse_pos) and not game_over and not display_ready:
                screen.blit(player_card_back_hover_text_outline, (mouse_pos[0] + 32, mouse_pos[1] + 2))
                screen.blit(player_card_back_hover_text, (mouse_pos[0] + 30, mouse_pos[1]))
            if card.on_table and card.active_image == card.front_image and card.is_ace and card.rect.collidepoint(mouse_pos) and not game_over and not display_ready:
                screen.blit(ace_hover_text_outline, (mouse_pos[0] + 32, mouse_pos[1] + 2))
                screen.blit(ace_hover_text, (mouse_pos[0] + 30, mouse_pos[1]))
        
    if bgm_playing == True:
        screen.blit(bgm_on_full, bgm_icon_position)
    else:
        screen.blit(bgm_off, bgm_icon_position)

    if bgm_toggle.collidepoint(mouse_pos):
        screen.blit(bgm_toggle_hover_text_outline, (mouse_pos[0] - 148, mouse_pos[1] + 33))
        screen.blit(bgm_toggle_hover_text, (mouse_pos[0] - 150, mouse_pos[1] + 35))
    
    """turn_indicator = clear_sans_bold_size_1.render(f'{current_turn}', True, (255, 255, 255)) # testing, get rid of afterwards
    waiting_indicator = clear_sans_bold_size_1.render(f'Waiting for player: {waiting_for_player}', True, (255, 255, 255))
    test_1 = clear_sans_bold_size_1.render(f'cards touching table: {player_number_of_cards_touching_table}', True, (255, 255, 255))
    test_2 = clear_sans_bold_size_1.render(f'player number of cards spawned: {player_number_of_cards_spawned}', True, (255, 255, 255))
    test_3 = clear_sans_bold_size_1.render(f'player hand value decorative: {decorative_player_hand_value}', True, (255, 255, 255))
    test_4 = clear_sans_bold_size_1.render(f'bot hand value: {bot_hand_value}', True, (255, 255, 255))
    test_5 = clear_sans_bold_size_1.render(f'real player hand value: {player_hand_value}', True, (255, 255, 255))

    screen.blit(test_3, (1000, 400))
    screen.blit(test_4, (1100, 450))
    screen.blit(turn_indicator, (1100, 500))
    screen.blit(waiting_indicator, (1100, 550))
    screen.blit(test_1, (1100, 600))
    screen.blit(test_2, (1000, 650))
    screen.blit(test_5, (1000, 350))"""

    cursor_image_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image, cursor_image_rect) # cursor should be the last thing blitted 
    
    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()
