import time
import requests
from github import Github, GithubException

class GitHubManager:
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.github = Github(token)
        self.user = self.github.get_user()
    
    def create_repo(self, repo_name, files):
        """
        Create a new GitHub repository and push files
        Returns: (repo_url, commit_sha, pages_url)
        """
        try:
            # Check if repo already exists
            try:
                existing_repo = self.user.get_repo(repo_name)
                print(f"⚠️ Repository {repo_name} already exists. Deleting...")
                existing_repo.delete()
                time.sleep(2)  # Wait for deletion to complete
            except GithubException:
                pass  # Repo doesn't exist, which is what we want
            
            # Create new repository
            print(f"📦 Creating repository: {repo_name}")
            repo = self.user.create_repo(
                name=repo_name,
                description=f"Auto-generated app for task {repo_name}",
                private=False,
                auto_init=False
            )
            
            # Add files to repository
            print(f"📝 Adding files to repository...")
            for filename, content in files.items():
                repo.create_file(
                    path=filename,
                    message=f"Add {filename}",
                    content=content
                )
                print(f"   ✓ Added {filename}")
            
            # Enable GitHub Pages
            print(f"🌐 Enabling GitHub Pages...")
            self._enable_github_pages(repo)
            
            # Get commit SHA
            commits = repo.get_commits()
            commit_sha = commits[0].sha
            
            repo_url = repo.html_url
            pages_url = f"https://{self.username}.github.io/{repo_name}/"
            
            return repo_url, commit_sha, pages_url
            
        except Exception as e:
            print(f"❌ Error creating repo: {str(e)}")
            raise
    
    def update_repo(self, repo_name, files):
        """
        Update an existing GitHub repository
        Returns: (repo_url, commit_sha, pages_url)
        """
        try:
            # Get existing repository
            repo = self.user.get_repo(repo_name)
            print(f"🔄 Updating repository: {repo_name}")
            
            # Update files
            for filename, content in files.items():
                try:
                    # Try to get existing file
                    file = repo.get_contents(filename)
                    # Update existing file
                    repo.update_file(
                        path=filename,
                        message=f"Update {filename}",
                        content=content,
                        sha=file.sha
                    )
                    print(f"   ✓ Updated {filename}")
                except GithubException:
                    # File doesn't exist, create it
                    repo.create_file(
                        path=filename,
                        message=f"Add {filename}",
                        content=content
                    )
                    print(f"   ✓ Added {filename}")
            
            # Get latest commit SHA
            commits = repo.get_commits()
            commit_sha = commits[0].sha
            
            repo_url = repo.html_url
            pages_url = f"https://{self.username}.github.io/{repo_name}/"
            
            return repo_url, commit_sha, pages_url
            
        except Exception as e:
            print(f"❌ Error updating repo: {str(e)}")
            raise
    
    def _enable_github_pages(self, repo):
        """
        Enable GitHub Pages for a repository using REST API
        """
        try:
            url = f"https://api.github.com/repos/{self.username}/{repo.name}/pages"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "source": {
                    "branch": "main",
                    "path": "/"
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            # 201 = Created, 409 = Already exists
            if response.status_code in [201, 409]:
                print(f"   ✓ GitHub Pages enabled")
            else:
                print(f"   ⚠️ Pages response: {response.status_code}")
            
            time.sleep(5)  # Wait for Pages to initialize
            
        except Exception as e:
            print(f"   ⚠️ Error enabling Pages (may already be enabled): {str(e)}")
    
    def wait_for_pages_live(self, pages_url, timeout=300):
        """
        Wait for GitHub Pages to go live (return 200 OK)
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(pages_url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✓ GitHub Pages is live!")
                    return True
                else:
                    print(f"   ⏳ Pages status: {response.status_code}, waiting...")
            except requests.RequestException:
                print(f"   ⏳ Pages not ready yet, waiting...")
            
            time.sleep(10)  # Check every 10 seconds
        
        print(f"   ⚠️ Timeout waiting for Pages to go live")
        return False