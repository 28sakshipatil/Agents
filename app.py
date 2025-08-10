#this is hierarchical financial assistant app not A2A protocol
#the agents are not aware of each other, they are just classes
import time
import textwrap

# ANSI color codes for better terminal output
class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_agent_message(agent_name, message, color):
    """Prints a formatted message from an agent."""
    print(f"\n{color}{colors.BOLD}{agent_name}:{colors.ENDC}{color}")
    # Wrap text for better readability in terminal
    wrapped_message = textwrap.fill(message, width=80)
    print(wrapped_message + colors.ENDC)
    time.sleep(1.5)

def get_user_input(prompt):
    """Gets input from the user."""
    return input(f"{colors.YELLOW}> {prompt}{colors.ENDC}")

class Taxwell:
    """The Tax Specialist Agent"""

    def calculate_tax(self):
        """Guides the user through tax calculation."""
        print_agent_message("Taxwell", "I can help with that. To calculate your tax liability for FY 2024-25, I need some details.", colors.GREEN)
        
        # Get Annual Income
        while True:
            try:
                income_str = get_user_input("Please enter your total annual income (in INR): ")
                income = float(income_str)
                if income >= 0:
                    break
                else:
                    print_agent_message("Taxwell", "Income must be a positive number.", colors.RED)
            except ValueError:
                print_agent_message("Taxwell", "That doesn't look like a valid number. Please try again.", colors.RED)

        # Get Deductions
        while True:
            try:
                deductions_str = get_user_input("Enter your total deductions (e.g., 80C, 80D). Enter 0 if none: ")
                deductions = float(deductions_str)
                if deductions >= 0:
                    break
                else:
                    print_agent_message("Taxwell", "Deductions must be a positive number.", colors.RED)
            except ValueError:
                print_agent_message("Taxwell", "That doesn't look like a valid number. Please try again.", colors.RED)

        print_agent_message("Taxwell", f"Thanks. Calculating tax for an income of ₹{income:,.2f} and deductions of ₹{deductions:,.2f}...", colors.GREEN)
        
        # --- Tax Calculation Logic ---
        # Old Regime
        taxable_old = max(0, income - deductions)
        tax_old = 0
        if taxable_old > 1000000:
            tax_old = 112500 + (taxable_old - 1000000) * 0.30
        elif taxable_old > 500000:
            tax_old = 12500 + (taxable_old - 500000) * 0.20
        elif taxable_old > 250000:
            tax_old = (taxable_old - 250000) * 0.05
        
        old_regime_tax = round(tax_old * 1.04)
        if taxable_old <= 500000: old_regime_tax = 0  # Rebate u/s 87A

        # New Regime
        taxable_new = income
        tax_new = 0
        if taxable_new > 1500000:
            tax_new = 150000 + (taxable_new - 1500000) * 0.30
        elif taxable_new > 1200000:
            tax_new = 90000 + (taxable_new - 1200000) * 0.20
        elif taxable_new > 900000:
            tax_new = 45000 + (taxable_new - 900000) * 0.15
        elif taxable_new > 600000:
            tax_new = 15000 + (taxable_new - 600000) * 0.10
        elif taxable_new > 300000:
            tax_new = (taxable_new - 300000) * 0.05
            
        new_regime_tax = round(tax_new * 1.04)
        if taxable_new <= 700000: new_regime_tax = 0 # Rebate u/s 87A

        recommendation = "The New Regime seems more beneficial." if new_regime_tax < old_regime_tax else "The Old Regime seems more beneficial."

        result_text = f"""
Here's your tax summary:

{colors.BOLD}Old Regime:{colors.ENDC}
- Taxable Income: ₹{taxable_old:,.2f}
- Tax Liability:  ₹{old_regime_tax:,.2f}

{colors.BOLD}New Regime (Default):{colors.ENDC}
- Taxable Income: ₹{taxable_new:,.2f}
- Tax Liability:  ₹{new_regime_tax:,.2f}

{colors.BOLD}Recommendation:{colors.ENDC} {recommendation}
        """
        print_agent_message("Taxwell", result_text, colors.GREEN)


