# scripts/update_stage.py
import asyncio
from src.utils import get_session_state, update_partial_state

async def update_stage_manually(session_id: str, new_stage: str):
    """Update stage manually for testing purposes"""
    
    # Get current state
    current_state = get_session_state(session_id)
    
    if not current_state:
        print(f"❌ No state found for session: {session_id}")
        return
    
    print(f"📊 Current stage: {current_state.get('stage', 'unknown')}")
    print(f"🔄 Updating to: {new_stage}")
    
    # Update only the stage
    update_data = {"stage": new_stage}
    update_partial_state(session_id, update_data)
    
    # Verify update
    updated_state = get_session_state(session_id)
    print(f"✅ Updated stage: {updated_state.get('stage', 'unknown')}")

async def main():
    # Update examples - modify these for your testing
        await update_stage_manually("24b8a7f79b8ae29a3d680e84099e1594", "setup_complete")


    
    # Example 1: Update first thread to need_company
    #await update_stage_manually("24b8a7f79b8ae29a3d680e84099e1594", "need_company")
    
    # Example 2: Update second thread to company_profile_completed
    #await update_stage_manually("6820568d02e6c38b2f1973f1ca78d553", "company_profile_completed")

if __name__ == "__main__":
    asyncio.run(main())