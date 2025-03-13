# LinkedIn Insider

LinkedIn Insider is a powerful tool that scrapes LinkedIn company pages and posts, stores the data in MongoDB, manages images through AWS S3, and provides AI-powered insights using LLAMA.

## Features

- **Company Information Scraping**: Extract detailed company profiles including name, description, industry, employee count, and specialties
- **Post Analytics**: Scrape and analyze company posts with engagement metrics (likes, comments)
- **Employee Insights**: Gather information about key employees and their roles
- **Image Management**: Automatic profile picture handling through AWS S3
- **AI-Powered Analysis**: Generate company insights using Groq's LLM API
- **Scalable Storage**: MongoDB integration for efficient data management
- **RESTful API**: FastAPI-based endpoints with filtering and pagination

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MongoDB
- **Cloud Storage**: AWS S3
- **AI Integration**: Groq API (llama-3.2-3b-preview model)
- **Scraping Tool**: Crawl4AI
- **Language**: Python 3.x

## Prerequisites

- Python 3.x
- MongoDB Atlas account
- AWS account with S3 access
- Groq API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-insider.git
   cd linkedin-insider
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` file:
   ```env
   # Groq API
   GROQ_API_KEY=your_groq_api_key

   # MongoDB
   MONGODB_URI=your_mongodb_connection_string

   # AWS
   BUCKET_NAME=your_s3_bucket_name
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET=your_aws_secret_key
   ```

## API Endpoints

### Company Information

- `GET /api/pages/{page_id}`
  - Retrieves detailed information about a company
  - Includes company profile, posts, and AI-generated insights
  - Auto-scrapes data if not in database
  - Response: LinkedInPage object containing:
    - Basic info (name, description, website, industry)
    - Follower and employee counts
    - Profile picture URL
    - Specialties list
    - Employee list
    - Recent posts
    - AI-generated insights

- `GET /api/pages`
  - List companies with filtering options
  - Query Parameters:
    - `min_followers`: Minimum follower count (optional)
    - `max_followers`: Maximum follower count (optional)
    - `industry`: Filter by industry (optional)
    - `skip`: Pagination offset (default: 0)
    - `limit`: Results per page (1-100, default: 10)
  - Response: Array of LinkedInPage objects

### Company Posts

- `GET /api/pages/{page_id}/posts`
  - Retrieve company posts with engagement metrics
  - Query Parameters:
    - `skip`: Offset (default: 0)
    - `limit`: Posts per page (1-100, default: 10)
  - Response: Array of Post objects containing:
    - Post ID
    - Content
    - Engagement metrics (likes, comments)


## License

This project is licensed under the MIT License - see the LICENSE file for details.