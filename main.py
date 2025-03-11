from dotenv import load_dotenv  # pip install python-dotenv
import ldclient
from ldclient.config import Config
from ldclient.context import Context
from ldai.client import LDAIClient, AIConfig, ModelConfig, LDMessage, ProviderConfig
from ldai.tracker import FeedbackKind, TokenUsage
import json
import os
import random
import time
from utils.create_context import create_multi_context, create_user_context


'''
Get environment variables
'''
# Load environment variables from .env file
load_dotenv(override=True)  # Force reload of environment variables

# Basic config
SDK_KEY = os.environ.get('SDK_KEY')
print(f"Using SDK_KEY: {SDK_KEY}")

# Read CONFIG_KEY directly from .env file
with open('.env', 'r') as env_file:
    for line in env_file:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            if key == 'CONFIG_KEY':
                CONFIG_KEY = value
                break
    else:
        # Fallback if not found in .env
        CONFIG_KEY = "ai-configs-exp-test"  

print(f"Using CONFIG_KEY: {CONFIG_KEY}")

# CSAT values
FULL_MODEL_CSAT = int(os.environ.get('FULL_MODEL_CSAT'))
MINI_MODEL_CSAT = int(os.environ.get('MINI_MODEL_CSAT'))
CLAUDE_CSAT = int(os.environ.get('CLAUDE_CSAT'))

# Error rates (percentages)
FULL_MODEL_ERROR_RATE = int(os.environ.get('FULL_MODEL_ERROR_RATE', 5))  # Default 5%
MINI_MODEL_ERROR_RATE = int(os.environ.get('MINI_MODEL_ERROR_RATE', 8))  # Default 8%
CLAUDE_ERROR_RATE = int(os.environ.get('CLAUDE_ERROR_RATE', 3))  # Default 3%

# Token ranges
FULL_MODEL_INPUT_TOKENS = json.loads(os.environ.get('FULL_MODEL_INPUT_TOKENS'))
MINI_MODEL_INPUT_TOKENS = json.loads(os.environ.get('MINI_MODEL_INPUT_TOKENS'))
CLAUDE_INPUT_TOKENS = json.loads(os.environ.get('CLAUDE_INPUT_TOKENS'))

FULL_MODEL_OUTPUT_TOKENS = json.loads(
    os.environ.get('FULL_MODEL_OUTPUT_TOKENS'))
MINI_MODEL_OUTPUT_TOKENS = json.loads(
    os.environ.get('MINI_MODEL_OUTPUT_TOKENS'))
CLAUDE_OUTPUT_TOKENS = json.loads(os.environ.get('CLAUDE_OUTPUT_TOKENS'))

# Duration ranges in milliseconds [min, max]
FULL_MODEL_DURATION = json.loads(os.environ.get('FULL_MODEL_DURATION'))
MINI_MODEL_DURATION = json.loads(os.environ.get('MINI_MODEL_DURATION'))
CLAUDE_DURATION = json.loads(os.environ.get('CLAUDE_DURATION'))

# Time to first token ranges in milliseconds [min, max]
FULL_MODEL_FIRST_TOKEN = json.loads(os.environ.get('FULL_MODEL_FIRST_TOKEN'))
MINI_MODEL_FIRST_TOKEN = json.loads(os.environ.get('MINI_MODEL_FIRST_TOKEN'))
CLAUDE_FIRST_TOKEN = json.loads(os.environ.get('CLAUDE_FIRST_TOKEN'))

# Number of iterations
NUMBER_OF_ITERATIONS = int(os.environ.get('NUMBER_OF_ITERATIONS'))

# Initialize the LaunchDarkly SDK
ldclient.set_config(Config(SDK_KEY))
aiclient = LDAIClient(ldclient.get())

# Fallback value for the config
fallback_value = AIConfig(
    enabled=True,
    model=ModelConfig(
        name="expert-gpt-4-o",
        parameters={"temperature": 0.8},
    ),
    messages=[LDMessage(role="system", content="")],
    provider=ProviderConfig(name="gpt-4o"),
)

'''
CSAT true or false calculator.
'''
def csat_tracker(percent_chance):
    calc_chance = random.randint(1, 100)
    if calc_chance <= percent_chance:
        return True
    else:
        return False

'''
Error rate calculator.
'''
def error_occurred(error_rate):
    calc_chance = random.randint(1, 100)
    if calc_chance <= error_rate:
        return True
    else:
        return False

