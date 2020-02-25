# Robo-Advisor Project

Utilizes AlphaVantage Stock Market API (https://www.alphavantage.co/) to pull updated trading recommendations.

## Prerequisites

    + Anaconda 3.7
    + Python 3.7
    + Pip

## Installation

Clone or download this repository: https://github.com/Gplafferty0219/robo-advisor onto your computer. The navigate there using the following commands:

```sh
cd Desktop
```

```sh
cd robo-advisor
```

Use Anaconda to create and activate a new virtual environment called something like "stocks-env". You can use the following commands

```sh
conda create -n stocks-env python=3.7#
conda activate stocks-env
```

From within this environment download the following packages:

```sh
pip install requests
pip install python-dotenv
pip install -r requirements.txt
```

## Setup

Before you begin, obtain an AlphaVantage API Key (https://www.alphavantage.co/support/#api-key)

Now, create a file in the repository called .env and enter your API key like so:

    ALPHAVANTAGE_API_KEY="abc123"

## Usage

Run the script!

```sh
python app/robo.py
```
