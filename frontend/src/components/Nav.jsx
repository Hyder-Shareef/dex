import { NavLink } from 'react-router-dom'

function Nav() {
  return (
    <header className="app-header">
      <div className="header-left">
        <span className="brand-name">Post Agent</span>
        <nav className="nav-tabs">
          <NavLink to="/" end className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            Generate
          </NavLink>
          <NavLink to="/approve" className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            Approve
          </NavLink>
          <NavLink to="/history" className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            History
          </NavLink>
          <NavLink to="/accounts" className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            Accounts
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default Nav
