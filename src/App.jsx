import { useState } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('Dashboard')
  const [selectedImage, setSelectedImage] = useState(null)
  const [imageName, setImageName] = useState('')
  const [uploading, setUploading] = useState(false)
  const [apiResult, setApiResult] = useState(null)
  const [error, setError] = useState('')

  const tools = [
    { icon: '🍽️', title: 'Food Recognition', desc: 'Identify food items and dishes', tab: 'Food Recognition' },
    { icon: '🥗', title: 'Nutrition Analysis', desc: 'Explore calories and nutrients', tab: 'Nutrition Analysis' },
    { icon: '🍎', title: 'Freshness Detection', desc: 'Check food freshness levels', tab: 'Freshness Detection' },
    { icon: '👨‍🍳', title: 'Smart Cooking', desc: 'Get recipes and cooking guidance', tab: 'Smart Cooking' },
    { icon: '📹', title: 'Hygiene Monitoring', desc: 'Analyze kitchen hygiene', tab: 'Hygiene Monitoring' },
    { icon: '📅', title: 'Meal Planner', desc: 'Plan personalized daily meals', tab: 'Meal Planner' },
  ]

  // Upload image to backend
 function handleImageUpload(event) {
  const file = event.target.files[0]

  if (!file) return

  setSelectedImage(URL.createObjectURL(file))
  setImageName(file.name)
  setApiResult(null)
  setError('')
}
  // Recognize food using AI
async function handleFoodRecognition() {
  if (!imageName) {
    setError('Please upload a food image first.')
    return
  }

  const fileInput = document.querySelector('input[type="file"]')
  const file = fileInput?.files?.[0]

  if (!file) {
    setError('Please select your food image again.')
    return
  }

  setUploading(true)
  setError('')
  setApiResult(null)

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(
      'https://food-verse-ai-backend-xnsu.onrender.com/api/recognize-food',
      {
        method: 'POST',
        body: formData
      }
    )

    const data = await response.json()

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || 'Food recognition failed.')
    }

    setApiResult(data)

  } catch (err) {
    setError(err.message)
  } finally {
    setUploading(false)
  }
}
  // Analyze food nutrition using AI
  async function handleNutritionAnalysis() {
    if (!imageName) {
      setError('Please upload a food image first.')
      return
    }

    const fileInput = document.querySelector('input[type="file"]')
    const file = fileInput?.files?.[0]

    if (!file) {
      setError('Please select your food image again.')
      return
    }

    setUploading(true)
    setError('')
    setApiResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(
        'https://food-verse-ai-backend-xnsu.onrender.com/api/nutrition-analysis',
        {
          method: 'POST',
          body: formData
        }
      )

      const data = await response.json()

      if (!response.ok || data.status === 'error') {
        throw new Error(data.message || 'Nutrition analysis failed.')
      }

      setApiResult(data)

    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }
    // Detect food freshness using AI
  async function handleFreshnessDetection() {
    if (!imageName) {
      setError('Please upload a food image first.')
      return
    }

    const fileInput = document.querySelector('input[type="file"]')
    const file = fileInput?.files?.[0]

    if (!file) {
      setError('Please select your food image again.')
      return
    }

    setUploading(true)
    setError('')
    setApiResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(
        'https://food-verse-ai-backend-xnsu.onrender.com/api/freshness-detection',
        {
          method: 'POST',
          body: formData
        }
      )

      const data = await response.json()

      if (!response.ok || data.status === 'error') {
        throw new Error(data.message || 'Freshness detection failed.')
      }

      setApiResult(data)

    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }
  
// Smart Cooking using AI
async function handleSmartCooking() {
  if (!selectedImage) {
    setError('Please upload a food image first.')
    return
  }

  setUploading(true)
  setError('')
  setApiResult(null)

  try {
    const fileInput = document.querySelector('input[type="file"]')
    const file = fileInput.files[0]

    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(
      'https://food-verse-ai-backend-xnsu.onrender.com/api/smart-cooking',
      {
        method: 'POST',
        body: formData
      }
    )

    const data = await response.json()

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || 'Smart Cooking failed.')
    }

    setApiResult(data)
  } catch (err) {
    setError(err.message)
  } finally {
    setUploading(false)
  }
}

 // Hygiene Monitoring using AI
