import pygame
import math
import random
import sys
from pygame.locals import *

# Setup display
# First step: initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('bgmusic.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

soft_click = pygame.mixer.Sound('soundeffect.wav')
soft_click.set_volume(0.4)  # 0.2


# Second step: define dimensions of our script and name the app
# Pro tip as a good habit: constant values - capital letters
WIDTH, HEIGHT = 800, 600
# Window
win = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame accepts a tupple for the width and height
pygame.display.set_caption("Hangman Game")
gameIcon = pygame.image.load('hangmangameicon.png')
pygame.display.set_icon(gameIcon)

# Button variables english
RADIUS = 20
GAP = 15
letters = []  # store buttons [34, 56, "A", True - visible (clicked) or invisible (unclicked)]
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
# comicsans, Courier, Times New Roman, Ariel
LETTER_FONT = pygame.font.SysFont('system', 40)
WORD_FONT = pygame.font.SysFont('system', 60)
WORD_FONT_ACTIVE = pygame.font.SysFont('system', 70)
TITLE_FONT = pygame.font.SysFont('system', 70)
TEXT_FONT = pygame.font.SysFont('system', 28)
SUB_TEXT_FONT = pygame.font.SysFont('system', 20)
GAME_END_FONT = pygame.font.SysFont('system', 100)
COUNTDOWN_TIMER_FONT = pygame.font.SysFont('comicsans', 70)  # 80


# Load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# Game variables
hangman_status = 0
# words = ["IDE", "LOL", "PYTHON", "PYGAME"] - MUST BE CAPITAL LETTERS
fruit = ["LEMON", "PINEAPPLE", "KIWI", "BANANA", "WATERMELON", "BLACKBERRY", "CHERRY", "PEACH", "AVOCADO", "GRAPES", "LIME", "MANGO", "ORANGE", "MELON", "PAPAYA", "PEAR",
         "PLUM", "RASPBERRY", "STRAWBERRY"]
mobile = ["MOTOROLA", "APPLE", "NOKIA", "SAMSUNG", "OPPO", "GOOGLE", "HUAWEI", "XIAOMI", "ONEPLUS", "LG", "VIVO"]
furniture_house = ["TABLE", "SOFA", "WARDROBE", "CHAIR", "BED", "DESK", "BATHTUB", "MIRROR", "FRIDGE", "COUCH", "CLOCK", "WINDOW", "DOOR"]
sport = ["ATHLETE", "ATHLETICS", "BADMINTON", "BALL", "BASEBALL", "BASKETBALL", "FOOTBALL", "SOCCER", "BICYCLE", "BIKE", "BOXER", "JUMP", "MOVE", "PLAYER", "QUARTER",
         "RACE", "RACING", "REFEREE", "RUN", "RUNNING", "RUGBY", "SCOREBOARD", "SKI", "SKIING", "SWIM", "SWIMMER", "SWIMMING", "SPORT", "SURFER", "SNOWBOARD", "HANDBALL"]
popular_english_words = ["BACK", "BEHIND", "BRING", "COLD", "HOT", "COUNTRY", "CRY", "COLOUR", "ANIMAL", "DOWN", "UP", "EXPERIENCE", "FIRST", "FRIEND", "FOOD", "DIFFERENT",
                         "EYE", "EARLY", "LATE", "AIR", "CLOSE", "CLEAR", "CUT", "CROSS", "BUILD", "FAST", "SLOW", "EXAMPLE", "FULL", "FORM", "GAME", "GET", "GIVE", "TAKE",
                         "MAKE", "REAL", "VISIBLE", "VISION", "GAME", "GIRL", "GO", "GOLD", "GOVERNMENT", "GREAT", "GROUND", "GROUP", "GROW", "GUY", "MONEY", "MONTH", "MOON",
                         "MORE"]
colours = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "PURPLE", "PINK", "WHITE", "GRAY", "BROWN", "BLACK"]
words = fruit + mobile + furniture_house + sport + popular_english_words + colours

