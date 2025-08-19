import random
import time

class ImpostorGame:
    def __init__(self):
        self.concepts = [
            "Pizza", "Ocean", "Mountain", "Library", "Bicycle", "Rainbow", 
            "Coffee", "Guitar", "Sunset", "Garden", "Castle", "River",
            "Telescope", "Bakery", "Lighthouse", "Forest", "Butterfly", 
            "Campfire", "Snowflake", "Waterfall", "Stadium", "Museum",
            "Airplane", "Kitchen", "Playground", "Market", "Beach"
        ]
        self.players = []
        self.secret_word = ""
        self.impostor = ""

    def setup_game(self):
        """Set up the game with player names and select impostor"""
        print("🕵️  IMPOSTOR WORD GAME  🕵️")
        print("=" * 30)
        
        # Get number of players
        while True:
            try:
                num_players = int(input("Enter number of players (3-10): "))
                if 3 <= num_players <= 10:
                    break
                else:
                    print("Please enter a number between 3 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get player names
        print("\nEnter player names:")
        for i in range(num_players):
            name = input(f"Player {i+1}: ").strip()
            if not name:
                name = f"Player {i+1}"
            self.players.append(name)
        
        # Select random word and impostor
        self.secret_word = random.choice(self.concepts)
        self.impostor = random.choice(self.players)
        
        print(f"\n✅ Game setup complete! {len(self.players)} players ready.")
        print("\nPress Enter to start distributing roles...")
        input()

    def distribute_roles(self):
        """Give each player their role individually"""
        print("\n" + "="*50)
        print("ROLE DISTRIBUTION - PLAYERS TAKE TURNS")
        print("="*50)
        print("\nEach player should look at the screen alone!")
        print("Others should look away during each turn.\n")
        
        for player in self.players:
            input(f"📱 {player}, press Enter when you're ready to see your role...")
            
            # Clear screen effect
            print("\n" * 20)
            
            if player == self.impostor:
                print("🔴 " + "="*30)
                print(f"   Hello {player}!")
                print("   YOU ARE THE IMPOSTOR")
                print("   Try to blend in without knowing the word!")
                print("="*30 + " 🔴")
            else:
                print("🟢 " + "="*30)
                print(f"   Hello {player}!")
                print(f"   Your word is: {self.secret_word.upper()}")
                print("   Try to find the impostor!")
                print("="*30 + " 🟢")
            
            print("\n⚠️  Remember your role and pass the device!")
            input("Press Enter when done (others can look again)...")
            print("\n" * 20)

    def reveal_results(self):
        """Show the results after the game"""
        print("\n" + "🎭 GAME RESULTS 🎭".center(40, "="))
        print(f"\n🎯 The secret word was: {self.secret_word.upper()}")
        print(f"🕵️  The impostor was: {self.impostor.upper()}")
        print("\n" + "="*40)
        
        print("\n📝 HOW TO PLAY:")
        print("1. Players discuss the word without saying it directly")
        print("2. Give hints, ask questions, but be subtle!")
        print("3. The impostor tries to blend in")
        print("4. After discussion, vote for who you think is the impostor")
        print("5. Impostor wins if they're not caught!")



    def show_results_menu(self):
        """Show menu after role distribution"""
        print("\n" + "🎮 GAME MENU 🎮".center(40, "="))
        print("\n🎯 All players have received their roles!")
        print("\nWhat would you like to do?")
        print("📊 Type 'results' to see the answer")
        print("🔄 Type 'new' for a new round with same players")
        print("❌ Type 'quit' to exit")
        
        while True:
            choice = input("\nYour choice: ").lower().strip()
            if choice == 'results':
                return 'results'
            elif choice == 'new':
                return 'new'
            elif choice == 'quit':
                return 'quit'
            else:
                print("Please enter 'results', 'new', or 'quit'")

    def run_game(self):
        """Main game loop"""
        # First setup - get players
        self.setup_game()
        
        while True:
            # Start new round with existing players
            self.secret_word = random.choice(self.concepts)
            self.impostor = random.choice(self.players)
            
            # Distribute roles
            self.distribute_roles()
            
            # Show menu instead of automatic results
            choice = self.show_results_menu()
            
            if choice == 'results':
                self.reveal_results()
                # After showing results, ask what to do next
                next_choice = self.show_results_menu()
                if next_choice == 'quit':
                    break
                elif next_choice == 'results':
                    continue  # Show menu again
                # If 'new', continue to next iteration
            elif choice == 'quit':
                break
            # If 'new', continue to next iteration
        
        print("\n👋 Thanks for playing Impostor Word Game!")

# Run the game
if __name__ == "__main__":
    game = ImpostorGame()
    game.run_game()