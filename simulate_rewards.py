import os
import json
import random
from typing import List
from server.smarthome_support_v1_environment import SmartHomeSupportEnv
from models import SmartHomeAction, ActionType

def simulate_episodes(num_episodes: int = 100):
    print(f"Starting simulation of {num_episodes} episodes...")
    
    task_ids = ["password-reset", "camera-offline", "security-triage"]
    stats = {tid: {"scores": [], "steps": []} for tid in task_ids}
    
    for i in range(num_episodes):
        task_id = random.choice(task_ids)
        env = SmartHomeSupportEnv(task_id=task_id)
        obs = env.reset()
        
        total_reward = 0.0
        step = 0
        done = False
        
        while not done and step < 10:
            step += 1
            
            # Simple simulation logic
            if task_id == "password-reset":
                if step == 1:
                    action = SmartHomeAction(action_type=ActionType.REPLY, ticket_id="T-100", content="https://smarthome.com/reset-password")
                else:
                    action = SmartHomeAction(action_type=ActionType.CLOSE_TICKET, ticket_id="T-100")
            
            elif task_id == "camera-offline":
                if step == 1:
                    action = SmartHomeAction(action_type=ActionType.CHECK_DEVICE_STATUS, ticket_id="T-200")
                elif step == 2:
                    action = SmartHomeAction(action_type=ActionType.REPLY, ticket_id="T-200", content="Restarting camera.")
                else:
                    action = SmartHomeAction(action_type=ActionType.CLOSE_TICKET, ticket_id="T-200")
            
            else: # security-triage
                if step == 1:
                    action = SmartHomeAction(action_type=ActionType.PRIORITIZE_TICKET, ticket_id="T-301", priority=1)
                elif step == 2:
                    action = SmartHomeAction(action_type=ActionType.REPLY, ticket_id="T-301", content="Handling security.")
                else:
                    action = SmartHomeAction(action_type=ActionType.CLOSE_TICKET, ticket_id="T-301")
            
            obs, reward, done, info = env.step(action)
            total_reward += reward
        
        # Apply the same capping logic as in inference.py
        final_score = max(0.0, min(total_reward, 1.0))
        stats[task_id]["scores"].append(final_score)
        stats[task_id]["steps"].append(step)

    print("\n--- Simulation Results ---")
    for tid, data in stats.items():
        avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
        max_score = max(data["scores"]) if data["scores"] else 0
        min_score = min(data["scores"]) if data["scores"] else 0
        print(f"Task: {tid}")
        print(f"  Episodes: {len(data['scores'])}")
        print(f"  Avg Score: {avg_score:.2f}")
        print(f"  Max Score: {max_score:.2f}")
        print(f"  Min Score: {min_score:.2f}")
        print("-" * 20)

if __name__ == "__main__":
    simulate_episodes(100)
