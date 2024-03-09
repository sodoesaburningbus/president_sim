This simulator applies state-by-state election odds to determine
the overall probabilities of presidential election outcomes.

Probabilities are such that they measure the chance of a Republican win
There are no third-parties considered.

The default scenario comes from 270towin.com
accessed March 8th, 2024 and uses the following assignments

Probabilities are:
Democrat Safe      - 0.05
Democrat Likely    - 0.20
Democrat Leans     - 0.35
Toss-up            - 0.50
Republican Leans   - 0.65
Republican Likely  - 0.80
Republican Safe    - 0.95

New scenarios can be created simply by modifying the probability in the input file.
The input file is structured as:
state,probability of Republican victory,electoral votes

To run the code, simply modify the options in the top of the run_sim script and use the command:
python run_sim.py

Package requirements are:
cartopy
matplotlib
numpy