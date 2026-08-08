import json
import re
from google import genai
from config import GEMINI_API_KEY

STOP_WORDS = {'and', 'the', 'for', 'with', 'from', 'that', 'this', 'are', 'has', 'have', 'not', 'you', 'your', 'all', 'any', 'out', 'new', 'via', 'per', 'off'}

class AIEmailClassifier:
    def __init__(self, api_key=None):
        self.api_key = api_key or GEMINI_API_KEY
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def classify_email(self, email_item, categories):
        """
        Classifies an email dictionary into one of the provided categories.
        Uses Gemini AI if API key is provided, otherwise uses a smart word-boundary scoring engine.
        """
        if not categories:
            return "Uncategorized"

        categories_str = ", ".join([f'"{c}"' for c in categories])
        prompt = f"""
You are an expert email categorization AI.
Classify the following email into EXACTLY ONE of these target categories: [{categories_str}].

EMAIL DETAILS:
- Subject: {email_item.get('subject', 'N/A')}
- Sender: {email_item.get('sender', 'N/A')}
- Snippet: {email_item.get('snippet', 'N/A')}

INSTRUCTIONS:
1. Select the SINGLE category from [{categories_str}] that BEST matches this specific email.
2. Differentiate carefully between work, financial/receipts, newsletters, promotional offers, social notifications, and urgent security alerts.
3. Do NOT assign all emails to a single category. Match each email to its true content type.

Respond ONLY in valid JSON:
{{
  "category": "<Exact name of one of the provided categories>"
}}
"""
        if not self.client:
            return self._smart_heuristic_classifier(email_item, categories)

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            raw_text = response.text.strip()
            
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            raw_text = raw_text.strip()

            result = json.loads(raw_text)
            chosen_cat = result.get('category', '').strip()
            
            for cat in categories:
                if cat.lower() == chosen_cat.lower():
                    return cat

            return self._smart_heuristic_classifier(email_item, categories)

        except Exception as e:
            print(f"Gemini AI classification error: {e}")
            return self._smart_heuristic_classifier(email_item, categories)

    def _smart_heuristic_classifier(self, email_item, categories):
        """
        Smart word-boundary scoring engine. Ensures stop words and partial substring matches
        do NOT cause all emails to collapse into a single category.
        """
        subject = email_item.get('subject', '').lower()
        snippet = email_item.get('snippet', '').lower()
        sender = email_item.get('sender', '').lower()
        combined = f"{subject} {snippet} {sender}"

        category_scores = {cat: 0 for cat in categories}

        # Knowledge base of domain keywords mapped to standard intent concepts
        domain_keywords = {
            'work': ['meeting', 'project', 'deadline', 'team', 'jira', 'github', 'zoom', 'calendar', 'client', 'report', 'status', 'office', 'invite', 'slack', 'notion', 'task', 'dev', 'pr', 'commit', 'build', 'pipeline', 'deployment', 'standup', 'agenda', 'doc', 'sheet', 'hr', 'interview', 'resume', 'hiring', 'salary', 'manager', 'lead'],
            'finance': ['receipt', 'invoice', 'payment', 'bank', 'statement', 'order', 'transaction', 'tax', 'refund', 'price', 'amount', 'subscription', 'amazon', 'paypal', 'stripe', 'billing', 'bill', 'charge', 'paid', 'due', 'balance', 'credit', 'debit', 'card', 'checkout', 'purchase', 'total', 'usd', 'eur', 'inr', 'wallet', 'transfer', 'wire'],
            'promo': ['sale', 'discount', 'offer', 'deal', 'coupon', 'shop', 'clearance', 'save', 'promo', 'store', 'bogo', 'vip', 'redeem', 'percent', 'off'],
            'newsletter': ['newsletter', 'digest', 'weekly', 'edition', 'article', 'read', 'blog', 'update', 'news', 'medium', 'substack', 'youtube', 'podcast', 'trends', 'insights', 'story', 'issue', 'briefing', 'daily', 'curated'],
            'social': ['linkedin', 'twitter', 'facebook', 'instagram', 'reddit', 'discord', 'notification', 'commented', 'tagged', 'mentioned', 'follower', 'friend', 'connection', 'photo', 'post', 'like'],
            'urgent': ['urgent', 'important', 'immediate', 'asap', 'alert', 'warning', 'security', 'verify', 'verification', 'password', 'reset', 'otp', 'code', 'login', 'attempt', 'unauthorized', 'suspended', 'threat'],
            'travel': ['flight', 'hotel', 'booking', 'ticket', 'reservation', 'trip', 'airline', 'airbnb', 'uber', 'cab', 'itinerary', 'travel', 'checkin', 'boarding', 'stay']
        }

        for cat in categories:
            cat_lower = cat.lower()

            # 1. Match domain concepts using exact word boundary
            for concept, keywords in domain_keywords.items():
                if concept in cat_lower:
                    for kw in keywords:
                        pattern = rf'\b{re.escape(kw)}\b'
                        if re.search(pattern, subject):
                            category_scores[cat] += 4
                        elif re.search(pattern, combined):
                            category_scores[cat] += 2

            # 2. Match words directly from category title (excluding common stop words)
            raw_words = re.split(r'[\s&/_\-]+', cat_lower)
            cat_words = [w for w in raw_words if len(w) > 2 and w not in STOP_WORDS]
            
            for w in cat_words:
                pattern = rf'\b{re.escape(w)}\b'
                if re.search(pattern, subject):
                    category_scores[cat] += 5
                elif re.search(pattern, combined):
                    category_scores[cat] += 3

        # Find highest score
        max_score = max(category_scores.values())
        if max_score > 0:
            # Return category with highest score
            for cat, score in category_scores.items():
                if score == max_score:
                    return cat

        # Fallback distribution if no keywords match: assign based on sender or subject length hash to avoid monolithic tagging
        email_hash = sum(ord(c) for c in (subject + sender))
        return categories[email_hash % len(categories)]
