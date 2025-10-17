import os
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from .llm_generator import LLMGenerator
from .github_manager import GitHubManager
from .evaluator_notifier import EvaluatorNotifier

load_dotenv()

app = Flask(__name__)
CORS(app)

# Your configuration
MY_EMAIL = os.getenv('MY_EMAIL')
MY_SECRET = os.getenv('MY_SECRET')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize managers
llm_generator = LLMGenerator(GEMINI_API_KEY)
github_manager = GitHubManager(GITHUB_TOKEN, GITHUB_USERNAME)
evaluator_notifier = EvaluatorNotifier()

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "LLM Code Deployment API is running"
    })

@app.route('/build-app', methods=['POST'])
def build_app():
    """
    Main endpoint that receives task requests and builds apps
    """
    try:
        data = request.json
        
        # STEP 1: Verify secret
        if data.get('secret') != MY_SECRET:
            return jsonify({"error": "Invalid secret"}), 403
        
        # STEP 2: Verify email
        if data.get('email') != MY_EMAIL:
            return jsonify({"error": "Wrong email"}), 403
        
        # STEP 3: Return 200 immediately
        # Process asynchronously to avoid timeout
        response = jsonify({"status": "received", "message": "Processing your request"})
        
        # Extract task information
        task_id = data.get('task')
        round_num = data.get('round')
        nonce = data.get('nonce')
        brief = data.get('brief')
        checks = data.get('checks', [])
        attachments = data.get('attachments', [])
        evaluation_url = data.get('evaluation_url')
        
        print(f"\n{'='*60}")
        print(f"📥 Received request for Task: {task_id}, Round: {round_num}")
        print(f"{'='*60}\n")
        
        # Process in background (or you can use Celery/background tasks)
        process_task(
            task_id=task_id,
            round_num=round_num,
            nonce=nonce,
            brief=brief,
            checks=checks,
            attachments=attachments,
            evaluation_url=evaluation_url
        )
        
        return response, 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def process_task(task_id, round_num, nonce, brief, checks, attachments, evaluation_url):
    """
    Process the task: generate code, create/update repo, deploy, notify
    """
    try:
        repo_name = task_id
        
        # STEP 4: Generate code using LLM
        print(f"🤖 Generating code with LLM...")
        generated_files = llm_generator.generate_app(
            brief=brief,
            checks=checks,
            attachments=attachments,
            task_id=task_id
        )
        
        # STEP 5: Create or update GitHub repo
        if round_num == 1:
            print(f"📦 Creating new GitHub repository: {repo_name}")
            repo_url, commit_sha, pages_url = github_manager.create_repo(
                repo_name=repo_name,
                files=generated_files
            )
        else:
            print(f"🔄 Updating existing repository: {repo_name}")
            repo_url, commit_sha, pages_url = github_manager.update_repo(
                repo_name=repo_name,
                files=generated_files
            )
        
        print(f"✅ Repository deployed!")
        print(f"   Repo: {repo_url}")
        print(f"   Pages: {pages_url}")
        print(f"   Commit: {commit_sha}")
        
        # STEP 6: Wait for GitHub Pages to be live
        print(f"⏳ Waiting for GitHub Pages to go live...")
        github_manager.wait_for_pages_live(pages_url, timeout=300)
        
        # STEP 7: Notify evaluator
        print(f"📤 Notifying evaluator...")
        success = evaluator_notifier.notify(
            evaluation_url=evaluation_url,
            email=MY_EMAIL,
            task_id=task_id,
            round_num=round_num,
            nonce=nonce,
            repo_url=repo_url,
            commit_sha=commit_sha,
            pages_url=pages_url
        )
        
        if success:
            print(f"✅ Successfully notified evaluator!")
        else:
            print(f"⚠️ Failed to notify evaluator, but repo is deployed")
        
        print(f"\n{'='*60}")
        print(f"✨ Task {task_id} Round {round_num} completed!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error processing task: {str(e)}")
        raise

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)