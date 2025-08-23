import React, { useState } from 'react'
import { BookOpen, Target, Zap, Brain } from 'lucide-react'

interface ContentForm {
  topic: string
  subject: string
  difficulty: string
  contentType: string
  learningObjectives: string
}

interface GeneratedContent {
  content: string
  keyConcepts: string[]
  learningObjectives: string[]
  studyMaterials?: {
    flashcards: Array<{ term: string; definition: string }>
    summary: string
  }
}

const ContentGenerator: React.FC = () => {
  const [form, setForm] = useState<ContentForm>({
    topic: '',
    subject: 'Computer Science',
    difficulty: 'Intermediate',
    contentType: 'Study Notes',
    learningObjectives: ''
  })

  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState<GeneratedContent | null>(null)
  const [error, setError] = useState<string | null>(null)

  const subjects = [
    'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 
    'Biology', 'History', 'Literature', 'Languages', 'Business', 'Arts'
  ]

  const difficulties = ['Beginner', 'Intermediate', 'Advanced']
  
  const contentTypes = [
    'Study Notes', 'Tutorial', 'Explanation', 'Summary', 'Comprehensive Guide'
  ]

  const handleInputChange = (field: keyof ContentForm, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  const generateContent = async () => {
    if (!form.topic.trim()) {
      setError('Please enter a topic')
      return
    }

    setIsGenerating(true)
    setError(null)
    setGeneratedContent(null)

    try {
      // Call the actual API endpoint to use AI agents
      const response = await fetch('/api/generate-content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: form.topic,
          subject: form.subject,
          difficulty: form.difficulty,
          contentType: form.contentType,
          learningObjectives: form.learningObjectives || undefined
        })
      })

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const data = await response.json()
      
      // Transform the API response to match our interface
      const transformedContent: GeneratedContent = {
        content: data.content || '',
        keyConcepts: data.keyConcepts || [],
        learningObjectives: data.learningObjectives || [],
        studyMaterials: data.studyMaterials || {
          flashcards: [],
          summary: ''
        }
      }
      
      setGeneratedContent(transformedContent)
    } catch (err) {
      setError('Failed to generate content. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-3 mb-6">
        <BookOpen className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold text-gray-900">Content Generator</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Target className="h-5 w-5 mr-2 text-primary-600" />
            Generate Educational Content
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Topic *
              </label>
              <input
                type="text"
                value={form.topic}
                onChange={(e) => handleInputChange('topic', e.target.value)}
                placeholder="e.g., Machine Learning, Calculus, World War II"
                className="input-field"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Subject
                </label>
                <select
                  value={form.subject}
                  onChange={(e) => handleInputChange('subject', e.target.value)}
                  className="input-field"
                >
                  {subjects.map(subject => (
                    <option key={subject} value={subject}>{subject}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Difficulty
                </label>
                <select
                  value={form.difficulty}
                  onChange={(e) => handleInputChange('difficulty', e.target.value)}
                  className="input-field"
                >
                  {difficulties.map(difficulty => (
                    <option key={difficulty} value={difficulty}>{difficulty}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <select
                value={form.contentType}
                onChange={(e) => handleInputChange('contentType', e.target.value)}
                className="input-field"
              >
                {contentTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Learning Objectives (Optional)
              </label>
              <textarea
                value={form.learningObjectives}
                onChange={(e) => handleInputChange('learningObjectives', e.target.value)}
                placeholder="What should students understand after studying this topic?"
                rows={3}
                className="input-field"
              />
            </div>

            <button
              onClick={generateContent}
              disabled={isGenerating || !form.topic.trim()}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <div className="flex items-center justify-center">
                  <Zap className="h-5 w-5 mr-2 animate-pulse" />
                  Generating Content...
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <Brain className="h-5 w-5 mr-2" />
                  Generate Content
                </div>
              )}
            </button>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Generated Content */}
        <div className="space-y-6">
          {generatedContent && (
            <>
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Generated Content</h3>
                <div className="prose prose-sm max-w-none">
                  <div dangerouslySetInnerHTML={{ __html: generatedContent.content.replace(/\n/g, '<br/>') }} />
                </div>
              </div>

              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Concepts</h3>
                <div className="space-y-2">
                  {generatedContent.keyConcepts.map((concept, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                      <span className="text-gray-700">{concept}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Learning Objectives</h3>
                <div className="space-y-2">
                  {generatedContent.learningObjectives.map((objective, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-green-600 rounded-full mt-2"></div>
                      <span className="text-gray-700">{objective}</span>
                    </div>
                  ))}
                </div>
              </div>

              {generatedContent.studyMaterials && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Study Materials</h3>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Flashcards</h4>
                      <div className="grid grid-cols-1 gap-2">
                        {generatedContent.studyMaterials.flashcards.map((card, index) => (
                          <div key={index} className="p-3 bg-gray-50 rounded-md">
                            <div className="font-medium text-gray-900">{card.term}</div>
                            <div className="text-sm text-gray-600">{card.definition}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Summary</h4>
                      <p className="text-gray-700 text-sm">{generatedContent.studyMaterials.summary}</p>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {!generatedContent && !isGenerating && (
            <div className="card bg-gray-50 border-dashed border-2 border-gray-300">
              <div className="text-center py-12">
                <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Content Generated Yet</h3>
                <p className="text-gray-500">
                  Fill out the form and click "Generate Content" to create educational materials.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ContentGenerator
