import os
import json
import random
from datetime import datetime

class Chaos:
    def __init__(self):
        self.general_keywords = [
            "python programming", "automation tools", "data analysis",
            "machine learning", "freelance jobs", "side hustle", "SEO tips",
            "online marketing", "content creation", "digital nomad",
            "work from home", "remote jobs", "coding tutorials", "software development",
            "tech trends", "AI applications", "web scraping", "data science",
            "startup ideas", "e-commerce", "blogging tips", "financial freedom",
            "personal finance", "social media marketing", "email marketing",
            "productivity hacks", "online courses", "programming languages",
            "cloud computing", "mobile apps", "game development", "open source",
            "career advice", "job search", "digital marketing strategies",
            "content marketing", "affiliate marketing", "lead generation",
            "SEO strategies", "website optimization", "python libraries",
            "deep learning", "artificial intelligence", "big data",
            "coding bootcamp", "python projects", "technology news",
            "software engineering", "tech startups", "internet of things",
            "cybersecurity", "blockchain technology", "virtual reality",
            "augmented reality", "cloud storage", "tech gadgets",
            "javascript frameworks", "python automation", "machine learning projects",
            "data visualization", "freelance python developer", "online business",
            "website design", "digital transformation", "python scripting",
            "remote work tips", "digital entrepreneur", "python for beginners",
            "tech tutorials", "python automation scripts", "content strategy",
            "email automation", "digital agency", "SEO content",
            "lead magnets", "web development", "python coding challenges",
            "technology trends 2025", "AI tools", "python data analysis",
            "automation workflow", "python web scraping", "content calendar",
            "startup marketing", "productivity tools", "python freelancing",
            "online side hustles", "python programming jobs", "technical writing",
            "content creation tools", "marketing automation", "python tutorials"
        ]

        self.vermont_keywords = [
            "Vermont tourism", "Burlington events", "Vermont local business",
            "Vermont farms", "Green Mountain State", "Vermont hiking trails",
            "Montpelier news", "Vermont maple syrup", "Vermont breweries",
            "Vermont skiing", "Vermont farmers market", "Vermont real estate",
            "Vermont local restaurants", "Vermont artisans", "Vermont festivals",
            "Vermont outdoor activities", "Vermont history", "Vermont crafts",
            "Vermont community events", "Vermont concerts", "Vermont tech jobs",
            "Vermont small businesses", "Vermont wineries", "Vermont lake activities",
            "Vermont camping spots", "Vermont weather", "Vermont ski resorts",
            "Vermont state parks", "Vermont vacation rentals", "Vermont farmers",
            "Vermont education", "Vermont public schools", "Vermont economy",
            "Vermont agriculture", "Vermont government", "Vermont transportation",
            "Vermont volunteer opportunities", "Vermont local artists", "Vermont theatre",
            "Vermont local news", "Vermont restaurants", "Vermont craft beer",
            "Vermont tourism spots", "Vermont outdoor festivals", "Vermont charities",
            "Vermont fishing", "Vermont hiking", "Vermont historical sites",
            "Vermont food festivals", "Vermont culture", "Vermont winter sports",
            "Vermont music scene", "Vermont local shops", "Vermont nature trails",
            "Vermont art galleries", "Vermont farmers markets", "Vermont ski areas",
            "Vermont local events calendar", "Vermont travel guide", "Vermont craft fairs",
            "Vermont outdoor adventures", "Vermont lake houses", "Vermont mountain biking",
            "Vermont local restaurants guide", "Vermont wellness retreats", "Vermont skiing resorts",
            "Vermont camping", "Vermont small towns", "Vermont holiday events",
            "Vermont real estate market", "Vermont summer camps", "Vermont local history",
            "Vermont wine tasting", "Vermont cultural festivals", "Vermont farm tours",
            "Vermont fishing spots", "Vermont local theater", "Vermont hiking maps",
            "Vermont ski pass", "Vermont mountain resorts", "Vermont local cuisine",
            "Vermont cycling routes", "Vermont nature preserves", "Vermont family activities",
            "Vermont local farmers", "Vermont ski season", "Vermont outdoor sports",
            "Vermont travel tips", "Vermont historical landmarks", "Vermont hiking guide",
            "Vermont local breweries", "Vermont lake activities", "Vermont craft shops"
        ]

        self.barre_keywords = [
            "Barre Vermont events", "Barre local news", "Barre restaurants",
            "Barre farmers market", "Barre small businesses", "Barre music scene",
            "Barre outdoor activities", "Barre history", "Barre local artists",
            "Barre community events", "Barre craft fairs", "Barre local shops",
            "Barre winter festivals", "Barre summer events", "Barre ski areas",
            "Barre hiking trails", "Barre local theater", "Barre breweries",
            "Barre school events", "Barre holiday celebrations", "Barre charity events",
            "Barre real estate", "Barre family activities", "Barre lake activities",
            "Barre mountain biking", "Barre wellness retreats", "Barre local farmers",
            "Barre art galleries", "Barre outdoor sports", "Barre local cuisine",
            "Barre cycling routes", "Barre community centers", "Barre food festivals",
            "Barre fishing spots", "Barre ski season", "Barre historical landmarks",
            "Barre travel guide", "Barre camping spots", "Barre summer camps",
            "Barre cultural festivals", "Barre local theater groups", "Barre volunteer opportunities",
            "Barre lake houses", "Barre mountain resorts", "Barre local museums",
            "Barre winter sports", "Barre local bookshops", "Barre family events",
            "Barre outdoor concerts", "Barre ski resorts", "Barre local charities",
            "Barre farmers markets guide", "Barre hiking maps", "Barre ski pass",
            "Barre mountain biking trails", "Barre local wineries", "Barre outdoor festivals",
            "Barre travel tips", "Barre local schools", "Barre community gardens",
            "Barre local theater productions", "Barre local wellness centers", "Barre cycling events",
            "Barre fishing tournaments", "Barre local craft breweries", "Barre hiking guides",
            "Barre winter events", "Barre summer festivals", "Barre local art exhibitions",
            "Barre mountain hiking trails", "Barre outdoor markets", "Barre family-friendly activities",
            "Barre local cultural events", "Barre ski club", "Barre local farm tours",
            "Barre charity fundraisers", "Barre art shows", "Barre local volunteer groups",
            "Barre community theater", "Barre local outdoor adventures", "Barre hiking spots",
            "Barre winter hiking", "Barre local festivals", "Barre small town events",
            "Barre outdoor music festivals", "Barre local fitness classes", "Barre winter sports clubs",
            "Barre local holiday markets", "Barre family festivals", "Barre hiking trails guide",
            "Barre local music venues", "Barre outdoor recreation", "Barre craft shows"
        ]

        self.output_dir = "chaos_output"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_chunks(self, chunk_count=3):
        chunks = []
        for _ in range(chunk_count):
            kw_general = random.choice(self.general_keywords)
            kw_vermont = random.choice(self.vermont_keywords)
            kw_barre = random.choice(self.barre_keywords)
            chunk = f"{kw_general}, {kw_vermont}, {kw_barre}"
            chunks.append(chunk)
        return chunks

    def save_chunks(self):
        chunks = self.generate_chunks()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        for i, chunk in enumerate(chunks, 1):
            data = {
                "chunk": chunk,
                "metadata": {
                    "categories": ["local", "money"],  # Example defaults
                    "priority": "medium",
                    "content": "blog"
                }
            }
            filename = os.path.join(self.output_dir, f"chunk_{timestamp}_{i:03}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        print(f"Chaos: Generated and saved {len(chunks)} chunks to '{self.output_dir}'.")

if __name__ == "__main__":
    chaos = Chaos()
    chaos.save_chunks()

