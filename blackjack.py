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

pygame.font.init()
cantarell_extrabold = pygame.font.SysFont('Cantarell Extrabold', 75)
clear_sans_bold_size_1 = pygame.font.SysFont('Clear Sans Bold', 50)
clear_sans_bold_size_2 = pygame.font.SysFont('Clear Sans Bold', 60)
bgm_toggle_hover_text = clear_sans_bold_size_1.render('Mute music', True, (0, 0, 0))
bgm_toggle_hover_text_outline = clear_sans_bold_size_1.render('Mute music', True, (255, 255, 255))

background_music_0 = pygame.mixer.Sound('resources/sounds/bgm0.mp3')
background_music_0.play(-1)
bgm_playing = True
bgm_icon_scale_multiplier = 5
bgm_icon_position = (1500, 25)
bgm_off = pygame.image.load('resources/bgm_off.png').convert_alpha()
bgm_on_full = pygame.image.load('resources/bgm_on_full.png').convert_alpha()
bgm_off = pygame.transform.scale(bgm_off, (16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier))
bgm_on_full = pygame.transform.scale(bgm_on_full, (16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier))

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
player_hand_value_indicator = hand_value_font.render(f'Your hand: ', True, (0, 0, 0))
player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: ', True, (255, 255, 255))

bot_hand = pygame.sprite.Group()
bot_hand_area = pygame.Rect(0, 0, 1600, 225)
bot_number_of_cards_spawned = 0
bot_hand_value = 0
bot_prompt = ""

card_scale_multiplier = 3

deck_coords = (38, 350)
deck_image = pygame.image.load('resources/cards/card-back.png').convert_alpha()
deck_image = pygame.transform.scale(deck_image, (36 * card_scale_multiplier, 54 * card_scale_multiplier))
deck_rect = pygame.Rect(deck_coords[0], deck_coords[1], 36 * card_scale_multiplier, 54 * card_scale_multiplier)
deck_hover_text = clear_sans_bold_size_1.render('Left click to hit from deck', True, (0, 0, 0))
deck_hover_text_outline = clear_sans_bold_size_1.render('Left click to hit from deck', True, (255, 255, 255))

header_position = (800, 150)
header_image = pygame.image.load('resources/header.png').convert_alpha()
header_rect = pygame.Rect(header_position[0], header_position[1], header_image.get_width(), header_image.get_height())
header_rect.center = header_position

play_button_position = (800, 500)
play_button_image_1 = pygame.image.load('resources/play_1.png').convert_alpha()
play_button_image_2 = pygame.image.load('resources/play_2.png').convert_alpha()
play_button_rect = pygame.Rect(play_button_position[0], play_button_position[1], play_button_image_1.get_width(), play_button_image_1.get_height())
play_button_rect.center = play_button_position
player_card_back_hover_text = clear_sans_bold_size_1.render('Right click to turn over', True, (0, 0, 0)).convert_alpha()
player_card_back_hover_text_outline = clear_sans_bold_size_1.render('Right click to turn over', True, (255, 255, 255)).convert_alpha()

stand_button_position = (20, 550)
stand_button_scale_multiplier = 0.75
stand_button_image_1 = pygame.image.load('resources/stand_1.png').convert_alpha()
stand_button_image_2 = pygame.image.load('resources/stand_2.png').convert_alpha()
stand_button_image_1 = pygame.transform.scale(stand_button_image_1, (200 * stand_button_scale_multiplier, 100 * stand_button_scale_multiplier))
stand_button_image_2 = pygame.transform.scale(stand_button_image_2, (200 * stand_button_scale_multiplier, 100 * stand_button_scale_multiplier))
stand_button_rect = pygame.Rect(stand_button_position[0], stand_button_position[1], stand_button_image_1.get_width(), play_button_image_1.get_height())

waiting_for_player = False
current_turn = "player"
on_main_menu = True
player_can_hit = False

sfx_lets_go_gambling = pygame.mixer.Sound('resources/sounds/lets_go_gambling.mp3')

