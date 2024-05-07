import React, {useEffect, useState} from 'react';
import axios from 'axios';
import styles from '../styles/styles.module.css'; // Assume styles are defined in this CSS file

export default function Home() {
  const [inputProductName, setInputProductName] = useState(''); // To track input field
  const [displayedProductName, setDisplayedProductName] = useState(''); // To display above the table
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [bestPriceStore, setBestPriceStore] = useState('');

  useEffect(() => {
    if (results) {
      let bestPrice = Number.MAX_SAFE_INTEGER;
      let storeName = '';
      Object.keys(results).filter(key => key !== 'product_name').forEach(store => {
        const priceString = results[store].price;
        if (priceString) {
          const price = parseFloat(priceString.replace(/[^\d.]/g, ''));
          if (price < bestPrice) {
            bestPrice = price;
            storeName = store;
          }
        }
      });
      setBestPriceStore(storeName ? `The best price is at ${storeName}: ${results[storeName].price}` : 'No prices available');
    }
  }, [results]);

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    const sanitizedProductName = inputProductName.replace(/[\u201C\u201D]/g, ''); // Strip typographic quotes
    console.log(`Requesting prices for: ${sanitizedProductName}`);  // Log the sanitized product name

    try {
      const response = await axios.get(`http://localhost:8000/prices/${encodeURIComponent(sanitizedProductName)}`);
      setResults(response.data);
      setDisplayedProductName(inputProductName); // Update displayed product name on successful fetch
      setInputProductName(''); // Clear input field after search
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please try again.');
      if (results === null) setDisplayedProductName(''); // Clear displayed name if no previous results
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1>Product Price Finder</h1>
      <div className={styles.searchBar}>
        <input
            type="text"
            className={styles.inputText}
            placeholder="Enter product name"
            value={inputProductName}
            onChange={(e) => setInputProductName(e.target.value)}
        />
        <button
            className={loading ? styles.buttonDisabled : styles.button}
            onClick={handleSearch}
            disabled={loading}
        >
            {loading ? 'Loading...' : 'Search'}
        </button>
      </div>

      {error && <p className={styles.error}>{error}</p>}

      {results && (
          <>
            <h2 className={styles.header}>{displayedProductName}</h2>
            <table className={styles.table}>
              <thead>
              <tr>
                <th className={styles.th}>Store</th>
                <th className={styles.th}>Price</th>
                <th className={styles.th}>Link</th>
              </tr>
              </thead>
              <tbody>
              {Object.keys(results).filter(key => key !== 'product_name').map(store => (
                  <tr key={store}>
                    <td className={styles.td}>{store}</td>
                    <td className={styles.td}>{results[store].price || 'Not available'}</td>
                    <td className={styles.td}>
                      {results[store].link
                          ? <a className={styles.link} href={results[store].link} target="_blank"
                               rel="noopener noreferrer">Product Link</a>
                          : 'N/A'}
                    </td>
                  </tr>
              ))}
              </tbody>
            </table>
            <p className={styles.bestPrice}>{bestPriceStore}</p>
          </>
      )}
    </div>
  );
}
