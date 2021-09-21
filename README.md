# SFMF
## Introduction
This repository models the single factor and multi factor credit risk portfolio distribution for commercial loans.
## Repository Structure
The repository is arranged in following directories:

* **code:** contains all the code for simulating both single and multi factor credit risk models.

    * **\_\_init.py\_\_:** the aim of this module is to create classes and functions that will be imported into other modules.
    * **single_factor_sensitivities.py:** the aim of this module is to calculate factor sensitvity, w_i. This is done using both the Maximum Likelihood Estimation (MLE) technique and calculating it from Probabilty of Default of individual assets.
    * **multi_factor_simulation.py:** This module generates the following -
       1. Portfolio loss based on the Multi Factor Model;
       2. Plot of the portfolio loss distribution;
       3. Value-at-Risk (VaR) for 90% and 99.9% confidence intervals;
       4. Expected Shortfall(ES) for 90% and 99.9% confidence intervals.
    * **multi_factor_simulation_ALITER.py:** This module generates the following (according to the [general multi-factor case](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiNkKrdkZHzAhXYDmMBHWFbB5IQFnoECAUQAQ&url=https%3A%2F%2Fwww.math.kth.se%2Fmatstat%2Fseminarier%2Freports%2FM-exjobb18%2F180601d.pdf&usg=AOvVaw3wwSt6S1zSZxo--_Ij_Yec)) -
       1. Portfolio loss based on the Multi Factor Model;
       2. Plot of the portfolio loss distribution;
       3. Value-at-Risk (VaR) for 90% and 99.9% confidence intervals;
       4. Expected Shortfall(ES) for 90% and 99.9% confidence intervals.
* **data:** contains the data for portfolio equity returns and covariance matrix.
* **export:** contains the output of both single and multi factor credit risk models.
## Outputs
Plots from the risk models:
### 
**Single factor portfolio loss distribution - 10,000 simulations**
![Single factor portfolio loss distribution - 10,000 simulations](https://raw.githubusercontent.com/arpanganguli/SFMF/main/export/single_factor_PLD_10000.png)
**Single factor portfolio loss distribution - 50,000 simulations**
![Single factor portfolio loss distribution - 50,000 simulations](https://raw.githubusercontent.com/arpanganguli/SFMF/main/export/single_factor_PLD_50000.png)
**Multi factor portfolio loss distribution - 10,000 simulations**
![Multi factor portfolio loss distribution - 10,000 simulations](https://raw.githubusercontent.com/arpanganguli/SFMF/main/export/multi_factor_PLD_10000.png)
**Multi factor portfolio loss distribution - 50,000 simulations**
![Multi factor portfolio loss distribution - 50,000 simulations](https://raw.githubusercontent.com/arpanganguli/SFMF/main/export/multi_factor_PLD_50000.png)