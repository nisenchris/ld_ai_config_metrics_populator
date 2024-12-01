# LaunchDarkly AI Config Simulator

A Python script that simulates user interactions with LaunchDarkly's AI configurations and generates synthetic tracking data.

## Overview

This tool simulates user interactions with different AI model configurations in LaunchDarkly, tracking:
- Generation events
- CSAT (Customer Satisfaction) feedback
- Token usage (input, output, and total)

## Features

- Supports multiple AI model variants:
  - Full Model (GPT-4)
  - Mini Model
  - French Language Model
  - Industrial Model
- Generates random but configurable:
  - CSAT scores
  - Token usage metrics
  - User contexts

## Prerequisites

- Python 3.x
- LaunchDarkly account with AI configuration set up
- LaunchDarkly SDK key

## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Copy the `.env.example` file to `.env` and update it with your LaunchDarkly SDK key and other configuration values:
    ```sh
    cp .env.example .env
    ```

5. Run the script:
    ```sh
    python main.py
    ```

## Usage

The script will simulate user interactions and track various metrics using the LaunchDarkly SDK. The main function `callLD` in `main.py` handles the primary loop to evaluate flags and send track events.

### Key Functions

- `csat_tracker(percent_chance)`: Determines if a CSAT event should be tracked based on a given percentage chance.
- `create_multi_context()`: Creates a multi-context combining user, device, and organization contexts.
- `callLD()`: Main function to evaluate flags and send track events to LaunchDarkly.

### Example Output

The script will print various tracking information to the console, such as:
- Flag variation
- Latency tracked
- Error rate tracked
- Version key
- Track data
- Successfully tracked activity for different models

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.