from google import genai
from google.genai import types
from ..config import get_settings
from ..schemas import RecommendationResponse

class GeminiService:
    def __init__(self):
        s=get_settings()
        self.settings=s
        self.client=genai.Client(api_key=s.gemini_api_key) if s.gemini_api_key and s.use_gemini else None
    @property
    def enabled(self): return self.client is not None
    def generate(self,prompt,image_bytes=None,image_mime=None):
        if not self.client: raise RuntimeError("Gemini disabled")
        contents=[prompt]
        if image_bytes and image_mime:
            contents.insert(0,types.Part.from_bytes(data=image_bytes,mime_type=image_mime))
        response=self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecommendationResponse,
                temperature=0.2,
                system_instruction="Return only schema-valid JSON. Use only supplied catalog items. Never claim live prices or inventory."
            )
        )
        if getattr(response,"parsed",None) is not None: return response.parsed
        return RecommendationResponse.model_validate_json(response.text)
