import { useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", { question });
      setResponse(res.data);
    } catch (err) {
      console.error(err);
      setResponse({ answer: "Error contacting backend" });
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>AI Data Agent Chat</h1>
      <input
        style={{ width: "300px", padding: "8px" }}
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a business question..."
      />
      <button style={{ marginLeft: "10px", padding: "8px" }} onClick={askQuestion}>
        Ask
      </button>

      {loading && <p>Loading...</p>}

      {response && (
        <div style={{ marginTop: "20px" }}>
          <h3>Answer:</h3>
          <p>{response.answer}</p>

          <h3>SQL Used:</h3>
          <pre>{response.sql_used}</pre>

          <h3>Table:</h3>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                {response.table.length > 0 &&
                  Object.keys(response.table[0]).map((col) => <th key={col}>{col}</th>)}
              </tr>
            </thead>
            <tbody>
              {response.table.map((row, idx) => (
                <tr key={idx}>
                  {Object.values(row).map((val, i) => (
                    <td key={i}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          {response.table.length > 0 && (
            <>
              <h3>Revenue Chart:</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={response.table}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="product" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="revenue" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
