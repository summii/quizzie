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

    def generate_question(self):
        """Generate a question for the given category using ollama"""
        category = random.choice(self.categories)
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
        

        
if __name__ == "__main__":
    game = QuizzieGame()
    game.generate_question()
