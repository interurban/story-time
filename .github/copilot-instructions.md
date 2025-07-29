<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Bedtime Story Generator - Copilot Instructions

This is a Flask web application for generating personalized bedtime stories using OpenAI's GPT API.

## Project Context

- **Technology Stack**: Python 3.9+, Flask, SQLite, OpenAI API, ReportLab, Bootstrap
- **Architecture**: Monolithic web application following MVC pattern
- **Target Users**: Parents and guardians creating bedtime stories for children aged 3-12
- **Key Features**: AI story generation, story management, PDF export, mobile responsiveness

## Code Style Guidelines

- Follow PEP 8 for Python code formatting
- Use descriptive variable names and functions
- Include docstrings for classes and functions
- Maintain separation of concerns between routes, models, and services
- Use template inheritance for HTML templates
- Keep JavaScript minimal and functional

## Database Schema

- **Stories**: id, title, content, theme, age_group, child_name, story_length, created_date, user_notes
- **Themes**: id, name, description, category, popularity_score

## Security Considerations

- Always validate user input
- Sanitize content for XSS prevention
- Use environment variables for sensitive data
- Implement content filtering for child-appropriate stories
- Rate limiting for API usage

## API Integration

- OpenAI GPT-3.5-turbo for story generation
- Implement proper error handling for API failures
- Use appropriate token limits to control costs
- Include retry mechanisms for reliability

## UI/UX Principles

- Mobile-first responsive design
- Child-friendly color schemes and typography
- Clear navigation and intuitive forms
- Accessibility compliance (WCAG 2.1)
- Dark mode support for nighttime use
- Print-friendly layouts

## Performance Guidelines

- Optimize database queries
- Implement pagination for story lists
- Use appropriate caching strategies
- Minimize external dependencies
- Compress static assets

## Error Handling

- Provide user-friendly error messages
- Log detailed errors for debugging
- Graceful degradation for API failures
- Validation feedback for forms

When suggesting code changes or new features, consider:
1. Child safety and content appropriateness
2. Performance impact on story generation
3. Database efficiency and scalability
4. User experience across devices
5. API cost optimization
