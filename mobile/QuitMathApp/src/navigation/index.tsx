import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import OnboardingScreen from "../screens/OnboardingScreen";
import LoginScreen from "../screens/LoginScreen";
import RegisterScreen from "../screens/RegisterScreen";
import HomeScreen from "../screens/HomeScreen";
import CravingLogScreen from "../screens/CravingLogScreen";
import TaskPlayerScreen from "../screens/TaskPlayerScreen";
import HistoryScreen from "../screens/HistoryScreen";
import EcoImpactScreen from "../screens/EcoImpactScreen";
import SettingsScreen from "../screens/SettingsScreen";

export type RootStackParamList = {
  Onboarding: undefined;
  Login: undefined;
  Register: undefined;
  Home: undefined;
  CravingLog: undefined;
  TaskPlayer: undefined;
  History: undefined;
  EcoImpact: undefined;
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export const RootNavigator = () => (
  <Stack.Navigator
    initialRouteName="Onboarding"
    screenOptions={{
      headerStyle: { backgroundColor: "#0b1020" },
      headerTintColor: "#ffffff",
      contentStyle: { backgroundColor: "#050713" }
    }}
  >
    <Stack.Screen name="Onboarding" component={OnboardingScreen} options={{ headerShown: false }} />
    <Stack.Screen name="Login" component={LoginScreen} options={{ title: "Sign in" }} />
    <Stack.Screen name="Register" component={RegisterScreen} options={{ title: "Create account" }} />
    <Stack.Screen name="Home" component={HomeScreen} options={{ title: "Quit‑Math" }} />
    <Stack.Screen name="CravingLog" component={CravingLogScreen} options={{ title: "Craving log" }} />
    <Stack.Screen name="TaskPlayer" component={TaskPlayerScreen} options={{ title: "Task session" }} />
    <Stack.Screen name="History" component={HistoryScreen} options={{ title: "History" }} />
    <Stack.Screen name="EcoImpact" component={EcoImpactScreen} options={{ title: "Eco impact" }} />
    <Stack.Screen name="Settings" component={SettingsScreen} options={{ title: "Settings" }} />
  </Stack.Navigator>
);
