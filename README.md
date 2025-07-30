# Bedtime Story Generator

A Python Flask web application that generates personalized bedtime stories for children using OpenAI's GPT API. Parents can input themes or ideas, and the application creates age-appropriate short stories perfect for nighttime reading.

## Features

- **AI-Powered Story Generation**: Uses OpenAI GPT to create unique, personalized bedtime stories
- **Age-Appropriate Content**: Customizable age groups (3-12 years) with appropriate language complexity
- **Personalization**: Insert child's name to make them the hero of the story
- **Multiple Story Lengths**: Short (2-3 min), Medium (5-7 min), Long (8-10 min) reading times
- **Story Management**: Save, edit, and organize generated stories
- **PDF Export**: Download stories as beautifully formatted PDFs
- **Print-Friendly**: Optimized layouts for physical printing
- **Mobile Responsive**: Works great on phones, tablets, and desktops
- **Dark Mode**: Night-friendly reading mode
- **Popular Themes**: Quick-select from trending story themes

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or download this repository**
   ```bash
   cd storytime
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and go to `http://localhost:5000`

## 🚀 Live Demo

Want to try it without installing? **[Try the live demo here!](https://bedtime-story-generator.onrender.com)**

*Note: The demo may take 30+ seconds to load initially due to free hosting limitations.*

## 🌐 Deploy Your Own

Deploy your own version for free:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/interurban/story-time)

**Quick Deploy Steps:**
1. Click the button above
2. Sign up/log in to Render
3. Set your `OPENAI_API_KEY` environment variable
4. Deploy!

For detailed instructions, see [DEPLOY.md](DEPLOY.md).

## Usage

1. **Generate a Story**:
   - Enter a theme or idea (e.g., "brave princess", "space adventure", "friendly dragon")
   - Select the child's age (3-12 years)
   - Optionally enter the child's name to personalize the story
   - Choose story length (short, medium, or long)
   - Click "Generate Story"

2. **Manage Stories**:
   - View all saved stories in "My Stories"
   - Edit story titles and add personal notes
   - Export stories to PDF format
   - Print stories for offline reading
   - Delete unwanted stories

3. **Popular Themes**:
   - Click on popular theme chips for quick story generation
   - Themes gain popularity based on usage

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_SECRET_KEY`: Secret key for Flask sessions (required for production)
- `FLASK_ENV`: Set to `development` for debug mode
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### Customization

The application can be customized by modifying:

- **Story prompts**: Edit the prompt templates in `app.py`
- **Age ranges**: Modify age options in templates
- **Story lengths**: Adjust word counts in `StoryGenerator` class
- **Themes**: Add default themes in the database initialization
- **Styling**: Customize CSS in `templates/base.html`

## API Endpoints

- `GET /` - Home page with story generation form
- `POST /generate` - Generate a new story
- `GET /stories` - List all saved stories
- `GET /story/<id>` - View a specific story
- `GET /story/<id>/edit` - Edit story metadata
- `POST /story/<id>/delete` - Delete a story
- `GET /story/<id>/pdf` - Download story as PDF
- `GET /api/themes` - Get popular themes (JSON)

## Database Schema

### Stories Table
- `id`: Primary key
- `title`: Story title
- `content`: Full story text
- `theme`: Story theme/prompt
- `age_group`: Target age
- `child_name`: Personalized name (optional)
- `story_length`: short/medium/long
- `created_date`: Timestamp
- `user_notes`: Personal notes

### Themes Table
- `id`: Primary key
- `name`: Theme name
- `description`: Theme description
- `category`: Theme category
- `popularity_score`: Usage count

## Security Features

- Input validation to prevent harmful content
- Content filtering for child-appropriate output
- Rate limiting to prevent API abuse
- Secure API key management
- XSS protection through template escaping

## Cost Management

- OpenAI API usage is optimized with appropriate token limits
- Story generation typically costs $0.001-0.003 per story
- Monitor usage in your OpenAI dashboard
- Consider implementing user quotas for public deployments

## Development

### Project Structure
```
storytime/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── stories.html   # Story list
│   ├── story.html     # Story view
│   └── edit_story.html # Story editor
└── static/           # Static assets (if needed)
```

### Running in Development Mode

```bash
# Set environment to development
set FLASK_ENV=development  # Windows
# export FLASK_ENV=development  # macOS/Linux

# Run with auto-reload
python app.py
```

### Code Quality and Linting

The project includes tools for maintaining code quality:

**Syntax Validation**
```bash
# Check all Python files for syntax errors
python validate.py
```

**Code Linting with flake8**
```bash
# Install development dependencies (includes flake8)
pip install -r requirements.txt

# Run linting on all Python files
flake8

# Run linting on specific files
flake8 app.py validate.py
```

The project includes a `.flake8` configuration file with basic recommended rules. Flake8 will check for:
- PEP 8 style violations
- Syntax errors
- Import issues
- Code complexity
- Line length limits (88 characters)

### Database Management

The application uses SQLite by default. The database file (`stories.db`) is created automatically when you first run the app.

To reset the database:
```bash
# Stop the application
# Delete the database file
del stories.db  # Windows
# rm stories.db  # macOS/Linux
# Restart the application
```

## Deployment

### Production Considerations

1. **Environment Variables**: Set production values for all environment variables
2. **Database**: Consider PostgreSQL for production deployments
3. **Web Server**: Use Gunicorn or similar WSGI server
4. **Reverse Proxy**: Configure nginx or Apache
5. **HTTPS**: Enable SSL/TLS encryption
6. **Monitoring**: Set up logging and error tracking

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**:
   - Check your API key is correct
   - Verify you have sufficient API credits
   - Ensure your API key has the necessary permissions

2. **Story Generation Fails**:
   - Check your internet connection
   - Verify the OpenAI service status
   - Review the error message in the browser console

3. **Database Errors**:
   - Ensure the application has write permissions
   - Check if the database file is corrupted
   - Try deleting and recreating the database

4. **PDF Export Issues**:
   - Verify ReportLab is installed correctly
   - Check if there are special characters in the story

### Getting Help

- Check the error messages in the browser console
- Review the terminal output for detailed error information
- Ensure all dependencies are installed correctly
- Verify environment variables are set properly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- OpenAI for the GPT API
- Flask community for the excellent web framework
- ReportLab for PDF generation capabilities
- Bootstrap for responsive UI components

---

**Happy storytelling! 🌙📚**
