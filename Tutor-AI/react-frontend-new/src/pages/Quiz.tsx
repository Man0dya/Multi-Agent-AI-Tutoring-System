import React, { useState } from 'react'
import { FileText, CheckCircle, Clock, Target } from 'lucide-react'

interface QuizQuestion {
  id: string
  question: string
  type: string
  options?: string[]
  correctAnswer: string
  explanation: string
  difficulty: string
  bloomLevel: string
}

interface QuizAnswer {
  questionId: string
  answer: string
}

const Quiz: React.FC = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<QuizAnswer[]>([])
  const [isCompleted, setIsCompleted] = useState(false)
  const [score, setScore] = useState(0)

  // Mock quiz questions - in real app, these would come from the Question Setter
  const mockQuestions: QuizQuestion[] = [
    {
      id: '1',
      question: 'What is the primary purpose of educational content?',
      type: 'Multiple Choice',
      options: [
        'To provide entertainment',
        'To educate and inform',
        'To sell products',
        'To confuse readers'
      ],
      correctAnswer: 'To educate and inform',
      explanation: 'Educational content is designed to provide value and increase understanding.',
      difficulty: 'Easy',
      bloomLevel: 'Understand'
    },
    {
      id: '2',
      question: 'True or False: Learning objectives help guide the educational process.',
      type: 'True/False',
      correctAnswer: 'True',
      explanation: 'Learning objectives provide clear goals and direction for both teachers and students.',
      difficulty: 'Easy',
      bloomLevel: 'Remember'
    },
    {
      id: '3',
      question: 'Explain how different learning concepts can be integrated.',
      type: 'Short Answer',
      correctAnswer: 'Concepts can be integrated by finding common themes and building connections.',
      explanation: 'Integration helps create a comprehensive understanding of the subject matter.',
      difficulty: 'Medium',
      bloomLevel: 'Analyze'
    }
  ]

  const currentQuestion = mockQuestions[currentQuestionIndex]
  const totalQuestions = mockQuestions.length
  const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100

  const handleAnswerChange = (answer: string) => {
    const existingAnswerIndex = answers.findIndex(a => a.questionId === currentQuestion.id)
    
    if (existingAnswerIndex >= 0) {
      const newAnswers = [...answers]
      newAnswers[existingAnswerIndex].answer = answer
      setAnswers(newAnswers)
    } else {
      setAnswers([...answers, { questionId: currentQuestion.id, answer }])
    }
  }

  const getCurrentAnswer = () => {
    const answer = answers.find(a => a.questionId === currentQuestion.id)
    return answer ? answer.answer : ''
  }

  const nextQuestion = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const submitQuiz = async () => {
    try {
      // Call the API to evaluate the quiz using AI agents
      const response = await fetch('/api/evaluate-quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          questions: mockQuestions,
          answers: answers.map(a => ({ questionId: a.questionId, answer: a.answer })),
          topic: 'Quiz Evaluation'
        })
      })

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const data = await response.json()
      
      // Use the AI-generated score and feedback
      setScore(data.score || 0)
      setIsCompleted(true)
      
      // Store the AI feedback for display
      localStorage.setItem('quizFeedback', JSON.stringify(data))
    } catch (error) {
      console.error('Quiz evaluation failed:', error)
      // Fallback to simple scoring if API fails
      let correctCount = 0
      answers.forEach(answer => {
        const question = mockQuestions.find(q => q.id === answer.questionId)
        if (question && answer.answer === question.correctAnswer) {
          correctCount++
        }
      })
      const finalScore = Math.round((correctCount / totalQuestions) * 100)
      setScore(finalScore)
      setIsCompleted(true)
    }
  }

  const canSubmit = answers.length === totalQuestions

  if (isCompleted) {
    return (
      <div className="space-y-8">
        <div className="text-center">
          <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Quiz Completed!</h1>
          <p className="text-xl text-gray-600">Your score: <span className="font-bold text-primary-600">{score}%</span></p>
        </div>

        <div className="card max-w-2xl mx-auto">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quiz Results</h2>
          
          {/* AI Feedback Section */}
          {(() => {
            const aiFeedback = localStorage.getItem('quizFeedback')
            if (aiFeedback) {
              try {
                const feedback = JSON.parse(aiFeedback)
                return (
                  <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h3 className="text-lg font-semibold text-blue-900 mb-3">🤖 AI Feedback</h3>
                    <div className="space-y-3">
                      <div>
                        <span className="font-medium">Overall Feedback:</span>
                        <p className="text-blue-800 mt-1">{feedback.feedback}</p>
                      </div>
                      {feedback.recommendations && feedback.recommendations.length > 0 && (
                        <div>
                          <span className="font-medium">Recommendations:</span>
                          <ul className="list-disc list-inside text-blue-800 mt-1">
                            {feedback.recommendations.map((rec: string, idx: number) => (
                              <li key={idx}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                )
              } catch (e) {
                console.error('Failed to parse AI feedback:', e)
              }
            }
            return null
          })()}
          
          <div className="space-y-4">
            {mockQuestions.map((question, index) => {
              const answer = answers.find(a => a.questionId === question.id)
              const isCorrect = answer && answer.answer === question.correctAnswer
              
              return (
                <div key={question.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-500">Question {index + 1}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {isCorrect ? 'Correct' : 'Incorrect'}
                    </span>
                  </div>
                  
                  <h4 className="font-medium text-gray-900 mb-2">{question.question}</h4>
                  
                  <div className="text-sm text-gray-600 mb-2">
                    <span className="font-medium">Your Answer:</span> {answer ? answer.answer : 'Not answered'}
                  </div>
                  
                  <div className="text-sm text-gray-600 mb-2">
                    <span className="font-medium">Correct Answer:</span> {question.correctAnswer}
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">Explanation:</span> {question.explanation}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        <div className="text-center">
          <button 
            onClick={() => window.location.reload()}
            className="btn-primary"
          >
            Take Another Quiz
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-3 mb-6">
        <FileText className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold text-gray-900">Interactive Quiz</h1>
      </div>

      {/* Progress Bar */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Target className="h-5 w-5 text-primary-600" />
            <span className="font-medium text-gray-900">Question {currentQuestionIndex + 1} of {totalQuestions}</span>
          </div>
          <div className="flex items-center space-x-2">
            <Clock className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-500">Progress: {Math.round(progress)}%</span>
          </div>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Question */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex space-x-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              currentQuestion.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
              currentQuestion.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {currentQuestion.difficulty}
            </span>
            <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {currentQuestion.bloomLevel}
            </span>
          </div>
        </div>
        
        <h2 className="text-xl font-semibold text-gray-900 mb-6">{currentQuestion.question}</h2>
        
        {/* Answer Options */}
        {currentQuestion.type === 'Multiple Choice' && currentQuestion.options && (
          <div className="space-y-3">
            {currentQuestion.options.map((option, index) => (
              <label key={index} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                <input
                  type="radio"
                  name={`question-${currentQuestion.id}`}
                  value={option}
                  checked={getCurrentAnswer() === option}
                  onChange={(e) => handleAnswerChange(e.target.value)}
                  className="text-primary-600 focus:ring-primary-500"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        )}
        
        {currentQuestion.type === 'True/False' && (
          <div className="space-y-3">
            <label className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                name={`question-${currentQuestion.id}`}
                value="True"
                checked={getCurrentAnswer() === 'True'}
                onChange={(e) => handleAnswerChange(e.target.value)}
                className="text-primary-600 focus:ring-primary-500"
              />
              <span className="text-gray-700">True</span>
            </label>
            <label className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                name={`question-${currentQuestion.id}`}
                value="False"
                checked={getCurrentAnswer() === 'False'}
                onChange={(e) => handleAnswerChange(e.target.value)}
                className="text-primary-600 focus:ring-primary-500"
              />
              <span className="text-gray-700">False</span>
            </label>
          </div>
        )}
        
        {(currentQuestion.type === 'Short Answer' || currentQuestion.type === 'Essay') && (
          <textarea
            value={getCurrentAnswer()}
            onChange={(e) => handleAnswerChange(e.target.value)}
            placeholder="Type your answer here..."
            className="input-field"
            rows={4}
          />
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={previousQuestion}
          disabled={currentQuestionIndex === 0}
          className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        
        <div className="flex space-x-3">
          {currentQuestionIndex < totalQuestions - 1 ? (
            <button
              onClick={nextQuestion}
              disabled={!getCurrentAnswer()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next Question
            </button>
          ) : (
            <button
              onClick={submitQuiz}
              disabled={!canSubmit}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Quiz
            </button>
          )}
        </div>
      </div>

      {/* Answer Summary */}
      <div className="card bg-gray-50">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Answer Summary</h3>
        <div className="grid grid-cols-5 gap-2">
          {mockQuestions.map((_, index) => {
            const isAnswered = answers.some(a => a.questionId === mockQuestions[index].id)
            const isCurrent = index === currentQuestionIndex
            
            return (
              <button
                key={index}
                onClick={() => setCurrentQuestionIndex(index)}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                  isCurrent 
                    ? 'bg-primary-600 text-white' 
                    : isAnswered 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-200 text-gray-600'
                }`}
              >
                {index + 1}
              </button>
            )
          })}
        </div>
        <div className="mt-3 text-sm text-gray-600">
          <span className="inline-block w-3 h-3 bg-green-100 rounded-full mr-2"></span>
          Answered
          <span className="inline-block w-3 h-3 bg-gray-200 rounded-full ml-4 mr-2"></span>
          Not Answered
        </div>
      </div>
    </div>
  )
}

export default Quiz
