import "./style.css";

import { useState } from "preact/hooks";
import { ApiClient } from "./client";

function SignUp() {
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const apiClient = new ApiClient();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password != confirmPassword) {
      //todo error
      return;
    }
    const response = await apiClient.signUp(username, name,  password);
    if (response) {
      //navigate to the next page
      const next = window.location.href.split("?").pop().split("&").map((x) => x.split("=")).find((x) => x[0] == "next");
      if (next?.length > 0) {
        window.location.href = next[1];
      } else {
        window.location.href = "/";
      }
    } else {
      //todo wrong password
    }
  };


  return (
    <div class="login-page">
      <div class="login-container">
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1em' }}>
            <label for="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onInput={(e) => setUsername(e.target.value)}
              required
              class="form-element"
            />
          </div>
          <div style={{ marginBottom: '1em' }}>
            <label for="username">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onInput={(e) => setName(e.target.value)}
              required
              class="form-element"
            />
          </div>
          <div style={{ marginBottom: '1em' }}>
            <label for="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onInput={(e) => setPassword(e.target.value)}
              required
              class="form-element"
            />
          </div>
          <div style={{ marginBottom: '1em' }}>
            <label for="password">Confirm password:</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onInput={(e) => setConfirmPassword(e.target.value)}
              required
              class="form-element"
            />
          </div>
          <button type="submit" style="padding:10px">Sign up</button>
          <a href="/login" style="margin-left:100px">I already have an account</a>
        </form>
      </div>
    </div>
  );
}

export default SignUp;