from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openai
import os
from dotenv import load_dotenv
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Handle both PostgreSQL and SQLite URLs
database_url = os.getenv('DATABASE_URL', 'sqlite:///stories.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')
DEMO_MODE = not openai_api_key

if DEMO_MODE:
    print("🔶 DEMO MODE: Running without OpenAI API key")
    print("   - Sample stories will be generated instead of AI stories")
    print("   - To enable full AI functionality, set OPENAI_API_KEY environment variable")
    print("   - Get an API key from: https://platform.openai.com/api-keys")
else:
    print("✅ OpenAI API key found - Full AI functionality enabled")
    openai.api_key = openai_api_key

# Database Models
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    age_group = db.Column(db.String(20), nullable=False)
    child_name = db.Column(db.String(50), nullable=True)
    story_length = db.Column(db.String(20), default='medium')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Story {self.title}>'

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    popularity_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Theme {self.name}>'

# Story Generation Service
class StoryGenerator:
    def __init__(self):
        self.length_configs = {
            'short': {'words': 200, 'description': '2-3 minutes'},
            'medium': {'words': 400, 'description': '5-7 minutes'},
            'long': {'words': 600, 'description': '8-10 minutes'}
        }
    
    def generate_story(self, theme, age_group, child_name=None, story_length='medium'):
        """Generate a bedtime story using OpenAI API or demo mode"""
        
        # Check if we're in demo mode
        if DEMO_MODE:
            return self._generate_demo_story(theme, age_group, child_name, story_length)
        
        try:
            # Build the prompt
            word_count = self.length_configs[story_length]['words']
            
            prompt = f"""Create a gentle, calming bedtime story for a {age_group}-year-old child.
            
Theme: {theme}
Length: Approximately {word_count} words
Child's name: {child_name if child_name else '[Child]'}

Requirements:
- Age-appropriate for {age_group} years old
- Positive, calming tone suitable for bedtime
- Include moral lessons about kindness, courage, or friendship
- No scary or violent content
- Clear beginning, middle, and end
- Use simple language appropriate for the age group
- If a child's name is provided, make them the main character
- End with a peaceful, sleepy conclusion

Please write the story now:"""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a skilled children's author who specializes in creating gentle, educational bedtime stories. Always create content that is completely appropriate for children and promotes positive values."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            story_content = response.choices[0].message.content.strip()
            
            # Generate a title
            title_prompt = f"Create a short, appealing title (maximum 6 words) for this bedtime story about {theme}:"
            
            title_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You create short, child-friendly story titles."},
                    {"role": "user", "content": title_prompt}
                ],
                max_tokens=20,
                temperature=0.5
            )
            
            title = title_response.choices[0].message.content.strip().strip('"')
            
            return {
                'title': title,
                'content': story_content,
                'success': True
            }
            
        except Exception as e:
            error_message = str(e)
            if "api_key" in error_message.lower():
                return {
                    'title': 'API Configuration Error',
                    'content': 'There seems to be an issue with the OpenAI API key configuration. Please check that your API key is valid and has sufficient credits.',
                    'success': False
                }
            elif "quota" in error_message.lower() or "billing" in error_message.lower():
                return {
                    'title': 'API Quota Exceeded',
                    'content': 'The OpenAI API quota has been exceeded. Please check your billing settings and try again later.',
                    'success': False
                }
            else:
                return {
                    'title': 'Story Generation Error',
                    'content': f'Sorry, there was an error generating your story. Please try again in a moment. If the problem persists, the app will work in demo mode.',
                    'success': False
                }
    
    def _generate_demo_story(self, theme, age_group, child_name=None, story_length='medium'):
        """Generate a demo story when OpenAI API is not available"""
        child_name = child_name or "Alex"
        
        demo_stories = {
            'brave princess': {
                'title': f'{child_name} and the Crystal Castle',
                'content': f"""Once upon a time, in a land filled with shimmering rainbows and gentle clouds, there lived a brave little person named {child_name}. {child_name} had always dreamed of visiting the magical Crystal Castle that sparkled on top of the highest hill.

One sunny morning, {child_name} decided it was time for an adventure. With a small backpack filled with snacks and a heart full of courage, {child_name} began the journey up the winding path.

Along the way, {child_name} met a lost baby rabbit who was crying softly. "Don't worry, little friend," said {child_name} kindly. "I'll help you find your family." Together, they searched until they found the rabbit's cozy burrow.

The grateful rabbit's mother gave {child_name} a special crystal that glowed with warm, golden light. "This will guide you safely," she said with a smile.

When {child_name} finally reached the Crystal Castle, the doors opened wide to reveal a beautiful garden filled with flowers that sang gentle lullabies. The castle's wise guardian appeared and said, "Your kindness to the little rabbit has shown your true bravery. Welcome to our peaceful kingdom."

{child_name} spent the day playing with friendly crystal butterflies and listening to the flowers' soothing songs. As the sun began to set, painting the sky in soft pastels, {child_name} knew it was time to go home.

The journey back was quick and easy, guided by the magical crystal's warm glow. {child_name} arrived home just as the first stars appeared, feeling proud of the day's adventure and the new friendship made along the way.

That night, {child_name} fell asleep peacefully, dreaming of crystal butterflies and gentle lullabies, knowing that tomorrow would bring new adventures and chances to help others."""
            },
            'space adventure': {
                'title': f'{child_name} and the Sleepy Stars',
                'content': f"""High above the clouds, where the stars twinkle like diamonds, lived a young space explorer named {child_name}. {child_name} had a special rocket ship painted in soft blues and silvers that could fly among the stars.

One peaceful evening, {child_name} noticed that some stars seemed dimmer than usual. "I wonder if they're feeling sleepy," thought {child_name}. With a gentle whoosh, the rocket ship lifted off into the velvet night sky.

As {child_name} flew closer to the stars, they discovered that the stars were indeed very tired. "We've been shining all day and all night," yawned a particularly drowsy star. "We need someone to sing us a lullaby."

{child_name} had the perfect idea. From the rocket ship's special music box, {child_name} played the most beautiful, gentle melody that floated through space like silver ribbons. One by one, the tired stars began to smile and shine more brightly.

The moon, who had been watching with delight, gave {child_name} a gift – a small bottle of moonbeam dust that sparkled like glitter. "Sprinkle this wherever you go," said the moon kindly, "and it will bring peaceful dreams."

{child_name} flew home slowly, sprinkling the magical moonbeam dust over all the houses below. Children everywhere began to have the most wonderful, peaceful dreams filled with gentle starlight and soft lullabies.

Back on Earth, {child_name} parked the rocket ship safely in the backyard and climbed into bed. The friendly stars winked goodnight through the window, and {child_name} drifted off to sleep, surrounded by the gentle glow of moonbeam dust and the quiet songs of happy stars."""
            },
            'friendly dragon': {
                'title': f'{child_name} and the Rainbow Dragon',
                'content': f"""In a valley surrounded by rolling green hills, there lived a gentle dragon named Rainbow who had scales that shimmered with every color imaginable. Unlike the scary dragons in old stories, Rainbow was kind and loved making friends with children.

One day, a curious child named {child_name} was exploring the hills when they heard a soft, musical humming. Following the sound, {child_name} discovered Rainbow sitting by a peaceful pond, carefully tending to a garden of the most beautiful flowers anyone had ever seen.

"Hello there," said Rainbow with a warm smile. "I'm Rainbow, and I take care of this magical garden. Each flower here represents a different dream that children have at night."

{child_name} was amazed to see flowers that glowed like stars, petals that sparkled like jewels, and blooms that seemed to dance in the gentle breeze. "They're beautiful!" {child_name} exclaimed.

Rainbow explained that every night, the dragon would collect the sweetest dreams from the flowers and blow them gently into the wind, so they could find their way to sleeping children all around the world.

"Would you like to help me tonight?" asked Rainbow. {child_name} nodded eagerly, and together they carefully gathered the dream-essence from each flower. Rainbow showed {child_name} how to whisper kind wishes into the magical mist.

As the evening stars appeared, Rainbow gently breathed the collected dreams into the night sky, where they transformed into twinkling lights that danced toward distant homes. {child_name} watched in wonder as the dreams floated away like gentle fireflies.

"Thank you for helping me," said Rainbow. "Because of your kindness, children everywhere will have especially sweet dreams tonight." Rainbow gave {child_name} a small, glowing flower to take home as a reminder of their magical friendship.

That night, {child_name} placed the special flower by the window and fell asleep with the biggest smile, knowing that somewhere in the hills, Rainbow was making sure everyone had wonderful dreams."""
            },
            'magical forest': {
                'title': f'{child_name} and the Whispering Trees',
                'content': f"""Deep in an enchanted forest where sunbeams danced through emerald leaves, there stood trees that could whisper the most wonderful secrets. A curious child named {child_name} discovered this magical place while following a pathway of golden leaves.

As {child_name} walked deeper into the forest, the trees began to whisper gentle greetings. "Welcome, young friend," rustled the wise old oak. "We've been waiting for someone with a kind heart like yours."

The trees explained that they were the guardians of all the forest creatures, and they needed {child_name}'s help. The woodland animals were preparing for their annual Festival of Friendship, but they had lost their way to the celebration clearing.

{child_name} eagerly agreed to help. Following the whispered directions from the trees, {child_name} found a family of lost hedgehogs, guided a confused owl back to his tree, and helped a shy deer find her courage to join the celebration.

As the sun began to set, {child_name} arrived at a beautiful clearing where animals of all kinds had gathered. There were rabbits with flower crowns, squirrels sharing acorns, and butterflies creating colorful patterns in the air.

The animals cheered when they saw {child_name} and invited their new friend to join the celebration. They danced under the starlight, shared stories, and the trees provided the most beautiful music by rustling their leaves in harmony.

As a thank-you gift, the animals presented {child_name} with a special acorn that would always glow softly, serving as a reminder that kindness and helping others creates the most magical adventures.

When it was time to go home, the trees whispered directions for the safest path, and fireflies lit the way. {child_name} arrived home feeling grateful for the new friends and the magical day in the whispering forest.

That night, {child_name} held the glowing acorn close and fell asleep to the gentle memory of the trees' whispered songs, dreaming of more adventures with forest friends."""
            }
        }
        
        # Use a matching story or default
        story_key = None
        for key in demo_stories.keys():
            if key.lower() in theme.lower() or theme.lower() in key.lower():
                story_key = key
                break
        
        if not story_key:
            # Use first story as default but customize it
            story_key = 'magical forest'
            story = demo_stories[story_key]
            # Customize title for the specific theme
            story['title'] = f"{child_name} and the {theme.title()} Adventure"
        else:
            story = demo_stories[story_key]
        
        return {
            'title': story['title'],
            'content': story['content'],
            'success': True,
            'demo': True
        }

