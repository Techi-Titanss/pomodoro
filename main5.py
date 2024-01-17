import pygame
import sys
from button import Button
from plyer import notification


pygame.init()
pygame.mixer.init()
history = []


# Load notification sounds

end_notification_sound = pygame.mixer.Sound("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\radar.mp3")

WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")

CLOCK = pygame.time.Clock()

BACKGROUND = pygame.image.load("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\background.png")

WHITE_BUTTON = pygame.image.load("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\button.jfif")

FONT = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 100)
timer_text = FONT.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(WIDTH/2, HEIGHT/2-25))

# Function to display notifications
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Pomodoro Timer",
        timeout=10,  # Notification will disappear after 10 seconds
    )

# Function to show start notification
def show_start_notification():
    show_notification("Pomodoro Timer", "Pomodoro started!")
    

# Function to show end notification
def show_end_notification():
    show_notification("Pomodoro Timer", "Pomodoro ended! Take a break.")
    end_notification_sound.play()





class DropdownMenu:
    def __init__(self, options, position, width, height, font, default_option, title=""):
        self.options = options
        self.visible_options = options[:5]  # Adjust the number of visible options
        self.rect = pygame.Rect(position, (width, height))
        self.font = font
        self.default_option = default_option
        self.selected_option = default_option
        self.is_open = False
        self.title = title
        self.scroll_offset = 0  # New attribute to track the scroll offset
        
        

    def draw(self, screen):
        # Draw the dropdown menu with the title
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Draw the title within the dropdown
        title_font = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 15)
        title_text = title_font.render(self.title, True, (2,2, 2))
        title_rect = title_text.get_rect(center=(self.rect.centerx, self.rect.centery - 2))
        screen.blit(title_text, title_rect)

        # Draw the selected option
        text = self.font.render(self.selected_option, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

        # Check if scrollbar is needed
        if len(self.options) > len(self.visible_options):
            pygame.draw.rect(screen, (200, 200, 200), (self.rect.right - 15, self.rect.top, 15, self.rect.height))
            scroll_button_height = self.rect.height / len(self.options)
            pygame.draw.rect(screen, (100, 100, 100),
                             (self.rect.right - 15, self.rect.top + self.scroll_offset * scroll_button_height,
                              15, scroll_button_height * len(self.visible_options)))

        if self.is_open:
            for i, option in enumerate(self.visible_options):
                option_rect = pygame.Rect(
                    self.rect.left,
                    self.rect.bottom + (i + 1) * self.rect.height,
                    self.rect.width - 15,  # Adjust width to accommodate the scrollbar
                    self.rect.height,
                )
                pygame.draw.rect(screen, (255, 255, 255), option_rect)
                pygame.draw.rect(screen, (0, 0, 0), option_rect, 2)
                option_text = self.font.render(option, True, (0, 0, 0))
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_open = not self.is_open
                elif self.is_open:
                    for i, option in enumerate(self.visible_options):
                        option_rect = pygame.Rect(
                            self.rect.left,
                            self.rect.bottom + (i + 1) * self.rect.height,
                            self.rect.width - 15,  # Adjust width to accommodate the scrollbar
                            self.rect.height,
                        )
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = option
                            self.is_open = False
            elif event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
                self.update_visible_options()
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(len(self.options) - len(self.visible_options), self.scroll_offset + 1)
                self.update_visible_options()

    def update_visible_options(self):
        self.visible_options = self.options[self.scroll_offset:self.scroll_offset + 5]  # Update visible options











    
START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START", 
                    pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#c97676", "#9ab034")
POMODORO_BUTTON = Button(None, (WIDTH/2-150, HEIGHT/2-100), 120, 30, "Pomodoro", 
                    pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (WIDTH/2, HEIGHT/2-100), 120, 30, "Short Break", 
                    pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (WIDTH/2+150, HEIGHT/2-100), 120, 30, "Long Break", 
                    pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")

TIME1_BUTTON = Button(None, (WIDTH / 2 -240, HEIGHT / 2 - 180), 80, 10, "5MINS", 
                      pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
TIME2_BUTTON = Button(None, (WIDTH / 2 - 150, HEIGHT / 2 - 180), 80, 10, "10MINS", 
                      pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
TIME3_BUTTON = Button(None, (WIDTH / 2 - 60, HEIGHT / 2 - 180), 80, 10, "15MINS", 
                      pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
TIME4_BUTTON = Button(None, (WIDTH / 2 +30, HEIGHT / 2 - 180), 80, 10, "30MINS", 
                      pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
TIME5_BUTTON = Button(None, (WIDTH / 2 +120, HEIGHT / 2 - 180), 80, 10, "45MINS", 
                      pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")
TIME6_BUTTON = Button(None, (WIDTH / 2 +210, HEIGHT / 2 - 180), 80, 10, "50MINS", 
                      pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20), "#FFFFFF", "#9ab034")

# Constants for default timings
DEFAULT_POMODORO_LENGTH = 1500 # 1500 secs / 25 mins
DEFAULT_SHORT_BREAK_LENGTH = 300 # 300 secs / 5 mins
DEFAULT_LONG_BREAK_LENGTH = 900 # 900 secs / 15 mins
DEFAULT_TIME1_LENGTH=300
DEFAULT_TIME2_LENGTH=600
DEFAULT_TIME3_LENGTH=900
DEFAULT_TIME4_LENGTH=1800
DEFAULT_TIME5_LENGTH=2700
DEFAULT_TIME6_LENGTH=3000

current_seconds = DEFAULT_POMODORO_LENGTH
pygame.time.set_timer(pygame.USEREVENT, 1000)
started = False

cycle_completed = False




# Define the dropdown menu options
time_options = ["5MINS", "10MINS", "15MINS", "30MINS", "45MINS", "50MINS"]

# Create a dropdown menu
time_dropdown = DropdownMenu(
    options=time_options,
    position=(WIDTH / 2 +150, HEIGHT / 2 +50),
    width=120,
    height=25,
    font=pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 10),
    default_option="Pomodoro",
    title="Timings"
)



while True:

    def get_selected_time_seconds(selected_option):
        time_mappings = {
            "5MINS": DEFAULT_TIME1_LENGTH,
            "10MINS": DEFAULT_TIME2_LENGTH,
            "15MINS": DEFAULT_TIME3_LENGTH,
            "30MINS": DEFAULT_TIME4_LENGTH,
            "45MINS": DEFAULT_TIME5_LENGTH,
            "50MINS": DEFAULT_TIME6_LENGTH,
    }
        return time_mappings.get(selected_option, DEFAULT_POMODORO_LENGTH)


    def update_timer_text(seconds):
        display_seconds = seconds % 60
        display_minutes = int(seconds / 60) % 60
        timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
        SCREEN.blit(timer_text, timer_text_rect)     
        



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                if started:
                    started = False
                else:
                    started = True
                    show_start_notification()  # Add this line to show start notification
          

                
           
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = DEFAULT_POMODORO_LENGTH
                started = False
            if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = DEFAULT_SHORT_BREAK_LENGTH
                started = False
            if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = DEFAULT_LONG_BREAK_LENGTH
                started = False
            if started:
                START_STOP_BUTTON.text_input = "STOP"
                START_STOP_BUTTON.text = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20).render(
                                        START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
            else:
                START_STOP_BUTTON.text_input = "START"
                START_STOP_BUTTON.text = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20).render(
                                        START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
        if event.type == pygame.USEREVENT and started:
            current_seconds -= 1
            
            if current_seconds <= 0 and not cycle_completed:
                show_end_notification()  # Add this line to show end notification



                history.append({
                        'type': '  Pomodoro Cycle completed',
                        'duration': DEFAULT_POMODORO_LENGTH ,
                        })
                cycle_completed = True



   
        time_dropdown.handle_event(event)


        # Check if the dropdown selection has changed
        if time_dropdown.selected_option != "":  # Check if a valid option is selected
            current_seconds = get_selected_time_seconds(time_dropdown.selected_option)
            update_timer_text(current_seconds)
            time_dropdown.selected_option = ""  # Reset the selection to avoid repeated updates








                
  
    if started:
        START_STOP_BUTTON.text_input = "STOP"
        START_STOP_BUTTON.text = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20).render(
                                START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
    else:
        START_STOP_BUTTON.text_input = "START"
        START_STOP_BUTTON.text = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20).render(
                                START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)

    # Reset the flag when starting a new cycle
    if current_seconds == DEFAULT_POMODORO_LENGTH:
        cycle_completed = False




        


    


        
  
    SCREEN.fill("#000000")
    SCREEN.blit(BACKGROUND, BACKGROUND.get_rect(center=(WIDTH/2, HEIGHT/2)))

    START_STOP_BUTTON.update(SCREEN)
    START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
    POMODORO_BUTTON.update(SCREEN)
    POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
    SHORT_BREAK_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    LONG_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    

    # Draw the dropdown menu
    time_dropdown.draw(SCREEN)

    # Modify the existing time buttons to update current_seconds
    if TIME1_BUTTON.check_for_input(pygame.mouse.get_pos()):
        current_seconds = DEFAULT_TIME1_LENGTH
        started = False


    # Display the selected time on the button
    TIME1_BUTTON.text_input = time_dropdown.selected_option
    TIME1_BUTTON.text = pygame.font.Font("C:\\Users\\kanur\\OneDrive\\Desktop\\mini project\\ArialRoundedMTBold.ttf.ttf", 20).render(
    TIME1_BUTTON.text_input, True, TIME1_BUTTON.base_color
    )
    



    

       
    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60
    timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
    SCREEN.blit(timer_text, timer_text_rect)

    history_text = pygame.font.Font(None, 25).render("History:", True, "white")
    SCREEN.blit(history_text, (10, 10))

    y_offset = 40  # Adjust this value based on your layout
    for entry in history:
        history_entry_text = pygame.font.Font(None, 20).render(f"{entry['type']} - {entry['duration']//60} mins", True, "white")
        SCREEN.blit(history_entry_text, (10, y_offset))
        y_offset += 25  # Adjust this value based on your layout

        
    pygame.display.update()

