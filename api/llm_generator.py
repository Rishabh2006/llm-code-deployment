import base64
import os
import google.generativeai as genai

class LLMGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    def generate_app(self, brief, checks, attachments, task_id):
        """
        Use Google Gemini to generate a complete web application
        Returns dict of files: {filename: content}
        """
        
        # Decode attachments
        decoded_attachments = []
        for att in attachments:
            name = att.get('name')
            url = att.get('url')
            
            if url.startswith('data:'):
                # Parse data URI
                parts = url.split(',', 1)
                if len(parts) == 2:
                    content = base64.b64decode(parts[1]).decode('utf-8', errors='ignore')
                    decoded_attachments.append({
                        'name': name,
                        'content': content
                    })
        
        # Build prompt
        prompt = self._build_prompt(brief, checks, decoded_attachments, task_id)
        
        # Call Gemini API
        print(f"🤖 Calling Google Gemini API...")
        response = self.model.generate_content(prompt)
        
        # Extract generated code
        generated_text = response.text
        
        # Parse the response to extract files
        files = self._parse_generated_files(generated_text, decoded_attachments)
        
        return files
    
    def _build_prompt(self, brief, checks, attachments, task_id):
        """Build the prompt for Gemini"""
        
        attachments_text = ""
        if attachments:
            attachments_text = "\n\nAttached files:\n"
            for att in attachments:
                attachments_text += f"\n--- {att['name']} ---\n{att['content']}\n"
        
        checks_text = "\n".join([f"- {check}" for check in checks])
        
        prompt = f"""You are an expert web developer. Generate a complete, production-ready single-page web application based on the following requirements.

**Task ID:** {task_id}

**Brief:**
{brief}

**Must pass these checks:**
{checks_text}
{attachments_text}

**Requirements:**
1. Create a complete HTML file with embedded CSS and JavaScript
2. Use CDN links for any libraries (Bootstrap, jQuery, etc.) - no npm installs
3. Make it visually professional with Bootstrap 5
4. Include all necessary functionality to pass the checks
5. Handle edge cases and errors gracefully
6. Add comments explaining key sections
7. If attachments are provided, embed or reference them appropriately

**IMPORTANT:**
- Do NOT use localStorage or sessionStorage (not supported in deployment environment)
- Use in-memory JavaScript variables for any state management
- All functionality must work in a single HTML file

Please provide:
1. index.html - The complete application
2. README.md - Professional documentation with:
   - Project summary
   - Setup instructions
   - Usage guide
   - Code explanation
   - MIT License section

Format your response as:

### index.html
```html
[your complete HTML code here]
```

### README.md
```markdown
[your complete README here]
```

Generate production-ready code that will pass all the checks listed above."""

        return prompt
    
    def _parse_generated_files(self, generated_text, attachments):
        """
        Parse Gemini's response to extract files
        """
        files = {}
        
        # Extract index.html
        if '```html' in generated_text:
            html_start = generated_text.find('```html') + 7
            html_end = generated_text.find('```', html_start)
            files['index.html'] = generated_text[html_start:html_end].strip()
        
        # Extract README.md
        if '```markdown' in generated_text:
            md_start = generated_text.find('```markdown') + 11
            md_end = generated_text.find('```', md_start)
            files['README.md'] = generated_text[md_start:md_end].strip()
        elif '```md' in generated_text:
            md_start = generated_text.find('```md') + 5
            md_end = generated_text.find('```', md_start)
            files['README.md'] = generated_text[md_start:md_end].strip()
        
        # Add MIT LICENSE
        files['LICENSE'] = self._get_mit_license()
        
        # Add attachments as separate files if needed
        for att in attachments:
            files[att['name']] = att['content']
        
        return files
    
    def _get_mit_license(self):
        """Return MIT license text"""
        return """MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""