# word = "DEVELOPER"  # guessed = ["D"] -> D _ _ _ _ _ _ _
word = random.choice(words)
guessed = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_THEME_PRIMARY = (31, 27, 36)
PRIMARY_COLOR = (187, 134, 252)
SECONDARY_COLOR = (3, 218, 197)
BUTTON_HOVER_COLOR = (145, 59, 249)
BUTTON_HOVER_COLOR_SECONDARY = (2, 168, 152)

counter = ''
timer_countdown = ''
timer_event = pygame.USEREVENT + 1


# draw function
def draw():
    # global pausegamebutton
    # global game_timer_countdown
    global counter
    global timer_countdown
    global timer_event

    win.fill(DARK_THEME_PRIMARY)
    pausegamebutton.draw(win)

    # game_timer_countdown_rect = game_timer_countdown.get_rect(topleft=win.get_rect().topleft)
    # win.blit(game_timer_countdown, game_timer_countdown_rect)

    timer_countdown_rect = timer_countdown.get_rect(center=(710, 552.5))  # y = 550 or 552.5 or 555
    win.blit(timer_countdown, timer_countdown_rect)

    # draw title
    text = TITLE_FONT.render("HANGMAN GAME", 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # game page bottom text
    text = SUB_TEXT_FONT.render("Press \'m/n\' - Mute/Unmute game music", 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 527.5))

    text = SUB_TEXT_FONT.render("Press \'p\' - Pause/Unpause the current game", 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 550))

    text = SUB_TEXT_FONT.render("Press \'ESC\' - Return to Main Menu", 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 572.5))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
        # render word
    text = WORD_FONT.render(display_word, 1, PRIMARY_COLOR)
    win.blit(text, (400, 200))

    # draw buttons/letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, PRIMARY_COLOR, (x, y), RADIUS, 1)  # "1" - thickness of outline (2, 3, 4 also good above isn't good)
            # render text
            text = LETTER_FONT.render(ltr, 1, PRIMARY_COLOR)
            # draw this
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    # Update the display - in pygame we have to (when we draw something)
    pygame.display.update()


def display_message(message):
    global counter
    global timer_countdown
    global timer_event
    # global playagainbutton
    # skip_endgame_screen = pygame.time.get_ticks() + 4*1000

    # game_end_counter = 10
    # game_end_timer_countdown = COUNTDOWN_TIMER_FONT.render(str(game_end_counter), True, SECONDARY_COLOR)

    # game_end_timer_event = pygame.USEREVENT + 1
    # pygame.time.set_timer(game_end_timer_event, 1000)  # set this to 4000 for example so that every 4 seconds the counter will decrease by 1 from 10
    # (1 second == 4 seconds or whatever we set here)

    counter = 10
    timer_countdown = COUNTDOWN_TIMER_FONT.render(str(counter), True, SECONDARY_COLOR)

    # timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    # set another event for backup but without a visible timer
    pygame.time.set_timer(pygame.USEREVENT, 20000)
    while True:
        # pygame.time.delay(1000)
        win.fill(DARK_THEME_PRIMARY)
        # playagainbutton = ButtonSecondary(PRIMARY_COLOR, BUTTON_HOVER_COLOR, PRIMARY_COLOR, 'Play Again!', 275, 400, 250, 100)
        playagainbutton.draw(win)
        game_result_text = 'THE WORD WAS: '
        word_was = WORD_FONT.render(game_result_text.upper(), 1, SECONDARY_COLOR)
        word_text = WORD_FONT.render(word.upper(), 1, SECONDARY_COLOR)
        game_end_text = GAME_END_FONT.render(message, 1, SECONDARY_COLOR)
        win.blit(word_was, (WIDTH / 2 - word_was.get_width() / 2, 120))
        win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 170))
        win.blit(game_end_text, (WIDTH / 2 - game_end_text.get_width() / 2, HEIGHT / 2 - game_end_text.get_height() / 2))

        for event in pygame.event.get():
            # if skip_endgame_screen <= pygame.time.get_ticks():
            #     main_menu()
            # else:
            #     if event.type == MOUSEBUTTONDOWN:
            #       ...

            # if event.type == game_end_timer_event:
            #     game_end_counter -= 1
            #     game_end_timer_countdown = COUNTDOWN_TIMER_FONT.render(str(game_end_counter), True, SECONDARY_COLOR)
            #     if game_end_counter == 0:
            #         pygame.time.set_timer(game_end_timer_event, 0)  # set to 0 - visible if we don't call main_menu() as example
            #         main_menu()
            if event.type == timer_event:
                counter -= 1
                timer_countdown = COUNTDOWN_TIMER_FONT.render(str(counter), True, SECONDARY_COLOR)
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)  # set to 0 - visible if we don't call main_menu() as example
                    main_menu()
            if event.type == USEREVENT:
                main_menu()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if playagainbutton.isOver(pos):
                    restart()
                    game()
            playagainbutton.handle_event(event)

        # game_end_timer_countdown_rect = game_end_timer_countdown.get_rect(midtop=win.get_rect().midtop)
        # win.blit(game_end_timer_countdown, game_end_timer_countdown_rect)
        timer_countdown_rect = timer_countdown.get_rect(midtop=win.get_rect().midtop)
        win.blit(timer_countdown, timer_countdown_rect)
        pygame.display.flip()
        pygame.display.update()
        # pygame.time.delay(4000)


