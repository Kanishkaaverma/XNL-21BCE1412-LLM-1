import logging
from opentelemetry import trace
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def track_error(error):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("track_error"):
        logger.error(f"Error Occurred: {error}")

def main(error_message):
    try:
        # Simulate an error for demonstration purposes
        raise ValueError(error_message)
    except Exception as e:
        track_error(e)

if __name__ == "__main__":
    error_message = input("Enter the error message to track: ")
    main(error_message)