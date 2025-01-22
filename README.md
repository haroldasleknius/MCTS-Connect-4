# Link to Video Which Runs the Code: **https://www.youtube.com/watch?v=u8TdbUeVKt8**
# Final Year Project - Game Playing Connect 4 With **Monte Carlo Tree Search**
This project explores the intersection of artificial intelligence and game theory by implementing a smart agent to play the classic game of Connect 4. The agent leverages Monte Carlo Tree Search (MCTS), a cutting-edge algorithm widely used in AI for decision-making in strategic games, to evaluate potential moves and determine the most optimal path to victory.

## The project aims to:
* Demonstrate the capabilities of Monte Carlo simulations for strategic planning.
* Highlight the effectiveness of MCTS in solving complex decision trees under uncertainty.
* Provide a competitive Connect 4 AI capable of challenging human players at various skill levels.

## Key features of this project include:
* MCTS Implementation: Utilizing random sampling, rollout simulations, and backpropagation to analyze game states and select the best moves.
* Connect 4 Game Engine: A fully functional implementation of the Connect 4 rules, designed to interface seamlessly with the AI.
* Adaptive Decision Making: The agent adjusts its strategy based on the game's state, considering both offensive and defensive plays.
* User Interaction: Play against the AI or let two AIs compete to observe the decision-making process.

This project serves as a deep dive into the world of artificial intelligence, game design, and algorithmic efficiency, showcasing the potential of MCTS in modern AI applications.

# Installation and Setup
## Requirements needed to run
* Python 3.12+
* Pip
* VSCode or Similar
* GitBash or an other terminal

# Setting Up a Virtual Environment and Installing Requirements
Follow these steps to set up a Python virtual environment and install the required dependencies on **Windows**, **macOS**, or **Linux**.

---

## Setting Up a Virtual Environment

### **Windows**
1. Open a terminal or command prompt.
2. Navigate to project directory:
   ```bash
   cd MCTS-Connect-4
3. Create a Virtual Environment:
    ```bash
    python -m venv venv
4. Activate the Virtual Environment
    ```bash
    venv/Scripts/activate

### **macOS/Linux**
1. Open a terminal or command prompt.
2. Navigate to project directory:
    ```bash
    cd MCTS-Connect-4
3. Create a Virtual Environment
    ```bash
    python3 -m venv venv
4. Activate the Virtual Environment
    ```bash
    source venv/bin/activate

## Installing Required Dependencies
1. Ensuring the virtual environment is activated.
2. Ensure you are in the same directory as requirements.txt
3. Run the Command:
    ```bash
    pip install -r requirements.txt
4. The venv should be running with the libraries in requirements.txt installed
5. Once finished, to exist the Virtual Environment type:
    ```bash
    deactivate
## Running the Software
In the terminal/command line run:
1. Test the multi-armed-bandit problem
    ```bash
    python multi-armed-bandit.py
2. Test the Connect4 game that has implemented MCTS
    ```bash
    python state.py
3. Run the unit tests for Connect4
    ```bash
    python testconnect4.py
4. Run the unit tests for MCTS functions
    ```bash
    python montecarlo.py