# defining two classes for different types of buttons
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = WORD_FONT.render(self.text, 1, BLACK)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class ButtonSecondary:
    def __init__(self, color_passive, color_active, color_click, text, x, y, width, height, function=None):
        """Init all needed variables only once"""
        self.rect = pygame.Rect(x, y, width, height)  # self.rect = pygame.Rect(x, y, 400, 100)
        self.color_passive = color_passive
        self.color_active = color_active
        self.color_click = color_click
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.function = function

        self.shadow_rect = self.rect.copy()
        self.shadow_rect.x += 5
        self.shadow_rect.y += 5

        # self.color_passive = (89, 89, 89)
        # self.color_active = (212, 200, 235)
        # self.color_click = (0, 200, 0)

        self.hovered = False
        self.clicked = False

        # self.font_passive = pygame.font.SysFont('Times New Roman', 24)
        # self.font_active = pygame.font.SysFont('Times New Roman', 28)
        self.font_passive = WORD_FONT
        self.font_active = WORD_FONT_ACTIVE

        self.render_text()

    def render_text(self):
        """Render text but don't display it"""

        # self.passive_text = WORD_FONT.render(self.text, 1, self.color_active)
        self.passive_text = self.font_passive.render(self.text, 1, BLACK)  # self.color_active
        self.passive_rect = self.passive_text.get_rect(center=self.rect.center)

        self.active_text = self.font_active.render(self.text, 1, BLACK)  # self.color_passive
        self.active_rect = self.active_text.get_rect(center=self.rect.center)

    def handle_event(self, event):
        """Check all events and change variables - without drawing and rendering"""

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.clicked = True
                # if self.function:
                #    self.function()

        if event.type == pygame.MOUSEBUTTONUP:
            if self.hovered:
                self.clicked = False
                # run function when button is released
                if self.function:
                    self.function()

    def draw(self, win):  # Third argument can be: outline=None
        """Draw rectangle and text but don't render text"""

        # if outline:
        #     pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        #
        # pygame.draw.rect(win, self.color_passive, (self.x, self.y, self.width, self.height), 0)

        if self.hovered:
            # shadow
            pygame.draw.rect(win, self.color_passive, self.shadow_rect)
            # rect
            if self.clicked:
                pygame.draw.rect(win, self.color_click, self.rect)
            else:
                pygame.draw.rect(win, self.color_active, self.rect)
            # text
            win.blit(self.active_text, self.active_rect)
        else:
            # rect
            pygame.draw.rect(win, self.color_passive, self.rect)
            # text
            win.blit(self.passive_text, self.passive_rect)

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


