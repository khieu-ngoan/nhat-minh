import React from 'react';
import { render } from "react-dom";
import store from './redux/store';
import { Provider } from 'react-redux'
import './index.css';
import {App} from './app';


function AppRoot() {
  return (
    <React.Fragment>
      <Provider store={store}>
        <App />
      </Provider>
    </React.Fragment>
  );
}
render(<AppRoot />, document.getElementById("root"));
