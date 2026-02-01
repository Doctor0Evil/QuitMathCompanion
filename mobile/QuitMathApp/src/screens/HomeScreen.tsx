import React from "react";
import { View, Text, StyleSheet, Button } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";

import { RootStackParamList } from "../navigation";
import AbstinenceStreak from "../components/AbstinenceStreak";
import EcoKarmaBadge from "../components/EcoKarmaBadge";

type Props = NativeStackScreenProps<RootStackParamList, "Home">;

const HomeScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Quit‑Math Companion</Text>
      <AbstinenceStreak />
      <EcoKarmaBadge />
      <View style={styles.buttons}>
        <Button title="Log craving" onPress={() => navigation.navigate("CravingLog")} />
        <Button title="Start task" onPress={() => navigation.navigate("TaskPlayer")} />
        <Button title="History" onPress={() => navigation.navigate("History")} />
        <Button title="Eco impact" onPress={() => navigation.navigate("EcoImpact")} />
      </View>
    </View>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#050713"
  },
  title: {
    fontSize: 24,
    color: "#ffffff",
    fontWeight: "700",
    marginBottom: 24
  },
  buttons: {
    width: "100%",
    gap: 12,
    marginTop: 24
  }
});
