import React from 'react'
import { BarChart3, TrendingUp, Target, Award } from 'lucide-react'

const ProgressTracking: React.FC = () => {
  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-3 mb-6">
        <BarChart3 className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold text-gray-900">Progress Tracking</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Target className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Quizzes Completed</p>
              <p className="text-2xl font-semibold text-gray-900">0</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Average Score</p>
              <p className="text-2xl font-semibold text-gray-900">0%</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Award className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Learning Streak</p>
              <p className="text-2xl font-semibold text-gray-900">0 days</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Learning Journey</h2>
        <div className="text-center py-12">
          <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Start Your Learning Journey</h3>
          <p className="text-gray-500">
            Take quizzes and generate content to see your progress here.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ProgressTracking