# Initialize story generator
story_generator = StoryGenerator()

# PDF Generation Service
def generate_pdf(story):
    """Generate PDF for a story"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch, bottomMargin=1*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    content_style = ParagraphStyle(
        'CustomContent',
        parent=styles['Normal'],
        fontSize=12,
        lineHeight=14,
        spaceAfter=12
    )
    
    story_elements = []
    
    # Add title
    title = Paragraph(story.title, title_style)
    story_elements.append(title)
    story_elements.append(Spacer(1, 20))
    
    # Add story content with proper paragraph breaks
    paragraphs = story.content.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            p = Paragraph(paragraph.strip(), content_style)
            story_elements.append(p)
            story_elements.append(Spacer(1, 12))
    
    # Add metadata
    story_elements.append(Spacer(1, 30))
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        textColor='gray'
    )
    
    metadata = f"Generated on: {story.created_date.strftime('%B %d, %Y')}<br/>Theme: {story.theme}<br/>Age Group: {story.age_group}"
    if story.child_name:
        metadata += f"<br/>Created for: {story.child_name}"
    
    story_elements.append(Paragraph(metadata, metadata_style))
    
    doc.build(story_elements)
    buffer.seek(0)
    return buffer

# Routes
@app.route('/')
def index():
    """Home page with story generation form"""
    recent_stories = Story.query.order_by(Story.created_date.desc()).limit(5).all()
    popular_themes = Theme.query.order_by(Theme.popularity_score.desc()).limit(10).all()
    return render_template('index.html', 
                         recent_stories=recent_stories, 
                         popular_themes=popular_themes,
                         demo_mode=DEMO_MODE)

# Make demo_mode available to all templates
@app.context_processor
def inject_demo_mode():
    return {'demo_mode': DEMO_MODE}

@app.route('/api/status')
def api_status():
    """API endpoint to check demo mode status"""
    return jsonify({
        'demo_mode': DEMO_MODE,
        'openai_configured': not DEMO_MODE
    })

@app.route('/generate', methods=['POST'])
def generate_story():
    """Generate a new story"""
    try:
        data = request.get_json() if request.is_json else request.form
        
        theme = data.get('theme', '').strip()
        age_group = data.get('age_group', '6')
        child_name = data.get('child_name', '').strip()
        story_length = data.get('story_length', 'medium')
        
        if not theme:
            return jsonify({'error': 'Theme is required'}), 400
        
        # Generate the story
        result = story_generator.generate_story(theme, age_group, child_name, story_length)
        
        if result['success']:
            # Save to database
            story = Story(
                title=result['title'],
                content=result['content'],
                theme=theme,
                age_group=age_group,
                child_name=child_name if child_name else None,
                story_length=story_length
            )
            db.session.add(story)
            
            # Update theme popularity
            existing_theme = Theme.query.filter_by(name=theme.lower()).first()
            if existing_theme:
                existing_theme.popularity_score += 1
            else:
                new_theme = Theme(
                    name=theme.lower(),
                    description=f"Stories about {theme}",
                    category="user_generated",
                    popularity_score=1
                )
                db.session.add(new_theme)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'demo': result.get('demo', False),
                'story': {
                    'id': story.id,
                    'title': story.title,
                    'content': story.content,
                    'theme': story.theme,
                    'age_group': story.age_group,
                    'child_name': story.child_name,
                    'created_date': story.created_date.strftime('%B %d, %Y at %I:%M %p')
                }
            })
        else:
            return jsonify({'error': result['content']}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/stories')
def list_stories():
    """List all saved stories"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    stories = Story.query.order_by(Story.created_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('stories.html', stories=stories)