# defining the function to draw text on the screen
def draw_text(surface, text, pos):
    # font = pygame.font.SysFont('Times New Roman', 24)
    image = LETTER_FONT.render(text, 1, WHITE)

    surface.blit(image, pos)

    # OPTIONS PAGE TITLES
    instructionstext = WORD_FONT.render("How to Play", 1, WHITE)
    win.blit(instructionstext, (WIDTH/2 - instructionstext.get_width()/2, 10))

    settingstext = WORD_FONT.render("Settings", 1, WHITE)
    win.blit(settingstext, (WIDTH/2 - settingstext.get_width()/2, 310))

    # OPTIONS PAGE INSTRUCTIONS
    # y = 20 gap, 25 gap, 30 gap
    firststep = TEXT_FONT.render("1. Try to guess the randomly selected english word", 1, WHITE)
    win.blit(firststep, (WIDTH/2 - firststep.get_width()/2, 62.5))

    secondstep = TEXT_FONT.render("2. The blank line represents each letter of the word", 1, WHITE)
    win.blit(secondstep, (WIDTH/2 - secondstep.get_width()/2, 92.5))

    thirdstep = TEXT_FONT.render("3. You have to guess the letters, each letter can be selected once", 1, WHITE)
    win.blit(thirdstep, (WIDTH/2 - thirdstep.get_width()/2, 122.5))

    fourthstep = TEXT_FONT.render("4. If you guess the letter correctly the letter will fill in the blank", 1, WHITE)
    win.blit(fourthstep, (WIDTH/2 - fourthstep.get_width()/2, 152.5))

    fifthstep = TEXT_FONT.render("5. If you guess the letter wrong, part of the \"hangman\" will be drawn", 1, WHITE)
    win.blit(fifthstep, (WIDTH/2 - fifthstep.get_width()/2, 182.5))

    sixthstep = TEXT_FONT.render("6. You can miss 6 times (\"hangman\" will be fully drawn) before losing the round", 1, WHITE)  # before defeat
    win.blit(sixthstep, (WIDTH/2 - sixthstep.get_width()/2, 212.5))

    seventhstep = TEXT_FONT.render("7. You have 40 seconds to guess the word right or you lose the round", 1, WHITE)
    win.blit(seventhstep, (WIDTH/2 - seventhstep.get_width()/2, 242.5))

    eighthstep = TEXT_FONT.render("8. You win if you guess the correct word", 1, WHITE)
    win.blit(eighthstep, (WIDTH/2 - eighthstep.get_width()/2, 275))

    # OPTIONS PAGE BOTTOM TEXTS
    pausetext = SUB_TEXT_FONT.render("Press \'m/n\' - Mute/Unmute game music", 1, WHITE)
    win.blit(pausetext, (WIDTH/2 - pausetext.get_width()/2, 488))

    # escapekeyleavetext = SUB_TEXT_FONT.render("Press \'ESC\' - Return to Main Menu", 1, WHITE)
    # win.blit(escapekeyleavetext, (WIDTH/2 - escapekeyleavetext.get_width()/2, 525))

# # defining the function to draw titles on the screen
# def draw_title(surface, text, pos):
#     image = TITLE_FONT.render(text, 1, WHITE)
#
#     surface.blit(image, pos)


# # defining the function to draw sub texts (instructions) on the screen
# def draw_sub_text(surface, text, pos):
#     image = TEXT_FONT.render(text, 1, WHITE)
#
#     surface.blit(image, pos)


def on_click_1():
    global text

    if text == text1:
        text = text2
        mutebutton.text = 'Unmute'
        mutebutton.render_text()
    else:
        text = text1
        mutebutton.text = 'Mute'
        mutebutton.render_text()


def on_click_2():
    global text

    if text == "text1":
        text = "text2"
    else:
        text = "text1"


def restart():
    global guessed
    global hangman_status
    global word
    global letters
    # global game_counter
    global counter

    guessed = []
    hangman_status = 0
    word = random.choice(words)
    # game_counter = 21  # 20
    counter = 40  # 41
    for letter in letters:
        letter[3] = True
    # game()


pause = False


