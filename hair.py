from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os
import logging

ASCII_CHARS: Dict[str, List[str]] = {
    'A': ['███████╗', '██╔══██╗', '███████║', '██╔══██║', '██║  ██║', '╚═╝  ╚═╝'],
    'B': ['██████╗ ', '██╔══██╗', '██████╔╝', '██╔══██╗', '██████╔╝', '╚═════╝ '],
    'C': ['██████╗ ', '██╔════╝', '██║     ', '██╔════╝', '╚██████╗', ' ╚═════╝'],
    'D': ['██████╗ ', '██╔══██╗', '██║  ██║', '██╔══██╗', '██████╔╝', '╚═════╝ '],
    'E': ['███████╗', '██╔════╝', '█████╗  ', '██╔══╝  ', '███████╗', '╚══════╝'],
    'F': ['███████╗', '██╔════╝', '█████╗  ', '██╔══╝  ', '██║     ', '╚═╝     '],
    'G': ['██████╗ ', '██╔════╝', '██║  ███╗', '██╔═══██║', '╚██████╔╝', ' ╚═════╝ '],
    'H': ['██╗   ██╗', '██║   ██║', '███████║', '██╔══██║', '██║  ██║', '╚═╝  ╚═╝'],
    'I': ['██╗', '██║', '██║', '██║', '██║', '╚═╝'],
    'J': ['     ██╗', '     ██║', '     ██║', '██   ██║', '╚█████╔╝', ' ╚════╝ '],
    'K': ['██╗  ██╗', '██║ ██╔╝', '█████╔╝ ', '██╔═██╗ ', '██║  ██╗', '╚═╝  ╚═╝'],
    'L': ['██╗     ', '██║     ', '██║     ', '██║     ', '███████╗', '╚══════╝'],
    'M': ['███╗   ███╗', '████╗ ████║', '██╔████╔██║', '██║╚██╔╝██║', '██║ ╚═╝ ██║', '╚═╝     ╚═╝'],
    'N': ['███╗   ██╗', '████╗  ██║', '██╔██╗ ██║', '██║╚██╗██║', '██║ ╚████║', '╚═╝  ╚═══╝'],
    'O': ['██████╗ ', '██╔══██╗', '██║  ██║', '██╔══██╗', '╚██████╔╝', ' ╚═════╝ '],
    'P': ['██████╗ ', '██╔══██╗', '██████╔╝', '██╔═══╝ ', '██║     ', '╚═╝     '],
    'Q': ['██████╗ ', '██╔══██╗', '██║  ██║', '██╔══██╗', '╚██████╔╝', ' ╚═════╝ '],
    'R': ['██████╗ ', '██╔══██╗', '██████╔╝', '██╔══██╗', '██║  ██║', '╚═╝  ╚═╝'],
    'S': ['███████╗', '██╔════╝', '███████╗', '╚════██║', '███████║', '╚══════╝'],
    'T': ['████████╗', '╚══██╔══╝', '   ██║   ', '   ██║   ', '   ██║   ', '   ╚═╝   '],
    'U': ['██╗   ██╗', '██║   ██║', '██║   ██║', '██╔═══██║', '╚██████╔╝', ' ╚═════╝ '],
    'V': ['██╗   ██╗', '██║   ██║', '██║   ██║', '╚██╗ ██╔╝', ' ╚████╔╝ ', '  ╚═══╝  '],
    'W': ['██╗    ██╗', '██║    ██║', '██║ █╗ ██║', '██║███╗██║', '╚███╔███╔╝', ' ╚══╝╚══╝ '],
    'X': ['██╗  ██╗', '╚██╗██╔╝', ' ╚███╔╝ ', ' ██╔██╗ ', '██╔╝ ██╗', '╚═╝  ╚═╝'],
    'Y': ['██╗   ██╗', '╚██╗ ██╔╝', ' ╚████╔╝ ', '  ╚██╔╝  ', '   ██║   ', '   ╚═╝   '],
    'Z': ['███████╗', '╚══███╔╝', '  ███╔╝ ', ' ███╔╝  ', '███████╗', '╚══════╝'],
    ' ': ['   ', '   ', '   ', '   ', '   ', '   ']
}

