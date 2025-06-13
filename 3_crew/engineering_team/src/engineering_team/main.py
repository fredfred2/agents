#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam
from dotenv import load_dotenv

# Load environment variables with rate limiting config
load_dotenv(override=True)

# Import our rate limiting configuration
try:
    from crewai_config import LITELLM_CONFIG, rate_limit
    print("✅ Rate limiting configuration loaded")
except ImportError:
    print("⚠️  Rate limiting configuration not found, using defaults")
    LITELLM_CONFIG = {}
try:
    import agentops
    agentops.init(os.getenv("AGENTOPS_API_KEY"))
    print("✅ AgentOps initialized successfully")
except Exception as e:
    print(f"⚠️  AgentOps initialization failed: {e}")
    print("Continuing without AgentOps monitoring...")
    agentops = None
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """

The system should allow users to create an account, log in, and manage their profile information.
the system should allow users to create an admin account and manage the system.
the system should allow to admin users to manage the products, categories, brands, and sizes and inventory.


Users must be able to register, sign in securely, and update their name, email, shipping address, and preferences.

The system should allow users to browse clothing items by category, size, color, brand, and price range.
Items should be filterable and searchable to improve discoverability based on user interest.

The system should allow users to view detailed information about each product, including images, sizes available, materials, care instructions, and price.
Each product page should clearly present all relevant data and available options.

The system should allow users to add items to a shopping cart and modify quantities before checkout.
Users must be able to review their cart, update item quantities, or remove products.

The system should allow users to proceed to checkout, enter payment details, and complete the purchase.
The checkout flow should include shipping method selection, address confirmation, and secure payment processing.

The system should allow users to view their order history and the status of current orders.
Orders should include tracking information, estimated delivery dates, and downloadable invoices.
Simulate every external API call or service call with a local repository.
"""
module_name = "ecommerce.py"
class_name = "Sales"


def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)


def replay(task_id: str = None):
    """
    Replay the crew execution from a specific task.
    """
    # Get task_id from command line arguments if not provided
    if task_id is None and len(sys.argv) > 1:
        task_id = sys.argv[1]
    
    if task_id is None:
        print("Error: task_id is required")
        sys.exit(1)
        
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    print(f"Replaying crew from task: {task_id}")
    # Create and replay the crew from the specified task
    result = EngineeringTeam().crew().replay(task_id=task_id, inputs=inputs)
    return result


if __name__ == "__main__":
    run()