'''
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():

    # Primary loop to evaluate config and send track events
    for i in range(NUMBER_OF_ITERATIONS):

        context = create_multi_context()
        print(f"Created multi-context with request: {context}")
        config, tracker = aiclient.config(CONFIG_KEY, context, fallback_value)
        variation_key = tracker._variation_key
        
        print(f"Variation key: {variation_key}")
        print(f"Tracking number: {i} / {NUMBER_OF_ITERATIONS}")

        # Track CSAT and token usage
        # Full 4o model - still differentiating variation by version key, not human friendly name
        if variation_key == "expert-gpt-4-o" or variation_key == "gpt-4-o":
            
            # Using human friendly name for variationKey
            track_data = {
                'variationKey': variation_key,
                'configKey': CONFIG_KEY
            }
            print(f"Track data: {track_data}")

            # Track generation success/error
            if error_occurred(FULL_MODEL_ERROR_RATE):
                tracker.track_error()
                print("Tracked error for full model")
            else:
                tracker.track_success()
                # Track CSAT only for successful generations
                if csat_tracker(FULL_MODEL_CSAT):
                    tracker.track_feedback({"kind": FeedbackKind.Positive})
                else:
                    tracker.track_feedback({"kind": FeedbackKind.Negative})

                input_tokens = random.randint(
                    FULL_MODEL_INPUT_TOKENS[0], FULL_MODEL_INPUT_TOKENS[1])
                output_tokens = random.randint(
                    FULL_MODEL_OUTPUT_TOKENS[0], FULL_MODEL_OUTPUT_TOKENS[1])
                total_tokens = input_tokens + output_tokens

                duration = random.randint(
                    FULL_MODEL_DURATION[0], FULL_MODEL_DURATION[1])
                tracker.track_duration(duration)

                # Track time to first token
                first_token_time = random.randint(
                    FULL_MODEL_FIRST_TOKEN[0], FULL_MODEL_FIRST_TOKEN[1])
                tracker.track_time_to_first_token(first_token_time)

                # NATIVE METHOD
                tokens = TokenUsage(
                    total=total_tokens,
                    input=input_tokens,
                    output=output_tokens
                )
                tracker.track_tokens(tokens)

                print(f"Successfully tracked activity for full model")

        # Mini 4o model
        elif variation_key == "expert-gpt-4-o-mini" or variation_key == "gpt-4-o-mini":
            track_data = {
                'variationKey': variation_key,
                'configKey': CONFIG_KEY
            }
            print(f"Track data: {track_data}")

            # Track generation success/error
            if error_occurred(MINI_MODEL_ERROR_RATE):
                tracker.track_error()
                print("Tracked error for mini model")
            else:
                tracker.track_success()
                # Track CSAT only for successful generations
                if csat_tracker(MINI_MODEL_CSAT):
                    tracker.track_feedback({"kind": FeedbackKind.Positive})
                else:
                    tracker.track_feedback({"kind": FeedbackKind.Negative})

                input_tokens = random.randint(
                    MINI_MODEL_INPUT_TOKENS[0], MINI_MODEL_INPUT_TOKENS[1])
                output_tokens = random.randint(
                    MINI_MODEL_OUTPUT_TOKENS[0], MINI_MODEL_OUTPUT_TOKENS[1])
                total_tokens = input_tokens + output_tokens

                duration = random.randint(
                    MINI_MODEL_DURATION[0], MINI_MODEL_DURATION[1])
                tracker.track_duration(duration)

                # Track time to first token
                first_token_time = random.randint(
                    MINI_MODEL_FIRST_TOKEN[0], MINI_MODEL_FIRST_TOKEN[1])
                tracker.track_time_to_first_token(first_token_time)

                tokens = TokenUsage(
                    total=total_tokens,
                    input=input_tokens,
                    output=output_tokens
                )
                tracker.track_tokens(tokens)

                print(f"Successfully tracked activity for mini model")

        # CLAUDE model
        elif variation_key == "bedrock-claude-3-5-sonnet" or variation_key == "claude-3-5-sonnet":
            track_data = {
                'variationKey': variation_key,
                'configKey': CONFIG_KEY
            }
            print(f"Track data: {track_data}")

            # Track generation success/error
            if error_occurred(CLAUDE_ERROR_RATE):
                tracker.track_error()
                print("Tracked error for CLAUDE model")
            else:
                tracker.track_success()
                # Track CSAT only for successful generations
                if csat_tracker(CLAUDE_CSAT):
                    tracker.track_feedback({"kind": FeedbackKind.Positive})
                else:
                    tracker.track_feedback({"kind": FeedbackKind.Negative})

                input_tokens = random.randint(
                    CLAUDE_INPUT_TOKENS[0], CLAUDE_INPUT_TOKENS[1])
                output_tokens = random.randint(
                    CLAUDE_OUTPUT_TOKENS[0], CLAUDE_OUTPUT_TOKENS[1])
                total_tokens = input_tokens + output_tokens

                duration = random.randint(
                    CLAUDE_DURATION[0], CLAUDE_DURATION[1])
                tracker.track_duration(duration)

                # Track time to first token
                first_token_time = random.randint(
                    CLAUDE_FIRST_TOKEN[0], CLAUDE_FIRST_TOKEN[1])
                tracker.track_time_to_first_token(first_token_time)

                # NATIVE METHOD
                tokens = TokenUsage(
                    total=total_tokens,
                    input=input_tokens,
                    output=output_tokens
                )
                tracker.track_tokens(tokens)

                print(f"Successfully tracked activity for CLAUDE model")

        else:
            print(f"No matching version key found for {variation_key}")

        time.sleep(.05)


'''
Execute!
'''
callLD()

'''
Responsibly close the LD Client
'''
ldclient.get().close()