class ASCIICliManager:
    def __init__(self) -> None:
        self.statistics: Dict[str, int] = {
            'ascii_text_generated': 0,
            'banners_created': 0,
            'menus_created': 0,
            'prompts_created': 0,
            'footers_created': 0,
            'total_operations': 0
        }
        self.operation_history: List[Dict[str, str]] = []
        self.setup_logging()
    
    def setup_logging(self) -> None:
        debug_folder: str = os.path.join(os.path.dirname(__file__), 'debug')
        os.makedirs(debug_folder, exist_ok=True)
        log_file: str = os.path.join(debug_folder, 'ascii_cli_stats.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def log_operation(self, operation_type: str, details: str) -> None:
        self.statistics[f'{operation_type}_created'] += 1
        self.statistics['total_operations'] += 1
        
        operation_record: Dict[str, str] = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation_type,
            'details': details
        }
        self.operation_history.append(operation_record)
        
        self.logger.info(f"Operation: {operation_type} | Details: {details}")
        self.logger.info(f"Statistics: {self.statistics}")

def generate_ascii_text(text: str) -> str:
    if not text.strip():
        return ""
    
    lines: List[str] = ['', '', '', '', '', '']
    for char in text.upper():
        if char in ASCII_CHARS:
            for i in range(6):
                lines[i] += ASCII_CHARS[char][i] + ' '
        else:
            for i in range(6):
                lines[i] += ASCII_CHARS[' '][i] + ' '
    
    cleaned_lines: List[str] = [line.rstrip() for line in lines]
    return '\n'.join(cleaned_lines)

def create_banner(title: str, subtitle: str = "") -> str:
    if not title.strip():
        return ""
    
    ascii_title: str = generate_ascii_text(title)
    lines: List[str] = ascii_title.split('\n')
    
    if not lines:
        return ""
    
    max_line_length: int = max(len(line) for line in lines if line.strip())
    banner_inner_width: int = 78
    
    padded_lines: List[str] = []
    for line in lines:
        line_length: int = len(line)
        if line_length >= banner_inner_width:
            padded_lines.append(f"║{line[:banner_inner_width]}║")
        else:
            padding_needed: int = banner_inner_width - line_length
            left_padding: int = padding_needed // 2
            right_padding: int = padding_needed - left_padding
            centered_line: str = ' ' * left_padding + line + ' ' * right_padding
            padded_lines.append(f"║{centered_line}║")
    
    banner: str = "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    banner += "║                                                                              ║\n"
    if padded_lines:
        banner += '\n'.join(padded_lines) + '\n'
    banner += "║                                                                              ║\n"
    if subtitle and subtitle.strip():
        banner += f"║  {subtitle.center(76)}  ║\n"
        banner += "║                                                                              ║\n"
    banner += "╚══════════════════════════════════════════════════════════════════════════════╝"
    return banner

def create_menu(title: str, items: List[str]) -> str:
    menu: str = f"╭─────────────────────────────────────────────────────────────────────────────╮\n"
    menu += f"│  {title.upper().ljust(75)} │\n"
    menu += f"├─────────────────────────────────────────────────────────────────────────────┤\n"
    menu += f"│                                                                             │\n"
    for i, item in enumerate(items, 1):
        menu += f"│  {i}. {item.ljust(69)} │\n"
    menu += f"│                                                                             │\n"
    menu += f"╰─────────────────────────────────────────────────────────────────────────────╯"
    return menu

def create_prompt(text: str) -> str:
    return f"┌─────────────────────────────────────────────────────────────────────────────┐\n│  {text.upper().ljust(75)} │\n└─────────────────────────────────────────────────────────────────────────────┘"

def create_footer(text: str) -> str:
    return f"╭─────────────────────────────────────────────────────────────────────────────╮\n│  {text.center(75)} │\n╰─────────────────────────────────────────────────────────────────────────────╯"

def validate_input(user_input: str, valid_choices: List[str]) -> bool:
    return user_input.strip() in valid_choices

