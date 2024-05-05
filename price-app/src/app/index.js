import React, { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [productName, setProductName] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/prices/${encodeURIComponent(productName)}`);
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please try again.');
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  return (
      <div style={{padding: '20px'}}>
          <h1>Product Price Finder</h1>
          <input
              type="text"
              placeholder="Enter product name"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              style={{marginRight: '10px', width: '300px'}}
          />
          <button onClick={handleSearch} disabled={loading}>
              {loading ? 'Loading...' : 'Search'}
          </button>

          {error && <p style={{ color: 'red' }}>{error}</p>}

          {results && (
              <table border="1" style={{marginTop: '20px', width: '100%'}}>
                  <thead>
                  <tr>
                      <th>Store</th>
                      <th>Price</th>
                      <th>Link</th>
                  </tr>
                  </thead>
                  <tbody>
                  {results.BestBuy && (
                      <tr>
                          <td>BestBuy</td>
                          <td>{results.BestBuy.price || 'Not available'}</td>
                          <td>{results.BestBuy.url ?
                              <a href={results.BestBuy.url} target="_blank" rel="noopener noreferrer">Product
                                  Link</a> : 'N/A'}</td>
                      </tr>
                  )}
                  {results.Walmart && (
                      <tr>
                          <td>Walmart</td>
                          <td>{results.Walmart.price || 'Not available'}</td>
                          <td>{results.Walmart.url ?
                              <a href={results.Walmart.url} target="_blank" rel="noopener noreferrer">Product
                                  Link</a> : 'N/A'}</td>
                      </tr>
                  )}
                  {results.Newegg && (
                      <tr>
                          <td>Newegg</td>
                          <td>{results.Newegg.price || 'Not available'}</td>
                          <td>{results.Newegg.url ?
                              <a href={results.Newegg.url} target="_blank" rel="noopener noreferrer">Product
                                  Link</a> : 'N/A'}</td>
                      </tr>
                  )}
                  </tbody>
              </table>
          )}
      </div>
  );
}
