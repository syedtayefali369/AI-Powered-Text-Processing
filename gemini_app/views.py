import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Configure Gemini API (you'll need to get an API key from Google AI Studio)
GEMINI_API_KEY = "AIzaSyBVb-JcV47iM-KrHtnGVFfPg7V1ts72-ic"  # Replace with your actual API key

class GeminiAIService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_text(self, prompt, function_type="general"):
        try:
            # Enhance prompt based on function type
            enhanced_prompt = self._enhance_prompt(prompt, function_type)
            
            response = self.model.generate_content(enhanced_prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _enhance_prompt(self, prompt, function_type):
        enhancements = {
            "summarize": f"Please provide a concise summary of the following text: {prompt}",
            "rewrite": f"Please rewrite the following text to improve clarity and flow: {prompt}",
            "translate": f"Please translate the following text to English: {prompt}",
            "proofread": f"Please proofread and correct any errors in the following text: {prompt}",
            "general": prompt
        }
        return enhancements.get(function_type, prompt)

# Initialize Gemini service
gemini_service = GeminiAIService()

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def process_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            function_type = data.get('function_type', 'general')
            
            if not prompt:
                return JsonResponse({'error': 'No prompt provided'}, status=400)
            
            # Process with Gemini AI
            result = gemini_service.generate_text(prompt, function_type)
            
            return JsonResponse({
                'result': result,
                'function_used': function_type
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)