def unpause():
    global pause
    pause = False


def paused():
    continuebutton = Button(PRIMARY_COLOR, 275, 100, 250, 100, 'Continue')
    # restart button
    restartbutton = Button(PRIMARY_COLOR, 275, 225, 250, 100, 'Restart')
    quitbutton = Button(PRIMARY_COLOR, 200, 500, 400, 75, 'Quit to Main Menu')  # Return to Main Menu

    while pause:
        win.fill(DARK_THEME_PRIMARY)  # dark mode primary color
        continuebutton.draw(win, WHITE)
        # restart button
        restartbutton.draw(win, WHITE)
        quitbutton.draw(win, WHITE)

        text = TITLE_FONT.render("Paused", 1, WHITE)
        win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continuebutton.isOver(pos):
                    unpause()  # unpause game by clicking on continue
                # restart button worked but after restart new game 'ESC' took to paused menu
                if restartbutton.isOver(pos):
                    restart()
                    game()
                if quitbutton.isOver(pos):
                    main_menu()
            if event.type == pygame.MOUSEMOTION:
                if continuebutton.isOver(pos):
                    continuebutton.color = BUTTON_HOVER_COLOR
                else:
                    continuebutton.color = PRIMARY_COLOR
                # restart button
                if restartbutton.isOver(pos):
                    restartbutton.color = BUTTON_HOVER_COLOR
                else:
                    restartbutton.color = PRIMARY_COLOR
                if quitbutton.isOver(pos):
                    quitbutton.color = BUTTON_HOVER_COLOR
                else:
                    quitbutton.color = PRIMARY_COLOR
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_p:
                    unpause()  # unpause with key p in paused menu
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()

        pygame.display.update()
        pygame.time.Clock().tick(60)


