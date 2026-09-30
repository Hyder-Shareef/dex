import { NavLink } from 'react-router-dom'

function Nav() {
  return (
    <header className="app-header">
      <div className="header-left">
        <NavLink to="/" className="brand-wrap">
          <span className="brand-logo-mark">&gt;|&lt;</span>
          <span className="brand-name">DEX</span>
        </NavLink>
      </div>

      <div className="nav-center-pill">
        <span className="pill-symbol">&gt;|&lt;</span>
        <span className="pill-dots">
          <span className="p-dot"></span>
          <span className="p-dot"></span>
          <span className="p-dot"></span>
          <span className="p-dot"></span>
          <span className="p-dot"></span>
        </span>
        <span className="pill-label">STUDIO ACTIVE</span>
      </div>

      <div className="header-right">
        <nav className="nav-tabs">
          <NavLink to="/" end className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            <span className="nav-num">01</span> GENERATE
          </NavLink>
          <NavLink to="/approve" className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            <span className="nav-num">02</span> APPROVE
          </NavLink>
          <NavLink to="/history" className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            <span className="nav-num">03</span> HISTORY
          </NavLink>
          <NavLink to="/accounts" className={({ isActive }) => `nav-tab ${isActive ? 'active' : ''}`}>
            <span className="nav-num">04</span> ACCOUNTS
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default Nav
