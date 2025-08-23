import React from 'react'
import { Brain, MessageSquare, TrendingUp } from 'lucide-react'

const FeedbackEvaluator: React.FC = () => {
  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-3 mb-6">
        <Brain className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold text-gray-900">AI Feedback Evaluator</h1>
      </div>

      <div className="card bg-blue-50 border-blue-200">
        <div className="text-center py-12">
          <MessageSquare className="h-16 w-16 text-blue-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-blue-900 mb-2">AI-Powered Feedback</h2>
          <p className="text-blue-700 text-lg">
            Get personalized feedback on your quiz performance and learning progress.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Quiz Results</h3>
          <p className="text-gray-600">No recent quiz results to evaluate.</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Learning Insights</h3>
          <p className="text-gray-600">Take a quiz to get personalized learning insights.</p>
        </div>
      </div>
    </div>
  )
}

export default FeedbackEvaluator