def main_menu():
    playbutton = Button(PRIMARY_COLOR, 275, 100, 250, 100, 'New Game')  # Play/Start New Game
    optionsbutton = Button(PRIMARY_COLOR, 275, 225, 250, 75, 'Options')  # How To Play
    creditsbutton = Button(PRIMARY_COLOR, 275, 325, 250, 75, 'Credits')
    exitbutton = Button(PRIMARY_COLOR, 275, 500, 250, 50, 'Exit')

    while True:
        win.fill(DARK_THEME_PRIMARY)  # dark mode primary color
        playbutton.draw(win, WHITE)
        optionsbutton.draw(win, WHITE)
        creditsbutton.draw(win, WHITE)
        exitbutton.draw(win, WHITE)

        text = TITLE_FONT.render("Main Menu", 1, WHITE)
        # textrect = text.get_rect()
        # textrect.topleft = (275, 20)
        win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

        text = SUB_TEXT_FONT.render("Press \'ESC\' to Exit", 1, WHITE)
        # textrect = text.get_rect()
        # textrect.topleft = (337.5, 572.5)
        win.blit(text, (WIDTH/2 - text.get_width()/2, 572.5))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playbutton.isOver(pos):
                    restart()  # can be after game() too
                    game()
                if optionsbutton.isOver(pos):
                    options()
                if creditsbutton.isOver(pos):
                    gamecredits()
                if exitbutton.isOver(pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if playbutton.isOver(pos):
                    playbutton.color = BUTTON_HOVER_COLOR
                else:
                    playbutton.color = PRIMARY_COLOR
                if optionsbutton.isOver(pos):
                    optionsbutton.color = BUTTON_HOVER_COLOR
                else:
                    optionsbutton.color = PRIMARY_COLOR
                if creditsbutton.isOver(pos):
                    creditsbutton.color = BUTTON_HOVER_COLOR
                else:
                    creditsbutton.color = PRIMARY_COLOR
                if exitbutton.isOver(pos):
                    exitbutton.color = BUTTON_HOVER_COLOR
                else:
                    exitbutton.color = PRIMARY_COLOR
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()

        pygame.display.update()
        pygame.time.Clock().tick(60)


pausegamebutton = ButtonSecondary(PRIMARY_COLOR, BUTTON_HOVER_COLOR, PRIMARY_COLOR, 'Pause', 52.5, 525, 170, 60)
playagainbutton = ButtonSecondary(SECONDARY_COLOR, BUTTON_HOVER_COLOR_SECONDARY, SECONDARY_COLOR, 'Play Again', 247.5, 440, 300, 100)
# game_counter = 20
# game_timer_countdown = COUNTDOWN_TIMER_FONT.render(str(game_counter), True, PRIMARY_COLOR)

def game():
    global hangman_status
    global pause
    # global game_counter
    # global game_timer_countdown
    global counter
    global timer_countdown
    global timer_event

    # Setup game loop
    # define game speed
    FPS = 60
    clock = pygame.time.Clock()

    # Only set this var to false once we lose or quit/exiting the game
    run = True  # controls the upcoming while loop

    # game_timer_event = pygame.USEREVENT + 1
    # pygame.time.set_timer(game_timer_event, 1000)

    counter = 40
    timer_countdown = COUNTDOWN_TIMER_FONT.render(str(counter), True, PRIMARY_COLOR)
    # timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    while run:
        clock.tick(FPS)
        # check for events in while loop (trigger events)
        for event in pygame.event.get():
            # if event.type == game_timer_event:
            #     game_counter -= 1
            #     game_timer_countdown = COUNTDOWN_TIMER_FONT.render(str(game_counter), True, PRIMARY_COLOR)
            #     if game_counter == 0:
            #         pygame.time.set_timer(game_timer_event, 0)  # set to 0 - visible if we don't call main_menu() as example
            #         display_message("TIME'S UP! You LOST!")
            if event.type == timer_event:
                counter -= 1
                timer_countdown = COUNTDOWN_TIMER_FONT.render(str(counter), True, PRIMARY_COLOR)
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)  # set to 0 - visible if we don't call main_menu() as example
                    display_message("TIME'S UP! You LOST!")
            if event.type == QUIT:
                # run = False - pressing X in the top right corner takes back to Main Menu
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    main_menu()  # paused menu restart button -> 'ESC' in new game took to paused so had to add this line
                if event.key == K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()
            # register mouse events
            if event.type == MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                # print(pos)  # get x and y pos of mouse in the window => check if pressed on button
                for letter in letters:
                    x, y, ltr, visible = letter
                    # distance
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            pygame.mixer.Sound.play(soft_click)
                            # print(ltr)
                            letter[3] = False  # letter[3] is the True value/visibility of the letter
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                pos = pygame.mouse.get_pos()
                if pausegamebutton.isOver(pos):
                    pause = True
                    paused()
            pausegamebutton.handle_event(event)

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            # print("won")
            display_message("You WON!")
            # break
            # main_menu()  # because of restart button otherwise break works fine

        if hangman_status == 6:
            # print("lost")
            display_message("You LOST!")
            # break
            # main_menu()  # because of restart button otherwise break works fine


