from flask import Flask, render_template_string, request
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>Gensyn Peer ID Checker</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f0f2f5;
      margin: 0;
      padding: 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    h2 {
      color: #1e293b;
      font-size: 32px;
      margin-bottom: 8px;
    }

    .subtext {
      color: #475569;
      font-size: 16px;
      margin-bottom: 24px;
    }

    form {
      width: 100%;
      max-width: 640px;
    }

    textarea {
      width: 100%;
      height: 80px;
      padding: 10px;
      font-size: 14px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      resize: vertical;
      margin-bottom: 12px;
    }

    button {
      width: 100%;
      padding: 10px;
      font-size: 16px;
      background-color: #2563eb;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.2s ease-in-out;
    }

    button:hover {
      background-color: #1d4ed8;
    }

    table {
      margin-top: 30px;
      width: 100%;
      max-width: 1000px;
      border-collapse: collapse;
      background-color: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }

    th {
      background-color: #2563eb;
      color: white;
    }

    .online {
      color: green;
      font-weight: 600;
    }

    .offline {
      color: gray;
      font-weight: 600;
    }

    .error {
      color: red;
      font-style: italic;
    }

    @media screen and (max-width: 768px) {
      body {
        padding: 20px;
      }

      form, table {
        width: 100%;
      }

      textarea {
        height: 80px;
      }
    }
  </style>
</head>
<body>
  <h2>Gensyn Peer ID Checker</h2>
  <div class="subtext">Enter Peer IDs separated by new lines below.</div>

  <form method="post">
    <textarea name="peer_ids" placeholder="Example:\nQm123...\nQm456...">{{ peer_input }}</textarea>
    <button type="submit">Check</button>
  </form>

  {% if results %}
    <table>
      <tr>
        <th>Peer ID</th>
        <th>Name</th>
        <th>Reward</th>
        <th>Score</th>
        <th>Status</th>
      </tr>
      {% for pid, res in results.items() %}
        <tr>
          <td>{{ pid }}</td>
          {% if res.get("error") %}
            <td colspan="4" class="error">{{ res["error"] }}</td>
          {% else %}
            <td>{{ res["peerName"] }}</td>
            <td>{{ res["reward"] }}</td>
            <td>{{ res["score"] }}</td>
            <td class="{{ 'online' if res['online'] else 'offline' }}">{{ 'Online' if res['online'] else 'Offline' }}</td>
          {% endif %}
        </tr>
      {% endfor %}
    </table>
  {% endif %}
</body>
</html>
'''

def fetch_peer_data(peer_id):
    try:
        r = requests.get(f"https://dashboard.gensyn.ai/api/v1/peer?id={peer_id}", timeout=4)
        return r.json() if r.status_code == 200 else {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def home():
    results = {}
    peer_input = ""
    if request.method == 'POST':
        peer_input = request.form['peer_ids']
        peer_ids = [line.strip() for line in peer_input.splitlines() if line.strip()]

        # Use ThreadPoolExecutor for parallel API requests
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_pid = {executor.submit(fetch_peer_data, pid): pid for pid in peer_ids}
            for future in as_completed(future_to_pid):
                pid = future_to_pid[future]
                try:
                    results[pid] = future.result()
                except Exception as exc:
                    results[pid] = {"error": str(exc)}

    return render_template_string(HTML, results=results, peer_input=peer_input)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
