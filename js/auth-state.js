document.addEventListener('DOMContentLoaded', () => {
  const navActions = document.querySelector('.nav-actions');
  
  if (!navActions) return;

  // Listen to auth state
  auth.onAuthStateChanged(async (user) => {
    if (user) {
      // User is signed in
      const firstName = user.displayName ? user.displayName.split(' ')[0] : 'User';
      
      // Sync user with PostgreSQL backend silently
      try {
        const token = await user.getIdToken();
        fetch('http://localhost:8000/api/auth/sync', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: user.displayName || '',
            email: user.email || ''
          })
        }).catch(err => console.error("Silent sync failed", err));
      } catch(e) {}
      
      navActions.innerHTML = `

        <a href="cart.html" class="btn-ghost" style="padding: 9px 12px;" aria-label="Cart">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
        </a>
        <a href="profile.html" class="btn-primary">Hi, ${firstName}</a>
        <button class="hamburger" onclick="toggleNav()" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      `;
    } else {
      // User is signed out
      navActions.innerHTML = `

        <a href="login.html" class="btn-primary">Sign In</a>
        <button class="hamburger" onclick="toggleNav()" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      `;
    }
  });
});
