# AI Tutoring System - React Frontend

A modern, responsive React frontend for the AI Tutoring System built with TypeScript, Vite, and Tailwind CSS.

## Features

- 🎯 **Interactive Dashboard** - Overview of learning progress and tools
- 📚 **Content Generator** - AI-powered educational content creation
- ❓ **Question Setter** - Intelligent assessment question generation
- 📝 **Interactive Quiz** - Take quizzes with real-time feedback
- 🤖 **AI Feedback** - Personalized learning feedback and evaluation
- 📊 **Progress Tracking** - Monitor learning journey and achievements
- 🔍 **Knowledge Base** - Search and explore educational resources

## Tech Stack

- **React 18** - Modern React with hooks and functional components
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API calls

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd react-frontend-new
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and visit `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Layout.tsx      # Main layout with navigation
├── pages/              # Page components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── ContentGenerator.tsx
│   ├── QuestionSetter.tsx
│   ├── Quiz.tsx
│   ├── FeedbackEvaluator.tsx
│   ├── ProgressTracking.tsx
│   └── KnowledgeBase.tsx
├── App.tsx             # Main app component with routing
├── main.tsx            # React entry point
└── index.css           # Global styles with Tailwind
```

## API Integration

The frontend is designed to work with the Python backend API. Currently, it uses mock data for demonstration purposes. To connect to the real backend:

1. Update the API endpoints in each component
2. Replace mock data with actual API calls
3. Configure the proxy in `vite.config.ts` to point to your backend

## Key Features

### Interactive Quiz System
- Multiple question types (MCQ, True/False, Short Answer, Essay)
- Real-time progress tracking
- Answer validation and scoring
- Detailed feedback and explanations

### Content Generation
- AI-powered educational content creation
- Multiple content types and difficulty levels
- Learning objectives and key concepts
- Study materials and flashcards

### Question Generation
- Intelligent question creation from content
- Bloom's taxonomy integration
- Difficulty level customization
- Multiple question type support

### Responsive Design
- Mobile-first approach
- Beautiful, modern UI
- Smooth animations and transitions
- Accessible components

## Development

### Adding New Pages

1. Create a new component in `src/pages/`
2. Add the route to `App.tsx`
3. Update the navigation in `Layout.tsx`

### Styling

- Use Tailwind CSS utility classes
- Custom components defined in `src/index.css`
- Responsive design with mobile-first approach

### State Management

- Local state with React hooks
- Context API for global state (if needed)
- Form state management with controlled components

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new code
3. Add proper error handling
4. Test on different screen sizes
5. Ensure accessibility standards

## License

This project is part of the AI Tutoring System.