async function handleHygieneMonitoring() {
  if (!selectedImage) {
    setError('Please upload a food image first.')
    return
  }

  setUploading(true)
  setError('')
  setApiResult(null)

  try {
    const fileInput = document.querySelector('input[type="file"]')
    const file = fileInput.files[0]

    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(
      'https://food-verse-ai-backend-xnsu.onrender.com/api/hygiene-monitoring',
      {
        method: 'POST',
        body: formData
      }
    )

    const data = await response.json()

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || 'Hygiene Monitoring failed.')
    }

    setApiResult(data)
  } catch (err) {
    setError(err.message)
  } finally {
    setUploading(false)
  }
}

// Meal Planner using AI
async function handleMealPlanner() {
  setUploading(true)
  setError('')
  setApiResult(null)

  try {
    const dietaryPreference = document.querySelector('#dietary-preference').value
    const healthGoal = document.querySelector('#health-goal').value
    const days = document.querySelector('#meal-days').value

    const response = await fetch(
      'https://food-verse-ai-backend-xnsu.onrender.com/api/meal-planner',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          dietary_preference: dietaryPreference,
          health_goal: healthGoal,
          days: Number(days)
        })
      }
    )

    const data = await response.json()

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || 'Meal Planner failed.')
    }

    setApiResult(data)
  } catch (err) {
    setError(err.message)
  } finally {
    setUploading(false)
  }
}

  return (
    <div className="app-container">

      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <span>🍃</span>
          <div>
            <h2>Food Verse</h2>
            <p>AI FOOD INTELLIGENCE</p>
          </div>
        </div>

        <p className="menu-heading">MENU</p>

        <nav>
          {['Dashboard', 'Food Recognition', 'Nutrition Analysis',
            'Freshness Detection', 'Smart Cooking',
            'Hygiene Monitoring', 'Meal Planner'].map((item) => (
              <button
                key={item}
                className={activeTab === item ? 'nav-item active' : 'nav-item'}
                onClick={() => setActiveTab(item)}
              >
                {item === 'Dashboard' ? '🏠' :
                  item === 'Food Recognition' ? '🍽️' :
                  item === 'Nutrition Analysis' ? '🥗' :
                  item === 'Freshness Detection' ? '🍎' :
                  item === 'Smart Cooking' ? '👨‍🍳' :
                  item === 'Hygiene Monitoring' ? '📹' : '📅'}
                <span>{item}</span>
              </button>
            ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <span>💡</span>
            <h3>Need Help?</h3>
            <p>Your smart food assistant is here to help.</p>
          </div>

          <p className="version">Food Verse AI · Version 1.0</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">

        <header className="topbar">
          <div>
            <p className="welcome">WELCOME TO FOOD VERSE AI</p>
            <h1>{activeTab}</h1>
          </div>

          <div className="profile">
            <span>✨ AI Powered</span>
            <div className="avatar">FV</div>
          </div>
        </header>

        {activeTab === 'Dashboard' ? (
          <>
            {/* Hero Section */}
            <section className="hero-section">
              <div className="hero-text">
                <span className="tag">YOUR INTELLIGENT FOOD COMPANION</span>

                <h2>
                  Discover food.<br />
                  <span>Understand nutrition.</span><br />
                  Eat smarter.
                </h2>

                <p>
                  Your all-in-one AI assistant for food recognition,
                  nutrition insights, freshness detection and smart cooking.
                </p>

                <button
                  className="primary-btn"
                  onClick={() => setActiveTab('Food Recognition')}
                >
                  Explore Food AI →
                </button>
              </div>

              <div className="hero-emoji">🥑</div>
            </section>

            {/* AI Features */}
            <section className="section">
              <div className="section-heading">
                <div>
                  <h2>Explore AI Features</h2>
                  <p>Everything you need for smarter food decisions.</p>
                </div>
              </div>

              <div className="tools-grid">
                {tools.map((tool) => (
                  <button
                    className="tool-card"
                    key={tool.title}
                    onClick={() => setActiveTab(tool.tab)}
                  >
                    <span className="tool-icon">{tool.icon}</span>
                    <h3>{tool.title}</h3>
                    <p>{tool.desc}</p>
                    <span className="card-arrow">Explore →</span>
                  </button>
                ))}
              </div>
            </section>
          </>
        
          /* Image Upload Section */
         ) : activeTab === 'Meal Planner' ? (
  <section className="upload-section">
    <div className="upload-heading">
      <span className="upload-icon">📅</span>
      <h2>Meal Planner</h2>
      <p>Create your personalized AI meal plan.</p>
    </div>

    <div className="upload-box">

      <label>Dietary Preference</label>
      <select id="dietary-preference">
        <option value="Vegetarian">Vegetarian</option>
        <option value="Vegan">Vegan</option>
        <option value="Non-vegetarian">Non-vegetarian</option>
      </select>

      <label>Health Goal</label>
      <select id="health-goal">
        <option value="Balanced diet">Balanced Diet</option>
        <option value="Weight loss">Weight Loss</option>
        <option value="Weight gain">Weight Gain</option>
        <option value="Muscle building">Muscle Building</option>
      </select>

      <label>Number of Days</label>
      <select id="meal-days">
        <option value="1">1 Day</option>
        <option value="3">3 Days</option>
        <option value="5">5 Days</option>
        <option value="7">7 Days</option>
      </select>

      <button
        className="primary-btn"
        onClick={handleMealPlanner}
        disabled={uploading}
      >
        {uploading ? 'Generating Meal Plan...' : 'Generate Meal Plan with AI'}
      </button>

      {error && (
        <p className="file-name" style={{ color: 'red' }}>{error}</p>
      )}

      {apiResult?.result && (
        <div className="api-result">
          <h3>Your AI Meal Plan 🎉</h3>
          <p style={{ whiteSpace: 'pre-wrap' }}>{apiResult.result}</p>
        </div>
      )}

    </div>
  </section>
) : (
  /* Image Upload Section */
  <section className="upload-section">
            <div className="upload-heading">
              <span className="upload-icon">
                {tools.find((tool) => tool.tab === activeTab)?.icon || '✨'}
              </span>

              <h2>{activeTab}</h2>
              <p>Start by uploading an image of your food.</p>
            </div>

            <div className="upload-box">

              {selectedImage ? (
                <img
                  src={selectedImage}
                  alt="Selected food"
                  className="preview-image"
                />
              ) : (
                <>
                  <div className="upload-symbol">📸</div>
                  <h3>Upload your food image</h3>
                  <p>Choose an image from your device to get started.</p>
                </>
              )}

              {/* Choose Image Button */}
              <label className="primary-btn upload-button">
                Choose Image

                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  onChange={handleImageUpload}
                  hidden
                />
              </label>

              {/* AI Recognition Button */}
              <button
  className="primary-btn"
 onClick={
  activeTab === 'Nutrition Analysis'
    ? handleNutritionAnalysis
    : activeTab === 'Freshness Detection'
      ? handleFreshnessDetection
      : activeTab === 'Smart Cooking'
        ? handleSmartCooking
        : activeTab === 'Hygiene Monitoring'
          ? handleHygieneMonitoring
          : handleFoodRecognition
}
  disabled={uploading}
>
  {uploading
    ? 'Analyzing...'
    : activeTab === 'Nutrition Analysis'
      ? 'Analyze Nutrition with AI'
      : activeTab === 'Freshness Detection'
        ? 'Detect Food Freshness with AI'
        : 'Recognize Food with AI'}
</button>

              {imageName && (
                <p className="file-name">
                  Selected: {imageName}
                </p>
              )}

              {uploading && (
                <p className="file-name">
                  Processing your image...
                </p>
              )}

              {error && (
                <p className="file-name" style={{ color: 'red' }}>
                  {error}
                </p>
              )}

                            {/* Display Upload or AI Results */}
              {apiResult && (
                <div className="api-result">
                  {apiResult.result ? (
                    <>
                      <h3>AI Food Recognition Results 🎉</h3>
                      <p style={{ whiteSpace: 'pre-wrap' }}>
                        {apiResult.result}
                      </p>
                    </>
                  ) : apiResult.predictions ? (
                    <>
                      <h3>AI Food Recognition Results 🎉</h3>
                      {apiResult.predictions.map((item, index) => (
                        <p key={index}>
                          {index + 1}. {item.food} — {item.confidence}% confidence
                        </p>
                      ))}
                    </>
                  ) : (
                    <>
                      <h3>Image Uploaded Successfully! 🎉</h3>
                      <p>Filename: {apiResult.filename}</p>
                      <p>Format: {apiResult.image_format}</p>
                      <p>Width: {apiResult.width}px</p>
                      <p>Height: {apiResult.height}px</p>
                      <p>{apiResult.message}</p>
                    </>
                  )}
                </div>
              )}
            </div>

            <p className="notice">
              Upload a food image and let AI identify your dish.
            </p>

          </section>
        )}

        {/* Footer */}
        <footer>
          <p>
            © 2026 Food Verse AI · Making food intelligence smarter 🌱
          </p>
        </footer>

      </main>
    </div>
  )
}

export default App

