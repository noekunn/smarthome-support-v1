from server import SmartHomeSupportEnv
from models import SmartHomeAction, ActionType

def test_password_reset():
    print("Testing Password Reset Task...")
    env = SmartHomeSupportEnv(task_id="password-reset")
    obs = env.reset()
    
    action = SmartHomeAction(
        action_type=ActionType.REPLY, 
        ticket_id="T-100", 
        content="Here is the link: https://smarthome.com/reset-password"
    )
    obs, reward, done, info = env.step(action)
    print(f"Step 1: Reward: {reward}, Done: {done}")
    
    action = SmartHomeAction(action_type=ActionType.CLOSE_TICKET, ticket_id="T-100")
    obs, reward, done, info = env.step(action)
    print(f"Step 2: Reward: {reward}, Done: {done}")
    assert reward == 1.0
    print("Password Reset Test Passed!")

def test_camera_offline():
    print("\nTesting Camera Offline Task...")
    env = SmartHomeSupportEnv(task_id="camera-offline")
    env.reset()
    
    # Step 1: Check status
    action = SmartHomeAction(action_type=ActionType.CHECK_DEVICE_STATUS, ticket_id="T-200")
    obs, reward, done, info = env.step(action)
    print(f"Step 1: Reward: {reward}, Status: {obs.last_action_result}")
    
    # Step 2: Reply
    action = SmartHomeAction(
        action_type=ActionType.REPLY, 
        ticket_id="T-200", 
        content="The camera is offline, we are restarting it."
    )
    obs, reward, done, info = env.step(action)
    print(f"Step 2: Reward: {reward}")
    
    # Step 3: Close
    action = SmartHomeAction(action_type=ActionType.CLOSE_TICKET, ticket_id="T-200")
    obs, reward, done, info = env.step(action)
    print(f"Step 3: Reward: {reward}, Done: {done}")
    assert reward == 1.0
    print("Camera Offline Test Passed!")

if __name__ == "__main__":
    test_password_reset()
    test_camera_offline()
