from dotenv import load_dotenv  # pip install python-dotenv
import ldclient
from ldclient.config import Config
from ldclient.context import Context
from ldai.client import LDAIClient
from ldai.tracker import FeedbackKind, TokenUsage
import json
import os
import random
from utils.create_context import create_multi_context


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
FRENCH_CSAT = int(os.environ.get('FRENCH_CSAT'))
INDUSTRIAL_CSAT = int(os.environ.get('INDUSTRIAL_CSAT'))

# Token ranges
FULL_MODEL_INPUT_TOKENS = json.loads(os.environ.get('FULL_MODEL_INPUT_TOKENS'))
MINI_MODEL_INPUT_TOKENS = json.loads(os.environ.get('MINI_MODEL_INPUT_TOKENS'))
FRENCH_INPUT_TOKENS = json.loads(os.environ.get('FRENCH_INPUT_TOKENS'))
INDUSTRIAL_INPUT_TOKENS = json.loads(os.environ.get('INDUSTRIAL_INPUT_TOKENS'))

FULL_MODEL_OUTPUT_TOKENS = json.loads(
    os.environ.get('FULL_MODEL_OUTPUT_TOKENS'))
MINI_MODEL_OUTPUT_TOKENS = json.loads(
    os.environ.get('MINI_MODEL_OUTPUT_TOKENS'))
FRENCH_OUTPUT_TOKENS = json.loads(os.environ.get('FRENCH_OUTPUT_TOKENS'))
INDUSTRIAL_OUTPUT_TOKENS = json.loads(
    os.environ.get('INDUSTRIAL_OUTPUT_TOKENS'))

# Number of iterations
NUMBER_OF_ITERATIONS = int(os.environ.get('NUMBER_OF_ITERATIONS'))

# Initialize the LaunchDarkly SDK
ldclient.set_config(Config(SDK_KEY))
aiclient = LDAIClient(ldclient.get())

# Fallback value for the config
fallback_value = {
    "model": {
        "id": "gpt-4o",
        "parameters": {
            "maxTokens": 4096,
            "temperature": 0.7
        }
    },
    "messages": [
        {
            "content": "You are an expert in a software system, explaining concepts to users in a clear and concise manner.",
            "role": "system"
        },
        {
            "content": "I am a user of the system looking for help.",
            "role": "user"
        }
    ],
    "enabled": True
}


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

    # Primary loop to evaluate flags and send track events
    for i in range(NUMBER_OF_ITERATIONS):
        context = create_multi_context()
        config = aiclient.config(
            'ai-config--self-service-chatbot', context, fallback_value)

        version_key = config.tracker.version_key
        print(f"Version key: {version_key}")

        track_data = {
            'versionKey': version_key,
            'configKey': CONFIG_KEY
        }

        print(f"Track data: {track_data}")

        # Track generation count
        config.tracker.track_success()
        # ldclient.get().track('$ld:ai:generation', context, track_data, 1)
        print(f"Generation for {context} tracked using {track_data}")

        # Track CSAT and token usage
        # Full 4o model
        if version_key == "565272b1-bf06-4fbf-89f6-a5b819fc87d5":
            if csat_tracker(FULL_MODEL_CSAT):
                # config.tracker.track_feedback({"kind": FeedbackKind.Positive})
                ldclient.get().track('$ld:ai:feedback:user:positive', context, track_data, 1)
            else:
                # config.tracker.track_feedback({"kind": FeedbackKind.Negative})
                ldclient.get().track('$ld:ai:feedback:user:negative', context, track_data, 1)

            input_tokens = random.randint(
                FULL_MODEL_INPUT_TOKENS[0], FULL_MODEL_INPUT_TOKENS[1])
            output_tokens = random.randint(
                FULL_MODEL_OUTPUT_TOKENS[0], FULL_MODEL_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

            print(f"Successfully tracked activity for full model")

        # Mini 4o model
        elif version_key == "6977453a-71f1-48d9-ab35-4227d6d83df2":
            if csat_tracker(MINI_MODEL_CSAT):
                # config.tracker.track_feedback({"kind": FeedbackKind.Positive})
                ldclient.get().track('$ld:ai:feedback:user:positive', context, track_data, 1)
            else:
                # config.tracker.track_feedback({"kind": FeedbackKind.Negative})
                ldclient.get().track('$ld:ai:feedback:user:negative', context, track_data, 1)

            input_tokens = random.randint(
                MINI_MODEL_INPUT_TOKENS[0], MINI_MODEL_INPUT_TOKENS[1])
            output_tokens = random.randint(
                MINI_MODEL_OUTPUT_TOKENS[0], MINI_MODEL_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

            print(f"Successfully tracked activity for mini model")

        # French model
        elif version_key == "f7f71473-513c-4130-80a8-f26cc86d7b8f":
            if csat_tracker(FRENCH_CSAT):
                # config.tracker.track_feedback({"kind": FeedbackKind.Positive})
                ldclient.get().track('$ld:ai:feedback:user:positive', context, track_data, 1)
            else:
                # config.tracker.track_feedback({"kind": FeedbackKind.Negative})
                ldclient.get().track('$ld:ai:feedback:user:negative', context, track_data, 1)

            input_tokens = random.randint(
                FRENCH_INPUT_TOKENS[0], FRENCH_INPUT_TOKENS[1])
            output_tokens = random.randint(
                FRENCH_OUTPUT_TOKENS[0], FRENCH_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

            print(f"Successfully tracked activity for french model")

        # Industrial model
        elif version_key == "8edcb831-670f-4471-b85e-b86d4b502603":
            if csat_tracker(INDUSTRIAL_CSAT):
                # config.tracker.track_feedback({"kind": FeedbackKind.Positive})
                ldclient.get().track('$ld:ai:feedback:user:positive', context, track_data, 1)
            else:
                # config.tracker.track_feedback({"kind": FeedbackKind.Negative})
                ldclient.get().track('$ld:ai:feedback:user:negative', context, track_data, 1)

            input_tokens = random.randint(
                INDUSTRIAL_INPUT_TOKENS[0], INDUSTRIAL_INPUT_TOKENS[1])
            output_tokens = random.randint(
                INDUSTRIAL_OUTPUT_TOKENS[0], INDUSTRIAL_OUTPUT_TOKENS[1])
            total_tokens = input_tokens + output_tokens

            ldclient.get().track('$ld:ai:tokens:input', context, track_data, input_tokens)
            ldclient.get().track('$ld:ai:tokens:output', context, track_data, output_tokens)
            ldclient.get().track('$ld:ai:tokens:total', context, track_data, total_tokens)

            print(f"Successfully tracked activity for industrial model")
        else:
            print(f"No matching version key found for {version_key}")


'''
Execute!
'''
callLD()

'''
Responsibly close the LD Client
'''
ldclient.get().close()