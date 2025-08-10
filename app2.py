import time
import textwrap
import os
import google.generativeai as genai

# ANSI color codes for better terminal output
class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_agent_message(agent_name, message, color, typing_delay=1.5):
    """Prints a formatted message from an agent."""
    print(f"\n{color}{colors.BOLD}{agent_name}:{colors.ENDC}{color}")
    wrapped_message = textwrap.fill(message, width=80)
    print(wrapped_message + colors.ENDC)
    time.sleep(typing_delay)

def get_user_input(prompt):
    """Gets input from the user."""
    return input(f"{colors.YELLOW}> {prompt}{colors.ENDC}")

def call_generative_ai(prompt):
    """Makes a real API call to the Gemini model."""
    print(f"\n{colors.BLUE}[Thinking... Contacting Generative AI...]{colors.ENDC}")
    
    # --- BEST PRACTICE: Get API Key from Environment Variable ---
    # It's safer to store your key outside the code.
    # Set it in your terminal before running: export GOOGLE_API_KEY="YOUR_API_KEY"
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # A fallback for simplicity if the environment variable isn't set.
        # WARNING: Do not commit your API key directly into the code in a real project.
        api_key = "" 
    
    if api_key == "YOUR_API_KEY_HERE":
        print(f"{colors.RED}ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual Gemini API key.{colors.ENDC}")
        return "I cannot connect to the AI service without a valid API key."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') # Or another suitable model
        response = model.generate_content(prompt)
        
        # Add a small delay to make the interaction feel natural
        time.sleep(1.5) 
        
        return response.text

    except Exception as e:
        print(f"{colors.RED}An error occurred with the AI service: {e}{colors.ENDC}")
        return "I'm sorry, I'm having trouble connecting to my knowledge base right now."


class FinancialContext:
    """A shared whiteboard for agents to read from and write to."""
    def __init__(self):
        self.income = None
        self.deductions = None
        self.age = None
        self.risk_tolerance = None
        self.tax_bracket = "Unknown"
        self.recommended_regime = "Unknown"

class Agent:
    """Base class for all specialist agents."""
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def process(self, context: FinancialContext):
        """The main method for an agent to perform its task."""
        raise NotImplementedError("Each agent must implement its own process method.")

class Taxwell(Agent):
    """The Tax Specialist Agent. Reads income/deductions, writes tax info to context."""
    def __init__(self):
        super().__init__("Taxwell", colors.GREEN)

    def process(self, context: FinancialContext):
        print_agent_message(self.name, "I need to assess your tax situation to build your financial profile.", self.color)
        
        if context.income is None:
            while True:
                try:
                    income_str = get_user_input("Please enter your total annual income (in INR): ")
                    context.income = float(income_str)
                    if context.income >= 0: break
                    else: print_agent_message(self.name, "Income must be a positive number.", colors.RED)
                except ValueError:
                    print_agent_message(self.name, "That doesn't look like a valid number.", colors.RED)
        
        if context.deductions is None:
            while True:
                try:
                    deductions_str = get_user_input("Enter your total deductions (e.g., 80C, 80D). Enter 0 if none: ")
                    context.deductions = float(deductions_str)
                    if context.deductions >= 0: break
                    else: print_agent_message(self.name, "Deductions must be a positive number.", colors.RED)
                except ValueError:
                    print_agent_message(self.name, "That doesn't look like a valid number.", colors.RED)

        # --- Perform Calculations ---
        taxable_old = max(0, context.income - context.deductions)
        tax_old = 0
        if taxable_old > 1000000: tax_old = 112500 + (taxable_old - 1000000) * 0.30
        elif taxable_old > 500000: tax_old = 12500 + (taxable_old - 500000) * 0.20
        elif taxable_old > 250000: tax_old = (taxable_old - 250000) * 0.05
        old_regime_tax = round(tax_old * 1.04)
        if taxable_old <= 500000: old_regime_tax = 0

        taxable_new = context.income
        tax_new = 0
        if taxable_new > 1500000: tax_new = 150000 + (taxable_new - 1500000) * 0.30
        elif taxable_new > 1200000: tax_new = 90000 + (taxable_new - 1200000) * 0.20
        elif taxable_new > 900000: tax_new = 45000 + (taxable_new - 900000) * 0.15
        elif taxable_new > 600000: tax_new = 15000 + (taxable_new - 600000) * 0.10
        elif taxable_new > 300000: tax_new = (taxable_new - 300000) * 0.05
        new_regime_tax = round(tax_new * 1.04)
        if taxable_new <= 700000: new_regime_tax = 0

        # --- Write findings back to the context ---
        context.recommended_regime = "New Regime" if new_regime_tax < old_regime_tax else "Old Regime"
        if context.recommended_regime == "Old Regime":
            if taxable_old > 1000000: context.tax_bracket = "30%"
            elif taxable_old > 500000: context.tax_bracket = "20%"
            else: context.tax_bracket = "5% or less"
        else:
            if taxable_new > 1500000: context.tax_bracket = "30%"
            elif taxable_new > 1200000: context.tax_bracket = "20%"
            else: context.tax_bracket = "15% or less"
            
        print_agent_message(self.name, f"I've analyzed your taxes. Your recommended regime is the {context.recommended_regime} and your marginal tax bracket is ~{context.tax_bracket}. I've updated the context.", self.color)
        
        # This prompt is now more specific for better AI results
        prompt = f"My annual income is {context.income:,.0f} INR with deductions of {context.deductions:,.0f} INR. My recommended tax regime is the {context.recommended_regime}. Briefly summarize why this regime is better for me."
        ai_summary = call_generative_ai(prompt)
        print_agent_message(self.name, ai_summary, self.color)


