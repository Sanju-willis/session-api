# src\scripts\run_onboarding.py
import asyncio
from graphs.home_graph import HomeGraph  # Adjust import based on your project structure

async def main():
    graph = HomeGraph()

    input_data = {
        "session_id": "123",                # optional
        "stage": "company_profile_completed",               # try "company_profile_completed", "onboarded"
        "user_id": "u1",
        "company_id": "c1",
        "message_type": "initial",          # not used but passed
        "messages": [],
    }

    result = await graph.invoke(input_data)
    print("Agent Reply:", result.get("message"))

if __name__ == "__main__":
    asyncio.run(main())

# PYTHONPATH=./ python scripts/run_onboarding.py
