import React from 'react'
import { Link } from 'react-router-dom'
import { 
  BookOpen, 
  HelpCircle, 
  FileText, 
  BarChart3, 
  Search, 
  Brain,
  TrendingUp,
  Users
} from 'lucide-react'

const Dashboard: React.FC = () => {
  const features = [
    {
      name: 'Content Generator',
      description: 'AI-powered educational content creation',
      icon: BookOpen,
      href: '/content-generator',
      color: 'bg-blue-500'
    },
    {
      name: 'Question Setter',
      description: 'Create intelligent assessment questions',
      icon: HelpCircle,
      href: '/question-setter',
      color: 'bg-green-500'
    },
    {
      name: 'Interactive Quiz',
      description: 'Take quizzes and test your knowledge',
      icon: FileText,
      href: '/quiz',
      color: 'bg-purple-500'
    },
    {
      name: 'AI Feedback',
      description: 'Get personalized learning feedback',
      icon: Brain,
      href: '/feedback',
      color: 'bg-orange-500'
    },
    {
      name: 'Progress Tracking',
      description: 'Monitor your learning journey',
      icon: TrendingUp,
      href: '/progress',
      color: 'bg-indigo-500'
    },
    {
      name: 'Knowledge Base',
      description: 'Search and explore educational resources',
      icon: Search,
      href: '/knowledge-base',
      color: 'bg-pink-500'
    }
  ]

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to AI Tutoring System
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Your intelligent learning companion powered by advanced AI agents. 
          Generate content, take quizzes, and receive personalized feedback to accelerate your learning journey.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BookOpen className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Content Generated</p>
              <p className="text-2xl font-semibold text-gray-900">24</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <HelpCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Questions Created</p>
              <p className="text-2xl font-semibold text-gray-900">156</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Users className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Learning Sessions</p>
              <p className="text-2xl font-semibold text-gray-900">12</p>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Learning Tools</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <Link
                key={feature.name}
                to={feature.href}
                className="card hover:shadow-lg transition-shadow duration-200 group"
              >
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg ${feature.color} text-white`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <h3 className="ml-3 text-lg font-semibold text-gray-900 group-hover:text-primary-600">
                    {feature.name}
                  </h3>
                </div>
                <p className="text-gray-600">{feature.description}</p>
                <div className="mt-4 flex items-center text-primary-600 text-sm font-medium">
                  Get Started
                  <svg className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Getting Started */}
      <div className="card bg-gradient-to-r from-primary-50 to-blue-50 border-primary-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
        <p className="text-gray-600 mb-6">
          New to the AI Tutoring System? Follow these steps to begin your learning journey:
        </p>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
            <span className="text-gray-700">Generate educational content in the Content Generator</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
            <span className="text-gray-700">Create assessment questions in the Question Setter</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
            <span className="text-gray-700">Take interactive quizzes to test your knowledge</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">4</div>
            <span className="text-gray-700">Receive personalized AI feedback and track your progress</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