@app.route('/story/<int:story_id>')
def view_story(story_id):
    """View a specific story"""
    story = Story.query.get_or_404(story_id)
    return render_template('story.html', story=story)

@app.route('/story/<int:story_id>/edit', methods=['GET', 'POST'])
def edit_story(story_id):
    """Edit story title and notes"""
    story = Story.query.get_or_404(story_id)
    
    if request.method == 'POST':
        story.title = request.form.get('title', story.title)
        story.user_notes = request.form.get('user_notes', '')
        db.session.commit()
        return redirect(url_for('view_story', story_id=story.id))
    
    return render_template('edit_story.html', story=story)

@app.route('/story/<int:story_id>/delete', methods=['POST'])
def delete_story(story_id):
    """Delete a story"""
    story = Story.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    return redirect(url_for('list_stories'))

@app.route('/story/<int:story_id>/pdf')
def export_pdf(story_id):
    """Export story as PDF"""
    story = Story.query.get_or_404(story_id)
    pdf_buffer = generate_pdf(story)
    
    filename = f"{story.title.replace(' ', '_')}.pdf"
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/themes')
def get_themes():
    """API endpoint to get popular themes"""
    themes = Theme.query.order_by(Theme.popularity_score.desc()).limit(20).all()
    return jsonify([{
        'name': theme.name,
        'description': theme.description,
        'category': theme.category,
        'popularity': theme.popularity_score
    } for theme in themes])

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Add some default themes if none exist
        if Theme.query.count() == 0:
        default_themes = [
            {'name': 'brave princess', 'category': 'fairy_tale', 'description': 'Stories about courageous princesses'},
            {'name': 'space adventure', 'category': 'adventure', 'description': 'Exciting journeys through space'},
            {'name': 'friendly dragon', 'category': 'fantasy', 'description': 'Tales of kind-hearted dragons'},
            {'name': 'magical forest', 'category': 'fantasy', 'description': 'Adventures in enchanted forests'},
            {'name': 'underwater kingdom', 'category': 'fantasy', 'description': 'Stories from beneath the sea'},
            {'name': 'superhero animals', 'category': 'adventure', 'description': 'Animals with special powers'},
            {'name': 'time travel', 'category': 'adventure', 'description': 'Journeys through different time periods'},
            {'name': 'talking toys', 'category': 'fantasy', 'description': 'Adventures with living toys'},
        ]
        
        for theme_data in default_themes:
            theme = Theme(**theme_data, popularity_score=1)
            db.session.add(theme)
        
        db.session.commit()

# Initialize the database
create_tables()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
