# These are very close, but will take some time to center, and also the right edges
# This is still in development but very close
# Save the prompts above for reference, they came close but needed some adjustments to look good
ASCII_CHARS = {
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

def generate_ascii_text(text):
    lines = ['', '', '', '', '', '']
    for char in text.upper():
        if char in ASCII_CHARS:
            for i in range(6):
                lines[i] += ASCII_CHARS[char][i] + ' '
    return '\n'.join(lines)

def create_banner(title, subtitle=""):
    ascii_title = generate_ascii_text(title)
    lines = ascii_title.split('\n')
    padded_lines = []
    for line in lines:
        padded_lines.append(f"║  {line.ljust(76)}  ║")
    
    banner = "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    banner += "║                                                                              ║\n"
    banner += '\n'.join(padded_lines) + '\n'
    banner += "║                                                                              ║\n"
    if subtitle:
        banner += f"║  {subtitle.center(76)}  ║\n"
        banner += "║                                                                              ║\n"
    banner += "╚══════════════════════════════════════════════════════════════════════════════╝"
    return banner

def create_menu(title, items):
    menu = f"╭─────────────────────────────────────────────────────────────────────────────╮\n"
    menu += f"│  {title.upper().ljust(75)} │\n"
    menu += f"├─────────────────────────────────────────────────────────────────────────────┤\n"
    menu += f"│                                                                             │\n"
    for i, item in enumerate(items, 1):
        menu += f"│  {i}. {item.ljust(69)} │\n"
    menu += f"│                                                                             │\n"
    menu += f"╰─────────────────────────────────────────────────────────────────────────────╯"
    return menu

def create_prompt(text):
    return f"┌─────────────────────────────────────────────────────────────────────────────┐\n│  {text.upper().ljust(75)} │\n└─────────────────────────────────────────────────────────────────────────────┘"

def create_footer(text):
    return f"╭─────────────────────────────────────────────────────────────────────────────╮\n│  {text.center(75)} │\n╰─────────────────────────────────────────────────────────────────────────────╯"

def save_to_file(content, output_type):
    import os
    from datetime import datetime
    debug_folder = os.path.join(os.path.dirname(__file__), 'debug')
    os.makedirs(debug_folder, exist_ok=True)
    file_path = os.path.join(debug_folder, 'ascii_output.txt')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"ASCII Generator Output - {output_type}\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("End of Output\n")
    return file_path

def main():
    while True:
        print("\nASCII Generator - Choose an option:")
        print("1. ASCII Text")
        print("2. Banner")
        print("3. Menu")
        print("4. Prompt")
        print("5. Footer")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            text = input("Enter text: ")
            result = generate_ascii_text(text)
            print("\n" + result)
            file_path = save_to_file(result, "ASCII Text")
            print(f"Output saved to: {file_path}")
        elif choice == '2':
            title = input("Banner title: ")
            subtitle = input("Subtitle (optional): ")
            result = create_banner(title, subtitle)
            print("\n" + result)
            file_path = save_to_file(result, "Banner")
            print(f"Output saved to: {file_path}")
        elif choice == '3':
            title = input("Menu title: ")
            items = []
            print("Enter menu items (empty line to finish):")
            while True:
                item = input("Item: ")
                if not item:
                    break
                items.append(item)
            if items:
                result = create_menu(title, items)
                print("\n" + result)
                file_path = save_to_file(result, "Menu")
                print(f"Output saved to: {file_path}")
        elif choice == '4':
            text = input("Prompt text: ")
            result = create_prompt(text)
            print("\n" + result)
            file_path = save_to_file(result, "Prompt")
            print(f"Output saved to: {file_path}")
        elif choice == '5':
            text = input("Footer text: ")
            result = create_footer(text)
            print("\n" + result)
            file_path = save_to_file(result, "Footer")
            print(f"Output saved to: {file_path}")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()