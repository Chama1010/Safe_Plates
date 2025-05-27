document.addEventListener('DOMContentLoaded', function () {
// long ingredient lists with show more and show less
const ingredientParagraphs = document.querySelectorAll('.ingredient-paragraph');

ingredientParagraphs.forEach((paragraph) => {
  const fullText = paragraph.textContent.trim();

  if (fullText.length > 100) {
    const shortText = fullText.substring(0, 100) + '…';

    paragraph.textContent = '';

    // Create span for dynamic text
    const span = document.createElement('span');
    span.className = 'ingredient-text';
    span.textContent = shortText;
    paragraph.appendChild(span);

    // show more and less toggle button
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

// fade in animation for recipe cards
  const recipeCards = document.querySelectorAll('.card');
  recipeCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 * index);
  });

  // prevent empty search submissions
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

  // save recipe
  const saveButtons = document.querySelectorAll('.save-btn');
  saveButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const recipeId = btn.dataset.recipeId;
      if (!recipeId) return;

      const response = await fetch(`/recipes/save/${recipeId}`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });

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

  // remove recipe from saved recipes 
  const unsaveButtons = document.querySelectorAll('.unsave-btn');
  unsaveButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const recipeId = btn.dataset.recipeId;
      const response = await fetch(`/unsave/${recipeId}`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });

      if (response.ok) {
        const card = btn.closest('.col'); 
        if (card) card.remove();
      } else {
        alert('Failed to remove the recipe.');
      }
    });
  });
});















