import React, { useState } from 'react'
import { Search, BookOpen, Filter, Download } from 'lucide-react'

const KnowledgeBase: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedSubject, setSelectedSubject] = useState('All')

  const subjects = ['All', 'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Literature']

  const mockResources = [
    {
      id: 1,
      title: 'Introduction to Machine Learning',
      subject: 'Computer Science',
      type: 'Study Guide',
      difficulty: 'Beginner',
      description: 'A comprehensive introduction to machine learning concepts and applications.'
    },
    {
      id: 2,
      title: 'Calculus Fundamentals',
      subject: 'Mathematics',
      type: 'Tutorial',
      difficulty: 'Intermediate',
      description: 'Core concepts of calculus with practical examples and exercises.'
    },
    {
      id: 3,
      title: 'Quantum Physics Basics',
      subject: 'Physics',
      type: 'Explanation',
      difficulty: 'Advanced',
      description: 'Understanding the fundamental principles of quantum mechanics.'
    }
  ]

  const filteredResources = mockResources.filter(resource => {
    const matchesSearch = resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         resource.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesSubject = selectedSubject === 'All' || resource.subject === selectedSubject
    return matchesSearch && matchesSubject
  })

  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-3 mb-6">
        <Search className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold text-gray-900">Knowledge Base</h1>
      </div>

      {/* Search and Filters */}
      <div className="card">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search for educational resources..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-gray-500" />
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="input-field"
            >
              {subjects.map(subject => (
                <option key={subject} value={subject}>{subject}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Resources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredResources.map(resource => (
          <div key={resource.id} className="card hover:shadow-lg transition-shadow duration-200">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-2">
                <BookOpen className="h-5 w-5 text-primary-600" />
                <span className="text-sm font-medium text-gray-500">{resource.type}</span>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                resource.difficulty === 'Beginner' ? 'bg-green-100 text-green-800' :
                resource.difficulty === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {resource.difficulty}
              </span>
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{resource.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{resource.description}</p>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">{resource.subject}</span>
              <button className="flex items-center space-x-1 text-primary-600 hover:text-primary-700 text-sm font-medium">
                <Download className="h-4 w-4" />
                <span>Access</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredResources.length === 0 && (
        <div className="card bg-gray-50 border-dashed border-2 border-gray-300">
          <div className="text-center py-12">
            <Search className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Resources Found</h3>
            <p className="text-gray-500">
              Try adjusting your search terms or filters to find educational resources.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default KnowledgeBase