credit_font = pygame.font.SysFont('Clear Sans Bold', 30)
music_credit_text = credit_font.render('Music credit: https://www.youtube.com/watch?v=ichpZqbRtwM', True, (0, 0, 0), (255, 255, 255))
art_credit_text = credit_font.render('Featuring art from opengameart.org', True, (0, 0, 0), (255, 255, 255))
ace_hover_text = clear_sans_bold_size_1.render('', True, (0, 0, 0))
ace_hover_text_outline = clear_sans_bold_size_1.render('', True, (255, 255, 255))

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

def make_bot_decision():
    pass

while running:

    mouse_pos = pygame.mouse.get_pos()
    mouse_delta = pygame.mouse.get_rel()
    cursor_image_rect.center = mouse_pos
    bgm_toggle = pygame.Rect(bgm_icon_position[0], bgm_icon_position[1], 16 * bgm_icon_scale_multiplier, 16 * bgm_icon_scale_multiplier)
    player_number_of_cards_touching_table = 0
    player_prompt = player_prompt_font.render(f'{player_prompt_text}', True, (0, 0, 0))
    player_prompt_outline = player_prompt_font.render(f"{player_prompt_text}", True, (255, 255, 255))
    number_of_cards_not_flipped_over = 0
    player_prompt_text = ""
    waiting_for_player = False
    player_number_of_cards_touching_table = 0
    player_number_of_cards_spawned = 0
    player_hand_value = 0
    bot_hand_value = 0
    decorative_player_hand_value = 0
    player_hand_value_text = ""
    bot_hand_value_text = ""

    if not on_main_menu:
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

        for card in player_hand: # have to have this out of the below FOR loop
            if player_hand_area.colliderect(card):
                player_number_of_cards_touching_table += 1 # so the cards on the table don't adjust their position the moment a card is spawned, but the moment it is dropped onto the table
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
            
            player_hand_value_indicator = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, (0, 0, 0))
            player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, (255, 255, 255))

        for card in bot_hand:
            if card.number <= 10:
                bot_hand_value += card.number
            elif card.number > 10 and not card.is_ace:
                bot_hand_value += 10
            elif card.number > 10 and card.is_ace:
                bot_hand_value += card.number

        for card in player_hand:

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
                player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: {decorative_player_hand_value} + ???', True, (255, 255, 255))
                player_hand_value_indicator = hand_value_font.render(f'Your hand: {decorative_player_hand_value} + ???', True, (0, 0, 0))

            if card.active_image == card.front_image and card.is_ace and card.rect.collidepoint(mouse_pos):
                if card.number == 1:
                    ace_hover_text = clear_sans_bold_size_1.render('Right click to change to 11', True, (0, 0, 0))
                    ace_hover_text_outline = clear_sans_bold_size_1.render('Right click to change to 1', True, (255, 255, 255))
                elif card.number == 11:
                    ace_hover_text = clear_sans_bold_size_1.render('Right click to change to 1', True, (0, 0, 0))
                    ace_hover_text_outline = clear_sans_bold_size_1.render('Right click to change to 1', True, (255, 255, 255))

        if number_of_cards_not_flipped_over == 1:
            player_prompt_text = "Waiting for you to turn over your card..."
            waiting_for_player = True
        elif number_of_cards_not_flipped_over > 1:
            player_prompt_text = "Waiting for you to turn over your cards..."
            waiting_for_player = True

        if current_turn == "bot" and not waiting_for_player:
            player_prompt_text = "Bot's turn"

        if current_turn == "bot" and not waiting_for_player:
            if bot_hand_value + 6.8 > 21: # 6.8 is like roughly the average card value
                current_turn = "player"
            elif bot_hand_value + 6.8 <= 21:
                bot_number_of_cards_spawned += 1
                bot_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], 50, 50, bot_number_of_cards_spawned))
                current_turn = "player"

        for card in bot_hand:
            card.on_table = True
            card.x = 500
            card.y = 500

        
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
                        flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                if play_button_rect.collidepoint(mouse_pos):
                    if on_main_menu:
                        sfx_lets_go_gambling.set_volume(0.2)
                        sfx_lets_go_gambling.play()
                    on_main_menu = False
                if not on_main_menu and deck_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player:
                    player_number_of_cards_spawned += 1
                    new_card = Card(random.randint(1, 13), random.choice(list(suits.items()))[0], mouse_pos[0], mouse_pos[1], player_number_of_cards_spawned)
                    new_card.being_dragged = True
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                    player_hand.add(new_card)
                    waiting_for_player = True
                    current_turn = "bot"
                if not on_main_menu and stand_button_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player:
                    flip_sound = pygame.mixer.Sound(f'resources/sounds/card_flip_{random.randint(1, 3)}.mp3')
                    flip_sound.play()
                    current_turn = "bot"
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #spawn new random card at mouse position
                player_number_of_cards_spawned += 1
                player_hand.add(Card(random.randint(1, 13), random.choice(list(suits.items()))[0], 100, 100, player_number_of_cards_spawned))

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
    else:
        pygame.draw.rect(screen, (176, 128, 58), player_hand_area)
        pygame.draw.rect(screen, (176, 128, 58), bot_hand_area)
        screen.blit(deck_image, deck_rect)
        
        player_hand_value_indicator_outline = hand_value_font.render(f'Your hand: {decorative_player_hand_value}', True, (255, 255, 255))
        screen.blit(player_hand_value_indicator_outline, (player_hand_value_indicator_position[0] + 1, player_hand_value_indicator_position[1] - 1))
        screen.blit(player_hand_value_indicator, player_hand_value_indicator_position)
        
        if stand_button_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player:
            screen.blit(stand_button_image_2, stand_button_rect)
        else:
            screen.blit(stand_button_image_1, stand_button_rect)
        
        if deck_rect.collidepoint(mouse_pos) and current_turn == "player" and not waiting_for_player:
            screen.blit(deck_hover_text_outline, (mouse_pos[0] + 51, mouse_pos[1] - 11))
            screen.blit(deck_hover_text, (mouse_pos[0] + 50, mouse_pos[1] - 10))

        for card in bot_hand:
            screen.blit(card.active_image, card.rect)

        for card in player_hand:
            screen.blit(card.active_image, card.rect)

        for card in player_hand:
            if card.on_table and card.active_image == card.back_image and card.rect.collidepoint(mouse_pos):
                screen.blit(player_card_back_hover_text_outline, (mouse_pos[0] - 11, mouse_pos[1] + 51))
                screen.blit(player_card_back_hover_text, (mouse_pos[0] - 10, mouse_pos[1] + 50))
            if card.on_table and card.active_image == card.front_image and card.is_ace and card.rect.collidepoint(mouse_pos):
                screen.blit(ace_hover_text_outline, (mouse_pos[0] - 1, mouse_pos[1] + 1))
                screen.blit(ace_hover_text, (mouse_pos[0], mouse_pos[1]))

        screen.blit(player_prompt_outline, (player_prompt_rect[0] - 1, player_prompt_rect[1] + 1))
        screen.blit(player_prompt, player_prompt_rect)
        
    if bgm_playing == True:
        screen.blit(bgm_on_full, bgm_icon_position)
    else:
        screen.blit(bgm_off, bgm_icon_position)

    if bgm_toggle.collidepoint(mouse_pos):
        screen.blit(bgm_toggle_hover_text_outline, (mouse_pos[0] - 151, mouse_pos[1] + 36))
        screen.blit(bgm_toggle_hover_text, (mouse_pos[0] - 150, mouse_pos[1] + 35))
    
    turn_indicator = clear_sans_bold_size_1.render(f'{current_turn}', True, (255, 255, 255)) # testing, get rid of afterwards
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
    screen.blit(test_5, (1000, 350))

    cursor_image_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image, cursor_image_rect) # cursor should be the last thing blitted 
    
    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()