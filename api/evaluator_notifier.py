import time
import requests

class EvaluatorNotifier:
    def notify(self, evaluation_url, email, task_id, round_num, nonce, 
               repo_url, commit_sha, pages_url, max_retries=5):
        """
        Notify the evaluator with repository details
        Implements exponential backoff: 1, 2, 4, 8, ... seconds
        """
        
        payload = {
            "email": email,
            "task": task_id,
            "round": round_num,
            "nonce": nonce,
            "repo_url": repo_url,
            "commit_sha": commit_sha,
            "pages_url": pages_url
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        for attempt in range(max_retries):
            try:
                print(f"📤 Attempt {attempt + 1}/{max_retries}: Notifying evaluator...")
                
                response = requests.post(
                    evaluation_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"   ✅ Evaluator notified successfully!")
                    print(f"   Response: {response.text}")
                    return True
                else:
                    print(f"   ⚠️ Evaluator returned status {response.status_code}")
                    print(f"   Response: {response.text}")
                    
                    # If not successful, retry with exponential backoff
                    if attempt < max_retries - 1:
                        delay = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
                        print(f"   ⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                
            except requests.RequestException as e:
                print(f"   ❌ Request failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    delay = 2 ** attempt
                    print(f"   ⏳ Retrying in {delay} seconds...")
                    time.sleep(delay)
        
        print(f"   ❌ Failed to notify evaluator after {max_retries} attempts")
        return False