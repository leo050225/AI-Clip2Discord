import os
import requests

class DiscordNotifier:
    @staticmethod
    def send(text_content):
        # Discord message character limit (Max 2000 characters)
        if len(text_content) > 1950:
            text_content = text_content[:1950] + "...(truncated)"

        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        
        # Validate if Webhook URL exists
        if not webhook_url:
            print("Discord Webhook URL not found")
            return False
        
        payload = {
            "content": f"**Results**\n\n{text_content}"
        }
        
        # Send the payload to the Discord webhook
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            print("Successfully sent to Discord!")
            return True
        except Exception as e:
            print(f"Failed to send to Discord: {e}")
            return False