def options():
    global text
    global text1
    global text2
    global mutebutton
    # global button2

    text1 = "Music on"
    text2 = "Music off"

    text = text1

    # settingstext = "Settings"
    # instructionstext = "How to Play"
    # firststep = "1. Try to guess the randomly selected english word"
    # secondstep = "2. The blank line represents each letter of the word"
    # thirdstep = "3. You have to guess the letters, each letter can be selected once"
    # fourthstep = "4. If you guess the letter correctly the letter will fill in the blank"
    # fifthstep = "5. If you guess the letter wrong, part of the 'hangman' will be drawn"
    # sixthstep = "6. You can miss 6 times before defeat"  # /losing the game
    # seventhstep = "7. You win if you guess the correct word"  # if you guess the word correctly

    # create button only once and assign function which it has to execute when it is pressed
    # text is "something" will show initially that then switch to mute/unmute
    # (89, 89, 89), (212, 200, 235), (0, 200, 0)
    mutebutton = ButtonSecondary(PRIMARY_COLOR, BUTTON_HOVER_COLOR, PRIMARY_COLOR, 'Mute', 150, 370, 250, 100, on_click_1)  # PRIMARY_COLOR, WHITE, BUTTON_HOVER_COLOR
    backbutton = ButtonSecondary(PRIMARY_COLOR, BUTTON_HOVER_COLOR, PRIMARY_COLOR, 'Back', 10, 525, 120, 60)
    # button2 = ButtonSecondary('Press', WIDTH - 435, HEIGHT - 350, on_click_2)

    music_paused = False

    done = False
    # done = True
    # while done:
    while not done:
        win.fill(DARK_THEME_PRIMARY)

        mutebutton.draw(win)
        backbutton.draw(win)
        # button2.draw(win, WHITE)  # win, OUTLINE

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                    on_click_1()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()
                    on_click_1()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if mutebutton.isOver(pos):
                    # Toggle
                    music_paused = not music_paused
                    if music_paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if backbutton.isOver(pos):
                    # done = True
                    main_menu()
            mutebutton.handle_event(event)
            backbutton.handle_event(event)
            # button2.handle_event(event)

        draw_text(win, text, (425, 410))

        # draw_title(win, settingstext, (300, 300))
        # draw_title(win, instructionstext, (275, 10))

        # draw_sub_text(win, firststep, (10, 70))
        # draw_sub_text(win, secondstep, (10, 100))
        # draw_sub_text(win, thirdstep, (10, 130))
        # draw_sub_text(win, fourthstep, (10, 160))
        # draw_sub_text(win, fifthstep, (10, 190))
        # draw_sub_text(win, sixthstep, (10, 220))
        # draw_sub_text(win, seventhstep, (10, 250))

        pygame.display.update()


# another way for options
# def options():
#     mutebutton = Button(PRIMARY_COLOR, 275, 500, 250, 50, 'Mute')
#     win.fill(DARK_THEME_PRIMARY)
#     music_paused = False
#
#     done = False
#     while not done:
#         mutebutton.draw(win, WHITE)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 done = True
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 if mutebutton.isOver(pos):
#                     # Toggle the boolean variable.
#                     music_paused = not music_paused  # music_paused = True
#                     if music_paused:
#                         pygame.mixer.music.pause()
#                     else:
#                         pygame.mixer.music.unpause()
#
#         pygame.display.update()
#         pygame.display.flip()


# closing credits or end credits
def gamecredits():
    game_credits = '''
    Hangman Game made in Python
    Game made by:
    BananaDealer
    Release date:
    2022 January
    Thank you all for playing!
    GitHub:
    https://github.com/BananaaaDealer
    /python-pygame-hangman
    '''
    # Press 'ESC' to return to Main Menu

    backbutton = ButtonSecondary(PRIMARY_COLOR, BUTTON_HOVER_COLOR, PRIMARY_COLOR, 'Back', 10, 525, 120, 60)

    centerx, centery = win.get_rect().centerx, win.get_rect().centery
    deltay = centery + 50  # adjust so it goes below screen start

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if backbutton.isOver(pos):
                    run = False
                    # main_menu()
            backbutton.handle_event(event)

        win.fill(DARK_THEME_PRIMARY)
        deltay -= 0.1
        i = 0
        msg_list = []
        pos_list = []

        for line in game_credits.split('\n'):
            msg = LETTER_FONT.render(line, True, SECONDARY_COLOR)
            msg_list.append(msg)
            pos = msg.get_rect(center=(centerx, centery + deltay + 60 * i))
            pos_list.append(pos)
            i = i + 1

        if centery + deltay < -600:
            run = False  # no repetition - once text scrolls up past screen, over

        # screen.blit(msg, pos)
        for j in range(i):
            win.blit(msg_list[j], pos_list[j])

        backbutton.draw(win)

        # text = SUB_TEXT_FONT.render("Press \'ESC\' to Return to Main Menu", 1, WHITE)
        # win.blit(text, (WIDTH/2 - text.get_width()/2, 550))

        pygame.display.update()


main_menu()
# we pass the while loop we quit pygame => close window
pygame.quit()

