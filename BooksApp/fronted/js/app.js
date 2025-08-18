// Funcție pentru recomandări
document.getElementById('recommend-btn').addEventListener('click', async () => {
  const query = document.getElementById('query-input').value;
  const cardsContainer = document.getElementById('recommendations-cards');
  const vulgarDiv = document.getElementById('vulgar-message');
  const anyDiv = document.getElementById('any-message');
  cardsContainer.innerHTML = '';
  vulgarDiv.textContent = '';
  anyDiv.textContent = '';

  const response = await fetch('/recommend/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  const data = await response.json();

  if (data.vulgar_message) {
    vulgarDiv.textContent = data.vulgar_message;
    return;
  }

  if (data.any_message) {
    anyDiv.textContent = data.any_message;
    return;
  }

  // Presupunem că backend-ul returnează o listă de obiecte carte cu .image, .title, .author
  data.forEach(book => {
    const card = createBookCard(book);
    cardsContainer.appendChild(card);
  });
});

async function fetchSummary(title) {
  // Endpoint pentru rezumat (presupunem că există)
  const resp = await fetch('/summary/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  });
  const data = await resp.json();
  return data.summary || '';
}

function createBookCard(book) {
  const card = document.createElement('div');
  card.className = 'book-card';

  const inner = document.createElement('div');
  inner.className = 'book-card-inner';

  // --- Front ---
  const front = document.createElement('div');
  front.className = 'book-card-front';

  // Imagine sau buton de generare
  if (book.image) {
    const img = document.createElement('img');
    img.className = 'book-image';
    img.src = `/book_images/${book.image}`;
    img.alt = book.title;
    front.appendChild(img);
  } else {
    const genBtn = document.createElement('button');
    genBtn.className = 'generate-image-btn';
    genBtn.textContent = 'Generează imagine';
    genBtn.onclick = async (e) => {
      e.stopPropagation();
      genBtn.disabled = true;
      genBtn.textContent = 'Se generează...';
      // Apelează backend pentru generare imagine
      const resp = await fetch('/generate-image/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: book.title, author: book.author })
      });
      const data = await resp.json();
      if (data.image) {
        // Actualizează imaginea pe card
        genBtn.remove();
        const img = document.createElement('img');
        img.className = 'book-image';
        img.src = `/book_images/${data.image}`;
        img.alt = book.title;
        front.insertBefore(img, front.firstChild);
      } else {
        genBtn.textContent = 'Eroare!';
      }
    };
    front.appendChild(genBtn);
  }

  // Titlu și autor
  const title = document.createElement('div');
  title.className = 'book-title';
  title.textContent = book.title;
  front.appendChild(title);

  const author = document.createElement('div');
  author.className = 'book-author';
  author.textContent = book.author;
  front.appendChild(author);

  // Buton flip
  const flipBtn = document.createElement('button');
  flipBtn.className = 'flip-btn';
  flipBtn.textContent = 'Vezi rezumat';
  flipBtn.onclick = (e) => {
    e.stopPropagation();
    card.classList.add('flipped');
    // Lazy load summary dacă nu există deja
    if (!back.querySelector('.book-summary').textContent) {
      fetchSummary(book.title).then(summary => {
        back.querySelector('.book-summary').textContent = summary || 'Rezumat indisponibil.';
      });
    }
  };
  front.appendChild(flipBtn);

  // --- Back ---
  const back = document.createElement('div');
  back.className = 'book-card-back';

  const summary = document.createElement('div');
  summary.className = 'book-summary';
  summary.textContent = ''; // Lazy load la flip
  back.appendChild(summary);

  // Buton back
  const backBtn = document.createElement('button');
  backBtn.className = 'flip-btn';
  backBtn.textContent = 'Înapoi';
  backBtn.onclick = (e) => {
    e.stopPropagation();
    card.classList.remove('flipped');
  };
  back.appendChild(backBtn);

  inner.appendChild(front);
  inner.appendChild(back);
  card.appendChild(inner);

  return card;
}

// Funcție pentru rezumat
document.getElementById('summary-btn').addEventListener('click', async () => {
  const title = encodeURIComponent(document.getElementById('title-input').value);
  const response = await fetch(`/summary/?title=${title}`);
  const data = await response.json();
  const div = document.getElementById('summary-result');
  div.innerHTML = `<h3>${data.title}</h3><p>${data.summary}</p>`;
});
