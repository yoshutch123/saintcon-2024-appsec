import { render } from "preact";

import "./style.css";

import { Router } from "preact-router";
import Login from "./login";
import RoomView from "./room";
import SignUp from "./signup";

const App = () => {
  return (
    <div class="chat-room">
      <Router>
        <RoomView path="/" />
        <Login path="/login" />
        <SignUp path="/signup" />
      </Router>
    </div>
  );
};

render(<App />, document.body);
