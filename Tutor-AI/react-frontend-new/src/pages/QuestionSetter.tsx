import React, { useState } from 'react'
import { HelpCircle, Target, Zap, Brain, FileText } from 'lucide-react'

interface QuestionForm {
  content: string
  questionCount: number
  questionTypes: string[]
  difficulty: string
  subject: string
}

interface GeneratedQuestion {
  id: string
  question: string
  type: string
  options?: string[]
  correctAnswer: string
  explanation: string
  difficulty: string
  bloomLevel: string
}

const QuestionSetter: React.FC = () => {
  const [form, setForm] = useState<QuestionForm>({
    content: '',
    questionCount: 5,
    questionTypes: ['Multiple Choice'],
    difficulty: 'Medium',
    subject: 'Computer Science'
  })

  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedQuestions, setGeneratedQuestions] = useState<GeneratedQuestion[]>([])
  const [error, setError] = useState<string | null>(null)

  const questionTypes = [
    'Multiple Choice', 'True/False', 'Short Answer', 'Essay', 'Fill in the Blank'
  ]

  const difficulties = ['Easy', 'Medium', 'Hard']
  
  const subjects = [
    'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 
    'Biology', 'History', 'Literature', 'Languages', 'Business', 'Arts'
  ]

  const bloomLevels = [
    'Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create'
  ]

  const handleInputChange = (field: keyof QuestionForm, value: string | number | string[]) => {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  const handleQuestionTypeChange = (type: string, checked: boolean) => {
    if (checked) {
      setForm(prev => ({
        ...prev,
        questionTypes: [...prev.questionTypes, type]
      }))
    } else {
      setForm(prev => ({
        ...prev,
        questionTypes: prev.questionTypes.filter(t => t !== type)
      }))
    }
  }

  const generateQuestions = async () => {
    if (!form.content.trim()) {
      setError('Please enter content to generate questions from')
      return
    }

    if (form.questionTypes.length === 0) {
      setError('Please select at least one question type')
      return
    }

    setIsGenerating(true)
    setError(null)
    setGeneratedQuestions([])

    try {
      // Call the actual API endpoint to use AI agents
      const response = await fetch('/api/generate-questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: form.content,
          questionCount: form.questionCount,
          questionTypes: form.questionTypes,
          difficulty: form.difficulty,
          subject: form.subject
        })
      })

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const data = await response.json()
      
      // Transform the API response to match our interface
      const transformedQuestions: GeneratedQuestion[] = data.questions.map((q: any) => ({
        id: q.id,
        question: q.question,
        type: q.type,
        options: q.options || [],
        correctAnswer: q.correctAnswer || '',
        explanation: q.explanation || '',
        difficulty: q.difficulty || form.difficulty,
        bloomLevel: q.bloomLevel || 'Understand'
      }))
      
      setGeneratedQuestions(transformedQuestions)
    } catch (err) {
      setError('Failed to generate questions. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-3 mb-6">
        <HelpCircle className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold text-gray-900">Question Setter</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Target className="h-5 w-5 mr-2 text-primary-600" />
            Generate Assessment Questions
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content to Generate Questions From *
              </label>
              <textarea
                value={form.content}
                onChange={(e) => handleInputChange('content', e.target.value)}
                placeholder="Paste or enter the content you want to generate questions from..."
                rows={6}
                className="input-field"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Questions
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={form.questionCount}
                  onChange={(e) => handleInputChange('questionCount', parseInt(e.target.value))}
                  className="input-field"
                />
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
                Question Types *
              </label>
              <div className="grid grid-cols-2 gap-2">
                {questionTypes.map(type => (
                  <label key={type} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={form.questionTypes.includes(type)}
                      onChange={(e) => handleQuestionTypeChange(type, e.target.checked)}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-700">{type}</span>
                  </label>
                ))}
              </div>
            </div>

            <button
              onClick={generateQuestions}
              disabled={isGenerating || !form.content.trim() || form.questionTypes.length === 0}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <div className="flex items-center justify-center">
                  <Zap className="h-5 w-5 mr-2 animate-pulse" />
                  Generating Questions...
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <Brain className="h-5 w-5 mr-2" />
                  Generate Questions
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

        {/* Generated Questions */}
        <div className="space-y-6">
          {generatedQuestions.length > 0 && (
            <>
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <FileText className="h-5 w-5 mr-2 text-primary-600" />
                  Generated Questions ({generatedQuestions.length})
                </h3>
                
                <div className="space-y-6">
                  {generatedQuestions.map((question, index) => (
                    <div key={question.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-gray-500">
                          Question {index + 1}
                        </span>
                        <div className="flex space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            question.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                            question.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {question.difficulty}
                          </span>
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {question.bloomLevel}
                          </span>
                        </div>
                      </div>
                      
                      <h4 className="font-medium text-gray-900 mb-3">{question.question}</h4>
                      
                      {question.type === 'Multiple Choice' && question.options && (
                        <div className="space-y-2 mb-3">
                          {question.options.map((option, optIndex) => (
                            <div key={optIndex} className="flex items-center space-x-2">
                              <input
                                type="radio"
                                name={`question-${question.id}`}
                                value={option}
                                className="text-primary-600 focus:ring-primary-500"
                              />
                              <span className="text-sm text-gray-700">{option}</span>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {question.type === 'True/False' && (
                        <div className="space-y-2 mb-3">
                          <label className="flex items-center space-x-2">
                            <input type="radio" name={`question-${question.id}`} value="True" className="text-primary-600" />
                            <span className="text-sm text-gray-700">True</span>
                          </label>
                          <label className="flex items-center space-x-2">
                            <input type="radio" name={`question-${question.id}`} value="False" className="text-primary-600" />
                            <span className="text-sm text-gray-700">False</span>
                          </label>
                        </div>
                      )}
                      
                      {(question.type === 'Short Answer' || question.type === 'Essay') && (
                        <textarea
                          placeholder="Type your answer here..."
                          className="input-field"
                          rows={3}
                        />
                      )}
                      
                      <div className="mt-4 p-3 bg-gray-50 rounded-md">
                        <div className="text-sm">
                          <span className="font-medium text-gray-700">Correct Answer:</span>
                          <span className="ml-2 text-gray-600">{question.correctAnswer}</span>
                        </div>
                        <div className="text-sm mt-2">
                          <span className="font-medium text-gray-700">Explanation:</span>
                          <span className="ml-2 text-gray-600">{question.explanation}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card bg-green-50 border-green-200">
                <div className="text-center">
                  <h3 className="text-lg font-medium text-green-900 mb-2">Questions Generated Successfully!</h3>
                  <p className="text-green-700 text-sm mb-4">
                    You can now take a quiz with these questions or generate new ones.
                  </p>
                  <div className="flex space-x-3 justify-center">
                    <button className="btn-primary">
                      Take Quiz
                    </button>
                    <button className="btn-secondary">
                      Generate New Questions
                    </button>
                  </div>
                </div>
              </div>
            </>
          )}

          {!generatedQuestions.length && !isGenerating && (
            <div className="card bg-gray-50 border-dashed border-2 border-gray-300">
              <div className="text-center py-12">
                <HelpCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Questions Generated Yet</h3>
                <p className="text-gray-500">
                  Fill out the form and click "Generate Questions" to create assessment questions.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default QuestionSetter
