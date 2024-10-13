
# **op-mica**
**Voting Influence and Concentration Analysis (VICA) for the Optimism Collective**

This repository is part of an Optimism Foundation Mission Request: **Measuring the Concentration of Power within the Collective**.

## **Project Overview**
This project aims to analyze the governance structures of the Optimism Collective by measuring the concentration of voting power, applying the Voting Influence and Concentration Analysis (VICA) methodology.

---

## **Setup**
Follow these steps to set up the environment:

### 1. **Create and Activate Virtual Environment** (Python 3.12)
```bash
# Check the Python 3.12 path
which python3.12

# Create a virtual environment
python3.12 -m venv op_env

# Activate the virtual environment
# On Windows:
op_env\Scripts\activate

# On macOS / Linux:
source op_env/bin/activate
```

### 2. **Verify Python Version**
```bash
python --version
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Deactivate Virtual Environment** (when done)
```bash
deactivate
```

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

## **Environment Variables**
Set the following environment variables in your `.env` file for API access:

```bash
DUNE_API_KEY=<your_dune_api_key>
OPSCAN_API_KEY=<your_ops_can_api_key>
```

---

## **Acknowledgements**

We extend our deep gratitude to the **Optimism Collective** for their sponsorship and support of this research. Their backing was instrumental in enabling us to explore and analyze the governance mechanisms within the Collective.

We would also like to thank **Emily** for her unwavering support and invaluable guidance throughout this project. Her insights were key in shaping both the direction and outcomes of this work.

Additionally, we express our sincere thanks to **Varit** and the **curiaLab team** for their invaluable contributions, especially in providing critical data support whenever needed.
