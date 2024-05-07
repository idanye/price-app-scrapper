import React, { useState } from 'react';
import axios from 'axios';
import styles from '../styles/styles.module.css'; // Assume styles are defined in this CSS file

export default function Home() {
  const [productName, setProductName] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    const sanitizedProductName = productName.replace(/[\u201C\u201D]/g, ''); // Strip typographic quotes
    console.log(`Requesting prices for: ${sanitizedProductName}`);  // Log the sanitized product name

    try {
      const response = await axios.get(`http://localhost:8000/prices/${encodeURIComponent(sanitizedProductName)}`);
      setResults(response.data);
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please try again.');
      setResults(null);
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
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
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
          <h2 className={styles.header}>{productName}</h2>
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
                      ? <a className={styles.link} href={results[store].link} target="_blank" rel="noopener noreferrer">Product Link</a>
                      : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
