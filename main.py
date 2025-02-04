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
load_dotenv()

# Basic config
SDK_KEY = os.environ.get('SDK_KEY')
CONFIG_KEY = os.environ.get('CONFIG_KEY')

# CSAT values
FULL_MODEL_CSAT = int(os.environ.get('FULL_MODEL_CSAT'))
MINI_MODEL_CSAT = int(os.environ.get('MINI_MODEL_CSAT'))
CLAUDE_CSAT = int(os.environ.get('CLAUDE_CSAT'))

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
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():

    # Primary loop to evaluate config and send track events
    for i in range(NUMBER_OF_ITERATIONS):

        context = create_multi_context()
        config, tracker = aiclient.config(CONFIG_KEY, context, fallback_value)
        variation_key = tracker._variation_key
        print(f"Variation key: {variation_key}")
        print(f"Tracking number: {i} / {NUMBER_OF_ITERATIONS}")

        # Track CSAT and token usage
        # Full 4o model - still differentiating variation by version key, not human friendly name
        if variation_key == "expert-gpt-4-o":
            
            # Using human friendly name for variationKey
            track_data = {
                'variationKey': "expert-gpt-4-o",
                'configKey': CONFIG_KEY
            }
            print(f"Track data: {track_data}")

            # Track generation count
            tracker.track_success()
            # ldclient.get().track('$ld:ai:generation', context, track_data, 1)

            if csat_tracker(FULL_MODEL_CSAT):
                tracker.track_feedback({"kind": FeedbackKind.Positive})
                # ldclient.get().track('$ld:ai:positive', context, track_data, 1)
            else:
                tracker.track_feedback({"kind": FeedbackKind.Negative})
                # ldclient.get().track('$ld:ai:negative', context, track_data, 1)

            input_tokens = random.randint(
                FULL_MODEL_INPUT_TOKENS[0], FULL_MODEL_INPUT_TOKENS[1])
            output_tokens = random.randint(
                FULL_MODEL_OUTPUT_TOKENS[0], FULL_MODEL_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            duration = random.randint(
                FULL_MODEL_DURATION[0], FULL_MODEL_DURATION[1])
            tracker.track_duration(duration)

            # NATIVE METHOD
            tokens = TokenUsage(
                total=total_tokens,
                input=input_tokens,
                output=output_tokens
            )
            tracker.track_tokens(tokens)

            # LDCLIENT METHOD
            # ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            # ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            # ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

            print(f"Successfully tracked activity for full model")

        # Mini 4o model
        elif variation_key == "expert-gpt-4-o-mini":
            track_data = {
                'variationKey': "expert-gpt-4-o-mini",
                'configKey': CONFIG_KEY
            }
            print(f"Track data: {track_data}")
            ldclient.get().track('$ld:ai:generation', context, track_data, 1)
            if csat_tracker(MINI_MODEL_CSAT):
                tracker.track_feedback({"kind": FeedbackKind.Positive})
                # ldclient.get().track('$ld:ai:positive', context, track_data, 1)
            else:
                tracker.track_feedback({"kind": FeedbackKind.Negative})
                # ldclient.get().track('$ld:ai:negative', context, track_data, 1)

            input_tokens = random.randint(
                MINI_MODEL_INPUT_TOKENS[0], MINI_MODEL_INPUT_TOKENS[1])
            output_tokens = random.randint(
                MINI_MODEL_OUTPUT_TOKENS[0], MINI_MODEL_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            duration = random.randint(
                MINI_MODEL_DURATION[0], MINI_MODEL_DURATION[1])
            tracker.track_duration(duration)

            tokens = TokenUsage(
                total=total_tokens,
                input=input_tokens,
                output=output_tokens
            )
            tracker.track_tokens(tokens)

            # ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            # ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            # ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

            print(f"Successfully tracked activity for mini model")

        # CLAUDE model
        elif variation_key == "bedrock-claude-3-5-sonnet":
            track_data = {
                'variationKey': "bedrock-claude-3-5-sonnet",
                'configKey': CONFIG_KEY
            }
            print(f"Track data: {track_data}")
            tracker.track_success()
            # ldclient.get().track('$ld:ai:generation', context, track_data, 1)
            if csat_tracker(CLAUDE_CSAT):
                tracker.track_feedback({"kind": FeedbackKind.Positive})
                # ldclient.get().track('$ld:ai:positive', context, track_data, 1)
            else:
                tracker.track_feedback({"kind": FeedbackKind.Negative})
                # ldclient.get().track('$ld:ai:negative', context, track_data, 1)

            input_tokens = random.randint(
                CLAUDE_INPUT_TOKENS[0], CLAUDE_INPUT_TOKENS[1])
            output_tokens = random.randint(
                CLAUDE_OUTPUT_TOKENS[0], CLAUDE_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            duration = random.randint(
                CLAUDE_DURATION[0], CLAUDE_DURATION[1])
            tracker.track_duration(duration)

            # NATIVE METHOD
            tokens = TokenUsage(
                total=total_tokens,
                input=input_tokens,
                output=output_tokens
            )
            tracker.track_tokens(tokens)

            # LDCLIENT METHOD   
            # ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            # ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            # ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

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