class Investa:
    """The Investment Advisor Agent"""

    def get_advice(self):
        """Guides the user through investment advice."""
        print_agent_message("Investa", "I can suggest some investment strategies. To personalize them, I need to know a bit about you.", colors.PURPLE)
        
        # Get Age
        while True:
            try:
                age_str = get_user_input("What is your age? ")
                age = int(age_str)
                if 18 <= age <= 100:
                    break
                else:
                    print_agent_message("Investa", "Please enter an age between 18 and 100.", colors.RED)
            except ValueError:
                print_agent_message("Investa", "Please enter a valid whole number for your age.", colors.RED)
        
        # Get Risk Tolerance
        while True:
            print_agent_message("Investa", "How would you describe your risk tolerance?", colors.PURPLE)
            risk_choice = get_user_input("Enter 'low', 'medium', or 'high': ").lower()
            if risk_choice in ['low', 'medium', 'high']:
                break
            else:
                print_agent_message("Investa", "Invalid choice. Please enter 'low', 'medium', or 'high'.", colors.RED)

        print_agent_message("Investa", f"Perfect. Generating suggestions for a {age}-year-old with {risk_choice} risk tolerance...", colors.PURPLE)
        
        advice = f"Here is a sample portfolio allocation I'd suggest:\n\n"
        if risk_choice == 'low':
            advice += """- 60% in Debt Instruments: Public Provident Fund (PPF), Fixed Deposits (FDs), Debt Mutual Funds.
- 20% in Hybrid Funds: Balanced advantage funds that mix equity and debt.
- 20% in Large-Cap Equity: NIFTY 50 Index Funds or large-cap mutual funds for steady growth."""
        elif risk_choice == 'medium':
            equity = min(80, 100 - age)
            debt = 100 - equity
            advice += f"""- {equity}% in Equity: A mix of Large-Cap Index Funds ({round(equity * 0.6)}%), Mid-Cap Funds ({round(equity * 0.3)}%), and a small allocation to Small-Cap Funds ({round(equity * 0.1)}%).
- {debt}% in Debt: A mix of PPF, and Corporate Bond Funds for stability."""
        else: # high risk
            advice += """- 70% in Equity: Focus on Mid-Cap and Small-Cap mutual funds for high growth potential.
- 20% in International Equity: An S&P 500 or NASDAQ 100 index fund for geographical diversification.
- 10% in Alternative Assets: Consider REITs or a small allocation to high-risk assets you understand."""

        advice += "\n\nDisclaimer: This is not financial advice. Please consult a registered financial advisor before making investment decisions."
        print_agent_message("Investa", advice, colors.PURPLE)


class Filer:
    """The ITR Filing Assistant Agent"""

    def give_guidance(self):
        """Provides guidance on ITR forms."""
        print_agent_message("Filer", "I can guide you through the ITR filing process.", colors.RED)
        
        while True:
            print_agent_message("Filer", "Which ITR form are you planning to file? If unsure, type 'unsure'.", colors.RED)
            choice = get_user_input("Options: 'ITR-1', 'ITR-2', 'unsure': ").lower()

            if choice == 'itr-1':
                guide_text = """Great, let's go through ITR-1 (Sahaj). Here are the key sections:

1.  Part A - General Information: Your PAN, Aadhaar, address, etc. (Mostly pre-filled).
2.  Part B - Gross Total Income: Enter salary (from Form 16), house property income, etc.
3.  Part C - Deductions: Fill in your deductions under Chapter VI-A (80C, 80D).
4.  Part D - Computation of Tax Payable: The system calculates your tax.
5.  Part E - Other Information: Details of all your bank accounts.
Remember to verify all pre-filled data before submitting!"""
                print_agent_message("Filer", guide_text, colors.RED)
                break
            elif choice == 'itr-2':
                guide_text = """ITR-2 is for individuals without business income but who may have capital gains.
In addition to ITR-1 sections, you'll have specific schedules for:
- Schedule CG: For Capital Gains from selling stocks, property, etc.
- Schedule FA: For reporting foreign assets and income.
It's crucial to have your broker statements and property sale documents handy."""
                print_agent_message("Filer", guide_text, colors.RED)
                break
            elif choice == 'unsure':
                info_text = """No problem. 
- ITR-1 (Sahaj) is for resident individuals with income up to ₹50 lakh from salary, one house property, and other sources.
- ITR-2 is for those who don't have business income but might have capital gains or foreign assets.
Which one sounds more like your situation?"""
                print_agent_message("Filer", info_text, colors.RED)
                # This loop will then repeat, allowing them to choose ITR-1 or ITR-2
            else:
                print_agent_message("Filer", "Invalid option. Please choose from the list.", colors.RED)


class Finley:
    """The Chief Financial Agent"""

    def __init__(self):
        self.tax_agent = Taxwell()
        self.investment_agent = Investa()
        self.itr_agent = Filer()

    def start(self):
        """Starts the main interaction loop."""
        print_agent_message("Finley", "Hello! I'm Finley, your chief financial agent. My team is here to help.", colors.BLUE)
        
        while True:
            print_agent_message("Finley", "What would you like to do today?", colors.BLUE)
            
            choice = get_user_input("""
1. Calculate my Tax
2. Get Investment Advice
3. Help with ITR Filing
4. Exit
Enter the number of your choice: """)

            if choice == '1':
                self.tax_agent.calculate_tax()
            elif choice == '2':
                self.investment_agent.get_advice()
            elif choice == '3':
                self.itr_agent.give_guidance()
            elif choice == '4':
                print_agent_message("Finley", "Goodbye! Feel free to reach out anytime.", colors.BLUE)
                break
            else:
                print_agent_message("Finley", "I'm sorry, that's not a valid choice. Please select from 1-4.", colors.BLUE)
            
            get_user_input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    chief_agent = Finley()
    chief_agent.start()
