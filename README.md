# Formatting Module  
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [License](#license)

A simple Python module to assist with daily tasks completed by data analysts / scientists. 

The source code contains three Python files:
1. core
2. io
3. pipeline

The core file contains functions for manipulating data, the io file contains functions for importing data, and the 
pipeline file contains a function that combines all functions from core and io to create an Extract Transform Load 
(ETL) pipeline. 

## Installation

From GitHub

pip install git+https://github.com/CJTAYL/formatting_module.git

## Features

- Auto-detect and read CSV, Excel, JSON, Parquet, etc.
- Batch data‐type casting (`assign_dtypes`)
- Phone formatting (`format_phone_number`) 
- Currency formatting (`format_currency`)
- Full ETL pipeline orchestration (`run_pipeline`)

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.  

---

### Authors

- Your Name – (https://github.com/CJTAYL)