import os
import re
import random
import pickle
import time
from datetime import datetime
from abc import ABC, abstractmethod
from functools import reduce
from typing import List, Dict, Tuple, Set
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

def clear_screen():
    """Clear the console screen for better readability"""
    os.system('cls' if os.name == 'nt' else 'clear')  #cls= clear screen

def typewriter_effect(text: str, delay: float = 0.03) -> None:
    """Print text with a typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_banner(text: str, color: str = Fore.CYAN, decoration: str = "=") -> None:
    """Print a decorated banner with the given text"""
    width = 60
    print(color + decoration * width)
    print(color + text.center(width))
    print(color + decoration * width)

class AsciiArt:
    DETECTIVE = f"""{Fore.YELLOW}
    ,/         \.
   ((           ))
    \\..--,./
     `..-.,'
      .-'`-.
    /`     _ \\
   /     _(  `\\
  |     ( `),  )
  |\     "  /
  \ \        /
   \ \    _,/
    \\_.-
    """

    COMPUTER = f"""{Fore.CYAN}
     .-------------------.
     |  >_              |
     |                  |
     | Python Detective |
     |                  |
     |                  |
     '---||------------'
         ||
    """

    MAGNIFYING_GLASS = f"""{Fore.WHITE}
     .--.
    /      \\
   |        |
    \      /
     `-..-'
       ||
       ||
       ||
       ||
    """

    EVIDENCE = f"""{Fore.GREEN}  .-========-,
    //|
    |   TOP   | |
    | SECRET  | |
    |         | |
    |_|/
    """

    SUSPECTS = f"""{Fore.RED}
      .---.    .---.    .---.
     /    |   /    |   /    |
    | .--.'  | .--.'  | .--.'
    | |      | |      | |
    | '--'   | '--'   | '--'
    '----'   '----'   '----'
    """

# Game configuration with character backgrounds
GAME_CONFIG = {
    'max_attempts': 3,
    'difficulty_levels': ('easy', 'medium', 'hard'),
    'score_multiplier': 1.5
}

SUSPECT_PROFILES = {
    'Alex Johnson': {
        'occupation': 'Python Instructor','age': 28,
        'background': 'A brilliant but sometimes mysterious coding instructor',
        'alibi': 'Was teaching an advanced Python class from 7 PM to 10 PM',
        'suspicious_traits': 'Known for creating complex encryption algorithms',
        'color': Fore.RED
    },
    'Blake Rodriguez': {
        'occupation': 'Software Developer',
        'age': 31,
        'background': 'A competitive programmer with multiple hackathon wins',
        'alibi': 'Was participating in an online coding competition',
        'suspicious_traits': 'Has deep knowledge of cybersecurity',
        'color': Fore.BLUE
    },
    'Casey Thompson': {
        'occupation': 'System Administrator',
        'age': 35,
        'background': 'Expert in system architecture and network security',
        'alibi': 'Was debugging a critical production issue',
        'suspicious_traits': 'Has access to all company servers',
        'color': Fore.GREEN
    }
}
class GameCharacter(ABC):
    def __init__(self, name: str, role: str):
        self._name = name  # Protected attribute
        self.__role = role  # Private attribute
        self.is_suspicious = False

    @property  #abstract
    def name(self) -> str:
        return self._name

    @abstractmethod
    def get_description(self) -> str:
        pass

class Suspect(GameCharacter):
    def __init__(self, name: str, profile: dict):
        super().__init__(name, "suspect")
        self.profile = profile
        self.clues: List[str] = []
        self.times_interrogated = 0

    def get_description(self) -> str:
        border = f"{Fore.CYAN}{'═' * 50}"
        return f"""
{border}
{Fore.YELLOW}┌── Suspect Profile: {self._name} ──┐
{Fore.WHITE}│ Occupation: {self.profile['occupation']}
│ Age: {self.profile['age']}
│ Background: {self.profile['background']}
│ Alibi: {self.profile['alibi']}
│ Notable: {self.profile['suspicious_traits']}
{Fore.YELLOW}└{'─' * (len(self._name) + 18)}┘
{border}"""

    def get_interrogation_response(self) -> str:
        self.times_interrogated += 1
        
        if self.is_suspicious:
            responses = [
                f"{Fore.RED}Nervously adjusts collar{Fore.WHITE} 'I... I was just doing my regular work that night.'",
                f"{Fore.RED}Avoids eye contact{Fore.WHITE} 'Check the logs if you don't believe me...'",
                f"{Fore.RED}Defensive tone{Fore.WHITE} 'Don't you need a warrant or something?'"
            ]
        else:
            responses = [
                f"{Fore.GREEN}Calmly explains{Fore.WHITE} 'I have nothing to hide. Check my alibi.'",
                f"{Fore.GREEN}Shows cooperation{Fore.WHITE} 'Happy to help with the investigation.'",
                f"{Fore.GREEN}Provides details{Fore.WHITE} 'I can show you my activity logs for that night.'"
            ]
        return f"""
{Fore.CYAN}╔{'═' * 48}╗
║{' ' * 48}║
║{random.choice(responses).center(48)}║
║{' ' * 48}║
╚{'═' * 48}╝
"""

class Detective:
    def __init__(self):
        self.evidence_log: List[str] = []
        self.score: float = 0.0
        self.name: str = ""
        
    def display_badge(self):
        return f"""
{Fore.YELLOW}    ._.
    |   |
    |   |    {Fore.WHITE}Detective Badge
    |   |    {Fore.CYAN}{self.name}
    |   |    {Fore.WHITE}Python Police Department
    |_|    {Fore.YELLOW}Badge #: {random.randint(1000, 9999)}
"""
class PythonDetectiveGame:
    def __init__(self):
        self.suspects: Dict[str, Suspect] = {}
        self.detective = Detective()
        self.current_level = 0
        self.__initialize_suspects()

    def __initialize_suspects(self) -> None:
        self.suspects = {
            name: Suspect(name, profile) 
            for name, profile in SUSPECT_PROFILES.items()
        }
        
        guilty_suspect = random.choice(list(self.suspects.keys()))
        self.suspects[guilty_suspect].is_suspicious = True

    def show_loading_animation(self):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for _ in range(20):
            for frame in frames:
                print(f"\r{Fore.CYAN}Loading {frame}", end="")
                time.sleep(0.1)
        print("\r" + " " * 20 + "\r")   #\r shifts cursosor to the beginning of the line

    def show_main_title(self):
        title = f"""
{Fore.CYAN}
██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                      
{Fore.YELLOW}
██████╗ ███████╗████████╗███████╗ ██████╗████████╗██╗██╗   ██╗███████╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██║██║   ██║██╔════╝
██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║██║   ██║█████╗  
██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║╚██╗ ██╔╝██╔══╝  
██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ██║ ╚████╔╝ ███████╗
╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝"""
        print(title)
        print(f"\n{Fore.CYAN}{'=' * 80}")

    def show_tutorial(self):
        clear_screen()
        self.show_main_title()
        print(AsciiArt.DETECTIVE)
        print(f"\n{Fore.YELLOW}=== PYTHON DETECTIVE: TUTORIAL ===")
        tutorial_text = """
Welcome, Detective! A cybercrime has occurred, and we need your help to catch the culprit.

Here's how to play:"""
        typewriter_effect(tutorial_text)
        
        instructions = [
            ("🔍 SEARCH FOR CLUES", "Investigate the crime scene for evidence"),
            ("👤 INTERROGATE SUSPECTS", "Question each suspect to find inconsistencies"),
            ("📋 VIEW EVIDENCE", "Review all the clues you've gathered"),
            ("💾 SAVE/LOAD", "Save your progress or continue a previous investigation"),
            ("⚖  MAKE AN ACCUSATION", "When you're ready, accuse who you think is guilty")
        ]

        for icon, desc in instructions:
            print(f"\n{Fore.CYAN}{icon}: {Fore.WHITE}{desc}")
            time.sleep(1.5)

    def show_case_briefing(self):
        clear_screen()
        print(AsciiArt.COMPUTER)
        print(f"{Fore.RED}=== CASE BRIEFING ===")
        briefing_text = """
Location: Tech Start-up Office
Time: Last night, between 11 PM and 2 AM
Crime: A sophisticated cyber attack was launched from within the building

The perpetrator:
- Has advanced Python programming skills
- Had access to the building last night
- Left traces of their code behind"""
        typewriter_effect(briefing_text)

    def display_menu(self):
        menu = f"""
{Fore.CYAN}
╔════════════════════════════════╗
║      DETECTIVE'S CONSOLE       ║
╚════════════════════════════════╝

{Fore.YELLOW}1. 🔍 Search for clues
{Fore.GREEN}2. 👤 Interrogate a suspect
{Fore.BLUE}3. 📋 View evidence log
{Fore.MAGENTA}4. 💾 Save investigation
{Fore.RED}5. 📂 Load investigation
{Fore.WHITE}6. ⚖  Make an accusation
{Fore.LIGHTRED_EX}7. 🚪 Exit investigation
"""
        print(menu)

    def search_clues(self) -> str:
        print(AsciiArt.MAGNIFYING_GLASS)
        print(f"{Fore.YELLOW}Searching for clues...\n")
        
        clue_types = [
            {
                'type': f"{Fore.BLUE}Code Fragment",
                'descriptions': [
                    "A Python script using advanced encryption",
                    "Suspicious network scanning code",
                    "An unusually complex algorithm implementation"
                ]
            },
            {
                'type': f"{Fore.GREEN}Digital Evidence",
                'descriptions': [
                    "Unusual login patterns in the server logs",
                    "Modified system files with recent timestamps",
                    "Encrypted communications in the network logs"
                ]
            },
            {
                'type': f"{Fore.MAGENTA}Physical Evidence",
                'descriptions': [
                    "Coffee cup with Python code sketches",
                    "Sticky note with suspicious IP addresses",
                    "Whiteboard with algorithm diagrams"
                ]
            }
        ]
        
        clue_type = random.choice(clue_types)
        clue_desc = random.choice(clue_type['descriptions'])
        
        # Animation for searching
        for _ in range(3):
            print(f"{Fore.CYAN}Analyzing evidence...", end='\r')
            time.sleep(0.3)
            print(f"{Fore.CYAN}Processing data...  ", end='\r')
            time.sleep(0.3)
        
        return f"{clue_type['type']}: {Fore.WHITE}{clue_desc}"

    def save_game_state(self) -> None:
        print(f"\n{Fore.CYAN}Saving investigation state...")
        try:
            with open('investigation_state.pkl', 'wb') as f:
                pickle.dump({
                    'detective': self.detective,
                    'suspects': self.suspects,
                    'level': self.current_level
                }, f)
            print(f"{Fore.GREEN}✓ Investigation saved successfully!")
        except Exception as e:
            print(f"{Fore.RED}Error saving investigation state: {e}")

    def load_game_state(self) -> bool:
        print(f"\n{Fore.CYAN}Loading previous investigation...")
        try:
            with open('investigation_state.pkl', 'rb') as f:
                game_state = pickle.load(f)
                self.detective = game_state['detective']
                self.suspects = game_state['suspects']
                self.current_level = game_state['level']
            print(f"{Fore.GREEN}✓ Investigation loaded successfully!")
            return True
        except FileNotFoundError:
            print(f"{Fore.RED}✗ No saved investigation found.")
            return False
        except Exception as e:
            print(f"{Fore.RED}Error loading investigation state: {e}")
            return False

    def interrogate_suspect(self) -> None:
        clear_screen()
        print(AsciiArt.SUSPECTS)
        print(f"{Fore.YELLOW}=== SUSPECT LIST ===")
        for i, suspect_name in enumerate(self.suspects.keys(), 1):
            print(f"{Fore.CYAN}{i}. {suspect_name}")
        
        try:
            choice = int(input(f"\n{Fore.WHITE}Select a suspect to interrogate (1-{len(self.suspects)}): "))
            if choice < 1 or choice > len(self.suspects):
                print(f"{Fore.RED}Invalid choice. Please try again.")
                return
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.")
            return
        
        suspect = list(self.suspects.values())[choice - 1]
        clear_screen()
        print(suspect.get_description())
        print(suspect.get_interrogation_response())
        
        if suspect.is_suspicious:
            print(f"{Fore.RED}This suspect seems nervous...")
        else:
            print(f"{Fore.GREEN}This suspect seems cooperative...")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")

    def view_evidence_log(self) -> None:
        clear_screen() 
        print(AsciiArt.EVIDENCE)
        print(f"{Fore.YELLOW}=== EVIDENCE LOG ===")
        if not self.detective.evidence_log:
            print(f"{Fore.RED}No evidence collected yet.")
        else:
            for i, evidence in enumerate(self.detective.evidence_log, 1):
                print(f"{Fore.CYAN}{i}. {evidence}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")

    def make_accusation(self) -> bool:
        clear_screen()
        print(AsciiArt.SUSPECTS)
        print(f"{Fore.YELLOW}=== MAKE AN ACCUSATION ===")
        for i, suspect_name in enumerate(self.suspects.keys(), 1):
            print(f"{Fore.CYAN}{i}. {suspect_name}")
        
        try:
            choice = int(input(f"\n{Fore.WHITE}Select the suspect you believe is guilty (1-{len(self.suspects)}): "))
            if choice < 1 or choice > len(self.suspects):
                print(f"{Fore.RED}Invalid choice. Please try again.")
                return False
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.")
            return False
        
        accused_suspect = list(self.suspects.values())[choice - 1]
        if accused_suspect.is_suspicious:
            print(f"{Fore.GREEN}Congratulations! You've caught the culprit!")
            return True
        else:
            print(f"{Fore.RED}Wrong accusation! The real culprit is still at large.")
            return False

    def run(self) -> None:
        clear_screen()
        self.show_main_title()
        self.show_tutorial()
        self.show_case_briefing()
        
        self.detective.name = input(f"\n{Fore.CYAN}Enter your detective's name: ")
        clear_screen()
        
        while True:
            self.display_menu()
            try:
                choice = int(input(f"{Fore.WHITE}Select an option (1-7): "))
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.")
                continue
            
            if choice == 1:
                clue = self.search_clues()
                self.detective.evidence_log.append(clue)
                print(f"\n{Fore.GREEN}Clue found: {clue}")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            elif choice == 2:
                self.interrogate_suspect()
            elif choice == 3:
                self.view_evidence_log()
            elif choice == 4:
                self.save_game_state()
            elif choice == 5:
                if self.load_game_state():
                    print(f"{Fore.GREEN}Game state loaded successfully!")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            elif choice == 6:
                if self.make_accusation():
                    break
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            elif choice == 7:
                print(f"{Fore.YELLOW}Exiting the game. Goodbye!")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")

if __name__ == "__main__":
    game = PythonDetectiveGame()
    game.run()