def save_output_file(content: str, output_type: str) -> str:
    debug_folder: str = os.path.join(os.path.dirname(__file__), 'debug')
    os.makedirs(debug_folder, exist_ok=True)
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path: str = os.path.join(debug_folder, f'ascii_{output_type.lower()}_{timestamp}.txt')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"ASCII Generator Output - {output_type}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("End of Output\n")
    return file_path

def process_ascii_generation(cli_manager: ASCIICliManager) -> None:
    text: str = input("Enter text: ").strip()
    if not text:
        print("Error: Text input cannot be empty")
        return
    
    result: str = generate_ascii_text(text)
    print("\n" + result)
    
    file_path: str = save_output_file(result, "ASCII_Text")
    cli_manager.log_operation("ascii_text", f"Text: '{text}', Length: {len(text)}")
    print("Generated successfully")

def process_banner_creation(cli_manager: ASCIICliManager) -> None:
    title: str = input("Banner title: ").strip()
    if not title:
        print("Error: Title cannot be empty")
        return
    
    subtitle: str = input("Subtitle (optional): ").strip()
    result: str = create_banner(title, subtitle)
    print("\n" + result)
    
    file_path: str = save_output_file(result, "Banner")
    cli_manager.log_operation("banners", f"Title: '{title}', Subtitle: '{subtitle}'")
    print("Banner created successfully")

def process_menu_creation(cli_manager: ASCIICliManager) -> None:
    title: str = input("Menu title: ").strip()
    if not title:
        print("Error: Menu title cannot be empty")
        return
    
    items: List[str] = []
    print("Enter menu items (empty line to finish):")
    while True:
        item: str = input("Item: ").strip()
        if not item:
            break
        items.append(item)
    
    if not items:
        print("Error: Menu must have at least one item")
        return
    
    result: str = create_menu(title, items)
    print("\n" + result)
    
    file_path: str = save_output_file(result, "Menu")
    cli_manager.log_operation("menus", f"Title: '{title}', Items: {len(items)}")
    print("Menu created successfully")

def process_prompt_creation(cli_manager: ASCIICliManager) -> None:
    text: str = input("Prompt text: ").strip()
    if not text:
        print("Error: Prompt text cannot be empty")
        return
    
    result: str = create_prompt(text)
    print("\n" + result)
    
    file_path: str = save_output_file(result, "Prompt")
    cli_manager.log_operation("prompts", f"Text: '{text}'")
    print("Prompt created successfully")

def process_footer_creation(cli_manager: ASCIICliManager) -> None:
    text: str = input("Footer text: ").strip()
    if not text:
        print("Error: Footer text cannot be empty")
        return
    
    result: str = create_footer(text)
    print("\n" + result)
    
    file_path: str = save_output_file(result, "Footer")
    cli_manager.log_operation("footers", f"Text: '{text}'")
    print("Footer created successfully")

def display_clean_menu() -> None:
    menu_items: List[str] = [
        "ASCII Text Generator",
        "Banner Creator", 
        "Menu Builder",
        "Prompt Designer",
        "Footer Generator",
        "Exit Application"
    ]
    print("\n" + create_menu("ASCII CLI GENERATOR", menu_items))

def main() -> None:
    cli_manager: ASCIICliManager = ASCIICliManager()
    valid_choices: List[str] = ['1', '2', '3', '4', '5', '6']
    
    print(create_banner("ASCII CLI", "Enhanced Interface"))
    
    while True:
        display_clean_menu()
        choice: str = input("\nSelect option: ").strip()
        
        if not validate_input(choice, valid_choices):
            print("Invalid selection. Please choose 1-6.")
            continue
        
        if choice == '1':
            process_ascii_generation(cli_manager)
        elif choice == '2':
            process_banner_creation(cli_manager)
        elif choice == '3':
            process_menu_creation(cli_manager)
        elif choice == '4':
            process_prompt_creation(cli_manager)
        elif choice == '5':
            process_footer_creation(cli_manager)
        elif choice == '6':
            print("Session complete")
            break

if __name__ == "__main__":
    main()