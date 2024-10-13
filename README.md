
# **op-mica**
**Voting Influence and Concentration Analysis (VICA) for the Optimism Collective**

This repository is part of an Optimism Foundation Mission Request: **Measuring the Concentration of Power within the Collective**.

A [Dune Dashboard]() has been created to visualize the results from VICA. It will be maintained and updated regularly.

## **Project Overview**
The Voting Influence and Concentration Analysis (VICA) is a systematic approach to estimating the voting bloc's marginal influence on voting outcomes and measuring the degree of concentration in the voting system. This method, specifically tailored for the Optimism Collective, leverages logistic regression, counterfactual analysis, and data augmentation to deliver a robust and comprehensive understanding of each voting bloc's explicit and implicit influence on the voting process.

For more details, please read the project report.

---

## **Dependencies**

### **Python**
- Python 3.12
- All Python dependencies are listed in `requirements.txt` and can be installed using the command above.

### **R** (>= 4.4.1)
This project also relies on R for certain statistical and graph-based computations. Ensure R version 4.4.1 or above is installed.

To install required R packages:
```r
install.packages("dplyr")
install.packages("igraph")
install.packages("entropy")
install.packages("moments")
install.packages("ineq")
```

---

## **Data**
Create a folder `raw_data` and save the Token house data in a csv format.
Update RAW_DATA_DIR in `core/data_processor.py`.
Raw data for token house currently reply on csv files, will migrate to API once available.

## **Environment Variables**
Set the following environment variables in your `.env` file for API access:

```bash
DUNE_API_KEY=<your_dune_api_key>
OPSCAN_API_KEY=<your_ops_can_api_key>
```

---

## **Setup**
Follow these steps to set up the environment:

### 1. **Create and Activate Virtual Environment** (Python 3.12)
```bash
# Create the virtual environment with Python 3.12
which python3.12
python3.12 -m venv op_env

# Activate the virtual environment
# Windows
op_env\Scripts\activate
# macOS / Linux
source op_env/bin/activate

# Verify the Python version
python --version

# Install dependencies
pip install -r requirements.txt

# Deactivate the virtual environment when done
deactivate
```

### 2. **Run**
Use `core/run.ipynb` to run, explore, and expirement with the model.

---

## **Acknowledgements**

We extend our deep gratitude to the **Optimism Collective** for their sponsorship and support of this research. We would also like to thank **Emily** for her unwavering support and invaluable guidance throughout this project. Her insights were key in shaping both the direction and outcomes of this work.

We express our sincere thanks to **Varit** and the **curiaLab team** for their invaluable contributions, especially in providing critical data support whenever needed.
