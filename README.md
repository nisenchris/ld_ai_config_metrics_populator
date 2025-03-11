# LaunchDarkly AI Config Simulator

A Python script that simulates user interactions with LaunchDarkly's AI configurations and generates synthetic tracking data.

## Overview

This tool simulates user interactions with different AI model configurations in LaunchDarkly, tracking:
- Generation events (successes and errors)
- CSAT (Customer Satisfaction) feedback
- Token usage (input, output, and total)
- Completion duration
- Time to first token

## Features

- Supports multiple AI model variants:
  - GPT-4o (Full Model)
  - GPT-4o Mini (Mini Model)
  - Claude 3.5 Sonnet
- Generates random but configurable:
  - CSAT scores
  - Error rates
  - Token usage metrics
  - Duration metrics
  - User contexts with multiple context kinds

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

5. Edit the `.env` file to update the following required variables:
    - `SDK_KEY`: Your LaunchDarkly SDK key (required)
    - `CONFIG_KEY`: The feature AI Config key to evaluate 

6. In LaunchDarkly, ensure your AI Config has variations with the following variation keys:
   - `gpt-4-o` - For the full GPT-4o model
   - `gpt-4-o-mini` - For the GPT-4o mini model
   - `claude-3-5-sonnet` - For the Claude 3.5 Sonnet model

7. Run the script:
    ```sh
    python main.py
    ```

## Usage

The script will simulate user interactions and track various metrics using the LaunchDarkly SDK. The main function `callLD` in `main.py` handles the primary loop to evaluate flags and send track events.

### Key Functions

- `csat_tracker(percent_chance)`: Determines if a CSAT event should be tracked based on a given percentage chance.
- `error_occurred(error_rate)`: Determines if an error should be simulated based on a given error rate.
- `create_multi_context()`: Creates a multi-context combining user, device, organization, and request contexts.
- `callLD()`: Main function to evaluate flags and send track events to LaunchDarkly.

### Context Types

The simulator uses a multi-context approach with four context kinds:

1. **User Context**: Includes attributes like name, plan, role, metro, and age.
2. **Device Context**: Includes attributes like OS, type, and version.
3. **Organization Context**: Includes attributes like name and region.
4. **Request Context**: Includes attributes like type, plan, priority, and source.

### Example Output

The script will print various tracking information to the console, such as:
- Flag variation key
- Tracking number and progress
- Track data (variation key and config key)
- Success/error tracking
- Token usage metrics
- Duration metrics
- Time to first token metrics

## Environment Variables

The `.env` file controls various aspects of the simulation:

- `SDK_KEY`: Your LaunchDarkly SDK key
- `CONFIG_KEY`: The feature flag key to evaluate (e.g., "chatbot-model-version")
- CSAT success rates for each model
- Error rates for each model
- Token ranges for input and output
- Duration ranges
- Time to first token ranges
- Number of iterations to run

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.