import time
import io
import base64
import hashlib
import os
from PIL import ImageGrab, Image
from dotenv import load_dotenv
from model_factory import ModelFactory
from discord_notifier import DiscordNotifier

# Load environment variables
load_dotenv()

def get_image_hash(image_bytes):
    """Calculate MD5 hash of an image to detect duplicates"""
    return hashlib.md5(image_bytes).hexdigest()

def main():
    print("Starting service...")
    print("Service initialized successfully!")
    
    # Initialize AI chain with fallback mechanism
    ai_chain = ModelFactory.get_vision_chain()
    prompt_text = os.getenv("AI_PROMPT", "Please describe this image.")
    
    last_image_hash = None

    try:
        while True:
            # Grab content from clipboard
            clipboard_content = ImageGrab.grabclipboard()
            
            # Check if the content is an image
            if isinstance(clipboard_content, Image.Image):
                # Convert image to byte stream
                buffered = io.BytesIO()
                # Convert RGBA to RGB for JPEG compatibility
                img_to_save = clipboard_content.convert('RGB')
                img_to_save.save(buffered, format="JPEG")
                img_bytes = buffered.getvalue()
                
                # Calculate MD5 to avoid redundant processing of the same image
                current_hash = get_image_hash(img_bytes)
                
                if current_hash != last_image_hash:
                    print("\nNew screenshot detected. Processing...")
                    last_image_hash = current_hash
                    
                    # Encode to Base64 for LangChain input
                    base64_image = base64.b64encode(img_bytes).decode("utf-8")
                    
                    try:
                        print("AI analyzing...")
                        result = ModelFactory.analyze_image(ai_chain, base64_image, prompt_text)
                        print(f"Analysis complete. Character count: {len(result)}")
                        
                        # Forward result to Discord
                        DiscordNotifier.send(result)
                        
                    except Exception as e:
                        print(f"AI processing error (All fallback models failed): {e}")
                        
            # Poll clipboard every 1 second to save CPU resources
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nService stopped manually.")

if __name__ == "__main__":
    main()