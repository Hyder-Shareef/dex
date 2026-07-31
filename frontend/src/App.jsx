import { Route, Routes } from 'react-router-dom'
import Nav from './components/Nav'
import Accounts from './pages/Accounts'
import Approve from './pages/Approve'
import Generate from './pages/Generate'
import History from './pages/History'

function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<Generate />} />
        <Route path="/approve" element={<Approve />} />
        <Route path="/history" element={<History />} />
        <Route path="/accounts" element={<Accounts />} />
      </Routes>
    </>
  )
}

export default App
