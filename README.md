# rational-choice-app
A Python GUI application demonstrating Pearce's Lemma: the duality between dominated strategies and justifiable beliefs in game theory.

## Companion Paper
For a detailed theoretical explanation of the concepts implemented in this tool, please refer to the companion paper:  
📄 **[Shadow Prices of Rationality (2026)](https://levokhanhtoan.com/wp-content/uploads/2026/01/shadowpricerationality2026.pdf)**

# Duality of Rational Choice

A Python GUI application demonstrating **Pearce's Lemma**: the duality between dominated strategies and rationalizable beliefs in game theory.

This tool allows users to input a payoff matrix, select a candidate action, and verify whether it is dominated (Primal problem) or justifiable by a specific belief (Dual problem).

## Features

- **Interactive Payoff Matrix**: Add/remove rows and columns dynamically.
- **Three Domination Concepts**:
  - **Strict**: Strictly dominated vs. Best response.
  - **Weak**: Weakly dominated vs. Cautious response (full support).
  - **Redundant**: Redundant vs. Unique best response.
- **Real-time Solver**: Uses Linear Programming (`scipy.optimize`) to solve primal and dual problems instantly.
- **Visual Analytics**: Matplotlib charts showing the dominating strategy or the rationalizing belief.

## Installation

### Prerequisites
- Python 3.8+

### Step-by-Step Installation (Mac/Linux)

Run the following commands in your terminal to set up the environment and run the app:

```bash
# 1. Download the code
git clone https://github.com/toanlecon/rational-choice-app.git

# 2. Go into the folder
cd rational-choice-app

# 3. Create a virtual environment (keeps your system clean)
python3 -m venv venv

# 4. Activate the environment
source venv/bin/activate

# 5. Install the required libraries (numpy, scipy, matplotlib)
pip install -r requirements.txt

# 6. Run the app
python3 -m rational_choice_app.main
