import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { Provider } from "react-redux";
import { StatusBar } from "expo-status-bar";

import { store } from "./state/store";
import { RootNavigator } from "./navigation";

export default function App() {
  return (
    <Provider store={store}>
      <NavigationContainer>
        <StatusBar style="light" />
        <RootNavigator />
      </NavigationContainer>
    </Provider>
  );
}
