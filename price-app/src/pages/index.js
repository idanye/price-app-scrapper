import React, { useState } from 'react';
import axios from 'axios';

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
    <div style={{ padding: '20px' }}>
      <h1>Product Price Finder</h1>
      <input
        type="text"
        placeholder="Enter product name"
        value={productName}
        onChange={(e) => setProductName(e.target.value)}
        style={{ marginRight: '10px', width: '300px' }}
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Loading...' : 'Search'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {results && (
        <table border="1" style={{ marginTop: '20px', width: '100%' }}>
          <thead>
            <tr>
              <th>Store</th>
              <th>Price</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>BestBuy</td>
              <td>{results.BestBuy || 'Not available'}</td>
              <td>N/A</td>
            </tr>
            <tr>
              <td>Walmart</td>
              <td>{results.Walmart || 'Not available'}</td>
              <td>N/A</td>
            </tr>
            <tr>
              <td>Newegg</td>
              <td>{results.Newegg || 'Not available'}</td>
              <td>N/A</td>
            </tr>
          </tbody>
        </table>
      )}
    </div>
  );
}
