document.addEventListener('DOMContentLoaded', function () {

  // 1. Show More / Show Less functionality for long ingredient texts
  const ingredientParagraphs = document.querySelectorAll('.ingredient-paragraph');

  ingredientParagraphs.forEach((paragraph) => {
    const fullText = paragraph.textContent.trim();

    if (fullText.length > 100) {
      const shortText = fullText.substring(0, 100) + '…';
      paragraph.textContent = '';

      // Create a span to toggle text content
      const span = document.createElement('span');
      span.className = 'ingredient-text';
      span.textContent = shortText;
      paragraph.appendChild(span);

      // Add toggle button
      const toggleBtn = document.createElement('button');
      toggleBtn.className = 'btn btn-sm btn-link p-0 mt-1';
      toggleBtn.type = 'button';
      toggleBtn.textContent = 'Show More';

      let expanded = false;

      toggleBtn.addEventListener('click', () => {
        expanded = !expanded;
        span.textContent = expanded ? fullText : shortText;
        toggleBtn.textContent = expanded ? 'Show Less' : 'Show More';
      });

      paragraph.appendChild(document.createElement('br'));
      paragraph.appendChild(toggleBtn);
    }
  });

  // 2. Fade-in animation for recipe cards on page load
  const recipeCards = document.querySelectorAll('.card');
  recipeCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

    // Delay each card slightly
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 * index);
  });

  // 3. Prevent form submission if search input is empty
  const searchForm = document.querySelector('form');
  if (searchForm) {
    searchForm.addEventListener('submit', function (event) {
      const searchInput = searchForm.querySelector('input[name="query"]');
      if (!searchInput.value.trim()) {
        event.preventDefault();
        alert('Please enter a search term.');
      }
    });
  }

  // 4. Save/Unsave recipe (AJAX)
  const saveButtons = document.querySelectorAll('.save-btn');
  saveButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const recipeId = btn.dataset.recipeId;
      if (!recipeId) return;

      const response = await fetch(`/recipes/save/${recipeId}`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });

      // Toggle button style and text on success
      if (response.ok) {
        const data = await response.json();
        btn.classList.toggle('btn-success', data.saved);
        btn.classList.toggle('btn-outline-success', !data.saved);
        btn.textContent = data.saved ? 'Saved' : 'Save';
      } else {
        alert('Failed to save recipe.');
      }
    });
  });

  // 5. Unsave recipe from "Saved Recipes" page (AJAX)
  const unsaveButtons = document.querySelectorAll('.unsave-btn');
  unsaveButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const recipeId = btn.dataset.recipeId;
      const response = await fetch(`/unsave/${recipeId}`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });

      // Remove recipe card from page if successful
      if (response.ok) {
        const card = btn.closest('.col'); 
        if (card) card.remove();
      } else {
        alert('Failed to remove the recipe.');
      }
    });
  });

});
