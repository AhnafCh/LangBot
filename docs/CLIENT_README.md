# RAG System Client Interface

## Overview
A simple web-based client interface to interact with your RAG (Retrieval-Augmented Generation) system.

## What's Included

### Files Created:
- **static/index.html** - A beautiful, responsive web interface for querying your RAG system

### Files Modified:
- **main.py** - Added CORS middleware and static file serving
- **rag.py** - Fixed response format to return plain text

## How to Use

### 1. Start the Server
The server should already be running. If not, start it with:
```powershell
uvicorn main:app --reload
```

### 2. Access the Client Interface
Open your web browser and go to:
```
http://localhost:8000
```

### 3. Use the Interface
- Type your question in the input field
- Click "Submit Query" or press Enter
- Wait for the response from your RAG system
- The interface will display the AI-generated answer based on your documents

## Features

✨ **Clean, Modern UI** - Beautiful gradient design with smooth animations
🚀 **Real-time Query** - Instant communication with your RAG backend
📱 **Responsive Design** - Works on desktop, tablet, and mobile
⌨️ **Keyboard Support** - Press Enter to submit queries
🔄 **Loading States** - Visual feedback while processing
❌ **Error Handling** - Clear error messages if something goes wrong

## API Endpoint

The client communicates with:
```
GET http://localhost:8000/query/?query=your_question_here
```

Response format:
```json
{
    "query": "your question",
    "response": "AI generated answer"
}
```

## Troubleshooting

### Server not starting?
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use

### Client can't connect?
- Verify the server is running on http://localhost:8000
- Check browser console (F12) for error messages
- Ensure CORS is properly configured (already done in main.py)

### No response from RAG?
- Verify your OpenAI API key is set in the `.env` file
- Check that `data/my_document.txt` exists and has content
- Look at the terminal for error messages

## Customization

You can customize the client by editing `static/index.html`:
- Change colors in the CSS section
- Modify the API_BASE_URL if your server runs on a different port
- Add more features like query history, export results, etc.

## Next Steps

Consider adding:
- [ ] Query history
- [ ] Multiple document upload
- [ ] Response formatting (markdown support)
- [ ] Authentication
- [ ] Rate limiting
- [ ] Export results to PDF/TXT
