// Recomandări
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

  data.forEach(book => {
    const card = createBookCard(book);
    cardsContainer.appendChild(card);
  });
});

// Creează card carte (cu flip/rezumat)
function createBookCard(book, options = {}) {
  const card = document.createElement('div');
  card.className = 'book-card';

  const inner = document.createElement('div');
  inner.className = 'book-card-inner';

  // --- Front ---
  const front = document.createElement('div');
  front.className = 'book-card-front';

  if (book.image) {
    const img = document.createElement('img');
    img.className = 'book-image';
    img.src = `/book_images/${book.image}?v=${Date.now()}`;
    img.alt = book.title;
    front.appendChild(img);
    if (!options.hideActions) {
      // Buton ștergere imagine
      const delBtn = document.createElement('button');
      delBtn.className = 'delete-image-btn';
      delBtn.textContent = 'Șterge imagine';
      delBtn.onclick = async (e) => {
        e.stopPropagation();
        delBtn.disabled = true;
        delBtn.textContent = 'Se șterge...';
        const resp = await fetch('/delete-image/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: book.title })
        });
        const data = await resp.json();
        if (data.success) {
          book.image = "";
          const newCard = createBookCard(book);
          card.parentNode.replaceChild(newCard, card);
        } else {
          delBtn.textContent = 'Eroare!';
        }
      };
      front.appendChild(delBtn);
    }
  } else if (!options.hideActions) {
    const genBtn = document.createElement('button');
    genBtn.className = 'generate-image-btn';
    genBtn.textContent = 'Generează imagine';
    genBtn.onclick = async (e) => {
      e.stopPropagation();
      genBtn.disabled = true;
      genBtn.textContent = 'Se generează...';
      const resp = await fetch('/generate-image/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: book.title, author: book.author })
      });
      const data = await resp.json();
      if (data.image) {
        book.image = data.image;
        const newCard = createBookCard(book);
        card.parentNode.replaceChild(newCard, card);
      } else {
        genBtn.textContent = 'Eroare!';
      }
    };
    front.appendChild(genBtn);
  }

  const title = document.createElement('div');
  title.className = 'book-title';
  title.textContent = book.title;
  front.appendChild(title);

  const author = document.createElement('div');
  author.className = 'book-author';
  author.textContent = book.author;
  front.appendChild(author);

  // --- Back (rezumat) ---
  const back = document.createElement('div');
  back.className = 'book-card-back';

  const summaryTitle = document.createElement('div');
  summaryTitle.className = 'book-summary-title';
  summaryTitle.textContent = 'Rezumat';
  back.appendChild(summaryTitle);

  const summary = document.createElement('div');
  summary.className = 'book-summary';
  summary.textContent = 'Se încarcă...';
  back.appendChild(summary);

  inner.appendChild(front);
  inner.appendChild(back);
  card.appendChild(inner);

  let summaryLoaded = false;

  card.onclick = async function () {
    card.classList.toggle('flipped');
    if (!summaryLoaded && card.classList.contains('flipped')) {
      summary.textContent = 'Se încarcă...';
      try {
        const resp = await fetch('/summary/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: book.title })
        });
        const data = await resp.json();
        summary.textContent = data.summary || 'Nu există rezumat disponibil.';
        summaryLoaded = true;
      } catch {
        summary.textContent = 'Eroare la încărcarea rezumatului.';
      }
    }
  };

  return card;
}

// Navigare între secțiuni
document.getElementById('goto-recommend').onclick = () => {
  document.getElementById('recommend-section').style.display = '';
  document.getElementById('library-section').style.display = 'none';
};

document.getElementById('goto-library').onclick = () => {
  document.getElementById('recommend-section').style.display = 'none';
  document.getElementById('library-section').style.display = '';
  loadLibrary();
};

// Încărcare toate cărțile
async function loadLibrary() {
  const container = document.getElementById('library-cards');
  container.innerHTML = '';
  const resp = await fetch('/all-books/');
  const books = await resp.json();
  books.forEach(book => {
    const card = createBookCard(book, { hideActions: true });
    container.appendChild(card);
  });
}
