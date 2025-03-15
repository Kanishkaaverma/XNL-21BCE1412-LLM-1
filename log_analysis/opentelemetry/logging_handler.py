import logging
import argparse
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_transaction(transaction):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("log_transaction"):
        logger.info(f"Transaction Logged: {transaction}")

def main(amount, description):
    transaction = {"amount": amount, "description": description}
    log_transaction(transaction)

if __name__ == "__main__":
    amount = float(input("Enter the transaction amount: "))
    description = input("Enter the transaction description: ")
    transaction = {"amount": amount, "description": description}
    log_transaction(transaction)