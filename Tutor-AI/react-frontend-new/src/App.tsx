import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ContentGenerator from './pages/ContentGenerator'
import QuestionSetter from './pages/QuestionSetter'
import Quiz from './pages/Quiz'
import FeedbackEvaluator from './pages/FeedbackEvaluator'
import ProgressTracking from './pages/ProgressTracking'
import KnowledgeBase from './pages/KnowledgeBase'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/content-generator" element={<ContentGenerator />} />
          <Route path="/question-setter" element={<QuestionSetter />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/feedback" element={<FeedbackEvaluator />} />
          <Route path="/progress" element={<ProgressTracking />} />
          <Route path="/knowledge-base" element={<KnowledgeBase />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
