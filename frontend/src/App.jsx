import { Route, Routes } from 'react-router-dom'
import Nav from './components/Nav'
import Accounts from './pages/Accounts'
import Approve from './pages/Approve'
import Generate from './pages/Generate'
import History from './pages/History'

function App() {
  return (
    <div className="cyber-frame">
      {/* Viewport corner markers from theme screenshot */}
      <div className="corner-mark top-left"><span>D</span><span className="crosshair">+</span></div>
      <div className="corner-mark top-right"><span>T</span><span className="crosshair">+</span></div>
      <div className="corner-mark bottom-left"><span>L</span><span className="crosshair">+</span></div>
      <div className="corner-mark bottom-right"><span>Y</span><span className="crosshair">+</span></div>

      <Nav />
      <div className="app-content-wrapper">
        <Routes>
          <Route path="/" element={<Generate />} />
          <Route path="/approve" element={<Approve />} />
          <Route path="/history" element={<History />} />
          <Route path="/accounts" element={<Accounts />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