class Investa(Agent):
    """The Investment Advisor Agent. Reads context, provides tailored advice."""
    def __init__(self):
        super().__init__("Investa", colors.PURPLE)

    def process(self, context: FinancialContext):
        print_agent_message(self.name, "To give you tailored investment advice, I need to know your age and risk appetite.", self.color)
        
        if context.age is None:
            while True:
                try:
                    age_str = get_user_input("What is your age? ")
                    context.age = int(age_str)
                    if 18 <= context.age <= 100: break
                    else: print_agent_message(self.name, "Please enter an age between 18 and 100.", colors.RED)
                except ValueError:
                    print_agent_message(self.name, "Please enter a valid whole number for your age.", colors.RED)
        
        if context.risk_tolerance is None:
            while True:
                risk_choice = get_user_input("Enter your risk tolerance ('low', 'medium', or 'high'): ").lower()
                if risk_choice in ['low', 'medium', 'high']:
                    context.risk_tolerance = risk_choice
                    break
                else: print_agent_message(self.name, "Invalid choice.", colors.RED)

        # --- Read from context and call AI for holistic advice ---
        print_agent_message(self.name, f"Excellent. I see from the context that your tax bracket is {context.tax_bracket}. I will now generate a holistic plan.", self.color)
        
        prompt = f"Act as an expert financial advisor in India. Give me a holistic investment plan for a {context.age}-year-old with a '{context.risk_tolerance}' risk tolerance, who is in the {context.tax_bracket} tax bracket. Focus on actionable advice, specific investment types (like PPF, ELSS, Index Funds), and explain the rationale, especially how the tax bracket influences the choices."
        detailed_advice = call_generative_ai(prompt)
        print_agent_message(self.name, detailed_advice, self.color)

class Finley:
    """The Chief Orchestrator Agent"""
    def __init__(self):
        self.tax_agent = Taxwell()
        self.investment_agent = Investa()

    def get_holistic_plan(self):
        """Orchestrates a multi-agent workflow for a full financial plan."""
        context = FinancialContext()
        print_agent_message("Finley", "Understood. To create a holistic financial plan, I will orchestrate a collaboration between my specialist agents.", colors.BLUE)
        
        # Step 1: Call Taxwell to populate the context
        self.tax_agent.process(context)
        
        print_agent_message("Finley", "Great. Now that we have your tax profile, I will bring in Investa to provide a tailored investment strategy.", colors.BLUE)

        # Step 2: Call Investa, which can now read Taxwell's findings
        self.investment_agent.process(context)

        print_agent_message("Finley", "Your personalized financial plan is complete.", colors.BLUE)

    def start(self):
        print_agent_message("Finley", "Hello! I'm Finley, your chief financial agent. My team now collaborates to provide holistic advice.", colors.BLUE)
        while True:
            print_agent_message("Finley", "What would you like to do today?", colors.BLUE, typing_delay=0.5)
            choice = get_user_input("1. Create a Holistic Financial Plan\n2. Exit\nEnter your choice: ")
            if choice == '1':
                self.get_holistic_plan()
            elif choice == '2':
                print_agent_message("Finley", "Goodbye! Feel free to reach out anytime.", colors.BLUE)
                break
            else:
                print_agent_message("Finley", "I'm sorry, that's not a valid choice.", colors.BLUE)
            get_user_input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    chief_agent = Finley()
    chief_agent.start()
