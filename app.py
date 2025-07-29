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
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///stories.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

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
        """Generate a bedtime story using OpenAI API"""
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
            return {
                'title': 'Story Generation Error',
                'content': f'Sorry, there was an error generating your story: {str(e)}',
                'success': False
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
    return render_template('index.html', recent_stories=recent_stories, popular_themes=popular_themes)

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
    app.run(debug=True, host='0.0.0.0', port=5000)
