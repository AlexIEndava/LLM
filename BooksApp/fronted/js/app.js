// Funcție pentru recomandări
document.getElementById('recommend-btn').addEventListener('click', async () => {
  const query = document.getElementById('query-input').value;
  const list = document.getElementById('recommendations-list');
  const vulgarDiv = document.getElementById('vulgar-message');
  const anyDiv = document.getElementById('any-message');
  
  list.innerHTML = '';
  vulgarDiv.textContent = '';
  anyDiv.textContent = '';

  const response = await fetch('/recommend/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  const data = await response.json();

  // Dacă backend-ul returnează un câmp special pentru vulgaritate
  if (data.vulgar_message) {
    vulgarDiv.textContent = data.vulgar_message;
    return;
  }

  if (data.any_message) {
    anyDiv.textContent = data.any_message;
    return;
  }

  // Altfel, afișează recomandările
  data.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.title} (scor: ${item.score.toFixed(2)})`;
    list.appendChild(li);
  });
});

 

// Funcție pentru rezumat
document.getElementById('summary-btn').addEventListener('click', async () => {
  const title = encodeURIComponent(document.getElementById('title-input').value);
  const response = await fetch(`/summary/?title=${title}`);
  const data = await response.json();
  const div = document.getElementById('summary-result');
  div.innerHTML = `<h3>${data.title}</h3><p>${data.summary}</p>`;
});
