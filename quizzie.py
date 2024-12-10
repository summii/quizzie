import requests
import random
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint
from difflib import SequenceMatcher

class QuizzieGame():
    def __init__(self):
        self.console = Console()
        self.categories = ["History", "Geography", "Arts", "Sports"]

        # self.points = [100, 200, 300, 400, 500]
        # self.board = {}
        # self.score = 0

    def generate_question(self, category):
        """Generate a question for the given category using ollama"""
        prompt = f"""Generate a {category} trivia question related to country india.Respond with only question on one line, followed by the answer on the next line.
        Make it challenging and interesting.
        """
        print(prompt)
        try:
            response = requests.post('http://localhost:11434/api/generate',
                                     json = {
                                         "model": "mistral",
                                         "prompt": prompt,
                                         "stream": False
                                     })
            response.raise_for_status()
            result = response.json()

            #split the response into question and answer
            lines = result['response'].strip().split('\n')
            if len(lines) >= 2:
                question = lines[0].strip()
                answer = lines[1].strip()

                #Remove common prefixes
                answer = answer.lower().replace('answer:', '').replace('a:', '').strip()
                return {
                    "question": question,
                    "answer": answer
                }
        except Exception as e:
            print(f"Error generating question: {e}")
            return None
        
    def check_answer(self, user_answer, correct_answer):
        """Check the user's answer against the correct answer using the robust matching strategy
        Args:
        user_answer: The user's answer
        correct_answer: The correct answer

        Returns:
        True if the answer is correct, False otherwise
        """
        player_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()

        #direct match
        if player_answer == correct_answer:
            return True
        
        similarity = SequenceMatcher(None, player_answer, correct_answer).ratio()
        if similarity >= 0.8:
            return True
        
        #Handle cases where one answer is more specific version of the other
        player_words = player_answer.split()
        correct_words = correct_answer.split()

        important_words = {word for word in correct_words if len(word) > 3}

        if important_words and important_words.issubset(player_words):
            return True
        return False
    
    def play_game(self):
        while True:
            try:
                # Ask if user wants to continue
                play_choice = Prompt.ask("\nDo you want to play? (yes/no)").lower()
                if play_choice != 'yes':
                    rprint("[yellow]Thanks for playing![/yellow]")
                    break

                category = Prompt.ask("Choose a category", choices=self.categories)
                ques_ans = self.generate_question(category)
                
                if not ques_ans:  # Handle case where question generation fails
                    rprint("[red]Failed to generate question. Try again.[/red]")
                    continue

                self.console.print(f"\n[blue]Question:[/blue] {ques_ans['question']}")

                user_answer = Prompt.ask("\nEnter your answer").lower()

                if self.check_answer(user_answer, ques_ans['answer']):
                    rprint("[green]Correct![/green]")
                else:
                    rprint(f"[red]Incorrect![/red] The correct answer is: {ques_ans['answer']}")
                
                time.sleep(1)  # Brief pause between questions

            except KeyboardInterrupt:
                rprint("\n[yellow]Game ended by user. Thanks for playing![/yellow]")
                break
            except Exception as e:
                rprint(f"[red]An error occurred: {e}[/red]")
                continue

if __name__ == "__main__":
    game = QuizzieGame()
    game.play_game()
