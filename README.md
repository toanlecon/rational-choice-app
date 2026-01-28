# rational-choice-app
A Python GUI application demonstrating Pearce's Lemma: the duality between dominated strategies and rationalizable beliefs in game theory.

# Duality of Rational Choice

A Python GUI application demonstrating **Pearce's Lemma**: the duality between dominated strategies and rationalizable beliefs in game theory.

This tool allows users to input a payoff matrix, select a candidate action, and verify whether it is dominated (Primal problem) or justifiable by a specific belief (Dual problem).

## Features

- **Interactive Payoff Matrix**: Add/remove rows and columns dynamically.
- **Three Domination Concepts**:
  - **Strict**: Strictly dominated vs. Best response.
  - **Weak**: Weakly dominated vs. Cautious response (full support).
  - **Redundant**: Very weakly dominated vs. Unique best response.
- **Real-time Solver**: Uses Linear Programming (`scipy.optimize`) to solve primal and dual problems instantly.
- **Visual Analytics**: Matplotlib charts showing the dominating strategy or the rationalizing belief.

## Installation

### Prerequisites
- Python 3.8+

### Install from Source
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/rational-choice-app.git](https://github.com/YOUR_USERNAME/rational-choice-app.git)
   cd rational-choice-app
