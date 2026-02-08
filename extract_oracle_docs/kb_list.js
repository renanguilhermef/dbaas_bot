Array.from(document.querySelectorAll('title, h1, h2, h3, h4, h5, h6, a, span, div'))
  .map(e => e.textContent)
  .map(t => {
    const match = t.match(/KB\d+/g);
    return match ? match : [];
  })
  .flat()
  .filter((v, i, a) => a.indexOf(v) === i) // unique
  .forEach(kb => console.log(kb));